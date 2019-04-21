from logging import getLogger
from os import getcwd
from os.path import isfile, realpath

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication

from vtk import (vtkActor, vtkBox, vtkCamera, vtkContourFilter,
                 vtkDataSetMapper, vtkExtractGeometry,
                 vtkGenericDataObjectReader, vtkImageActor,
                 vtkImageMapToColors, vtkImageReslice,
                 vtkInteractorStyleTrackballCamera, vtkLookupTable, vtkMath,
                 vtkMatrix4x4, vtkNamedColors, vtkOutlineFilter, vtkPlane,
                 vtkPointPicker, vtkPolyDataMapper, vtkRenderer)

logger = getLogger( __name__ )

################################################################################
################################################################################

class BasicScene( QObject ):

    ########################################################################

    def __init__( self, renderWindow, *args, **kwargs ):
        """
        Creates a basic scene in which isosurfaces and orthogonal slices through
        the volumetric data are visualized.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, **kwargs )

        self._renderWindow = renderWindow
        self._settings = QApplication.instance().settings

        self._observedObjectsAndTags = []
        self._slices = [None, None, None]

        self.initializeScene()

    ############################################################################

    def initializeScene( self, fileName = None, interactionStyle = None ):
        """
        Initializes the scene using the given (relative) filename and
        interaction style (Opacity/Interactive/Automatic).
        """
        logger.debug( f"initializeScene( {fileName}, {interactionStyle} )" )

        if fileName is None:
            fileName = self._settings.value( f"{__class__.__name__}/FileName", "" , type = str )

        fullName = realpath( getcwd() + fileName )

        if not isfile( fullName ) or not self._createReader( fullName ):
            logger.info( f"Unable to read file {fullName}! Creating empty renderer." )
            self._createNamedColors()
            self._createEmptyRenderer()
            return

        logger.info( f"File {fullName} read succesfully!" )
        self._settings.setValue( f"{__class__.__name__}/FileName", fileName )

        self._createNamedColors()
        self._createOutlineActor()
        self._createContour()
        self._createContourActor()              # InteractionStyle = Opacity
        self._createContourExtractionActors()   # InteractionStyle = Interactive
        self._createContourExtractionActor()    # InteractionStyle = Automatic
        self._createImageResliceActors()
        self._createRendererAndInteractor()

        if interactionStyle is None:
            interactionStyle = self._settings.value( f"{__class__.__name__}/InteractionStyle", "Opacity", type = str )
        self.setInteractionStyle( interactionStyle )
        self._settings.setValue( f"{__class__.__name__}/InteractionStyle", self._style )

        bounds = self.getBounds()
        self._min, self._max = bounds[::2], bounds[1::2]

    ############################################################################

    def getBounds( self ):
        """
        Get the bounds of the scene.
        """
        extent = self._reader.GetOutput().GetExtent()
        spacing = self._reader.GetOutput().GetSpacing()

        return [ extent[i] * spacing[i // 2] for i in range( 6 ) ]

    ############################################################################

    def getInteractionStyle( self ):
        """
        Get the current interaction style for the scene.
        """
        return self._style

    ############################################################################

    def setInteractionStyle( self, interactionStyle ):
        """
        Sets the interaction style for the scene.
        -> "Opacity"        : The outline will stay the same but with a
                              variable opacity.
        -> "Interactive"    : The outline will be split up into 1/2/4/8 pieces,
                              depending on the amount of image planes and middle-
                              mouse clicking piece will toggle its opacity.
        -> "Automatic"      : The outline will be split up into 1/2/4/8 pieces,
                              depending on the amount of image planes and the
                              piece facing the camera will be removed automatically.
        """
        logger.debug( f"setInteractionStyle( {interactionStyle} )" )

        for obj, tag in self._observedObjectsAndTags: obj.RemoveObserver( tag )
        self._observedObjectsAndTags = []

        self._renderer.RemoveAllViewProps()
        for actor in self._imageResliceActors:
            self._renderer.AddActor( actor )
        self._interactor.SetInteractorStyle( vtkInteractorStyleTrackballCamera() )

        if interactionStyle == "Opacity":
            self._style = "Opacity"
            self._renderer.AddActor( self._outlineActor )
            self._renderer.AddActor( self._contourActor )
            self._opacity = self._settings.value( f"{__class__.__name__}/Opacity", 0.4, type = float )
            self.setOpacity( self._opacity )
        elif interactionStyle == "Interactive":
            self._style = "Interactive"
            self._renderer.AddActor( self._outlineActor )
            for actor in self._contourExtractionActors:
                self._renderer.AddActor( actor )
            interactor = MouseInteractorToggleOpacity( self._renderer, self._contourExtractionActors, self._slices )
            self._interactor.SetInteractorStyle( interactor )
            self._opacity = self._settings.value( f"{__class__.__name__}/Opacity", 0.4, type = float )
            self.setOpacity( self._opacity )
        else:
            self._style = "Automatic"
            self._renderer.AddActor( self._outlineActor )
            self._renderer.AddActor( self._contourExtractionActor )
            cam = self._renderer.GetActiveCamera()
            tag = cam.AddObserver( "ModifiedEvent", self._onCameraMoved )
            self._observedObjectsAndTags.append( (cam, tag) )
            self._DOP = cam.GetDirectionOfProjection()

        self._renderer.ResetCamera()
        self._renderWindow.Render()

    ############################################################################

    def updateSlices( self, slices = [None, None, None]):
        """
        Updates the (inter)actors that depend on the position of the slices.
        """
        logger.debug( f"updateSlices( {slices} )" )

        self._slices = list( slices )

        if self._style == "Interactive":
            self._updateContourExtractionActors()
            self._interactor.GetInteractorStyle().updateSlices( self._slices )
        elif self._style == "Automatic":
            self._updateContourExtractionActor( force = True )

        self._updateImageResliceActors()

        self._renderWindow.Render()

    ############################################################################

    def getOpacity( self ):
        """
        Get the opacity value that is used in the current interaction style.
        """
        if self._style == "Automatic": return 1
        else: return self._opacity

    ############################################################################

    def setOpacity( self, value ):
        """
        Set the opacity value if used in the current interaction style.
        """
        if self._style == "Automatic": return

        self._opacity = value

        if self._style == "Opacity":
            self._contourActor.GetProperty().SetOpacity( self._opacity )
        else:
            self._interactor.GetInteractorStyle().setOpacity( self._opacity )

        self._settings.setValue( f"{__class__.__name__}/Opacity", self._opacity )

    ############################################################################

    def resetOpacity( self ):
        """
        Reset the opacity such that all actors are opaque.
        """
        if self._style == "Opacity":
            self._contourActor.GetProperty().SetOpacity( 1 )
        if self._style == "Automatic":
            self._contourExtractionActor.GetProperty().SetOpacity( 1 )
        else:
            for actor in self._contourExtractionActors:
                actor.GetProperty().SetOpacity( 1 )

    ############################################################################

    def _createReader( self, fileName ):
        """
        Creates a VTK file reader and check if the data is valid.
        """
        self._reader = vtkGenericDataObjectReader()
        self._reader.SetFileName( fileName )

        return self._reader.IsFileStructuredPoints()

    ############################################################################

    def _createNamedColors( self ):
        """
        Creates named colors for convenience.
        """
        self._colors = vtkNamedColors()
        self._colors.SetColor( "Head", (1.0000, 0.3882, 0.2784, 1.0000) )
        self._colors.SetColor( "Background", (0.1000, 0.1000, 0.2000, 1.0000) )

    ############################################################################

    def _createOutlineActor( self ):
        """
        Creates a white outline around the volumetric data for context.
        """
        self._outline = vtkOutlineFilter()
        self._outline.SetInputConnection( self._reader.GetOutputPort() )

        self._outlineMapper = vtkPolyDataMapper()
        self._outlineMapper.SetInputConnection( self._outline.GetOutputPort() )

        self._outlineActor = vtkActor()
        self._outlineActor.SetMapper( self._outlineMapper )

    ############################################################################

    def _createContour( self ):
        """
        Creates an isosurface (contour) from the volumetric data.
        """
        value = self._settings.value( f"{__class__.__name__}/ContourValue", 127, type = int )

        self._contour = vtkContourFilter()
        self._contour.SetInputConnection( self._reader.GetOutputPort() )
        self._contour.SetValue( 0, value )

    ############################################################################

    def _createContourActor( self ):
        """
        Creates an actor from the isosurface (contour). Used in the "Opacity"
        interaction style.
        """
        self._contourMapper = vtkPolyDataMapper()
        self._contourMapper.SetInputConnection( self._contour.GetOutputPort() )
        self._contourMapper.ScalarVisibilityOff()

        self._contourActor = vtkActor()
        self._contourActor.SetMapper( self._contourMapper )
        self._contourActor.GetProperty().SetColor( self._colors.GetColor3d( "Head" ) )

    ############################################################################

    def _createContourExtractionActors( self ):
        """
        Splits up the original contour into 8 pieces. Used in the "Interactive"
        interaction style.
        """
        self._boxes = [vtkBox() for _ in range( 8 )]
        for box in self._boxes: box.SetBounds( 0, 0, 0, 0, 0, 0 )

        self._contourExtractions = [vtkExtractGeometry() for _ in range( 8 )]
        for i, contourExtraction in enumerate( self._contourExtractions ):
            contourExtraction.SetInputConnection( self._contour.GetOutputPort() )
            contourExtraction.SetImplicitFunction( self._boxes[i] )
            contourExtraction.ExtractInsideOn()
            contourExtraction.ExtractBoundaryCellsOn()

        self._contourExtractionMappers = [vtkDataSetMapper() for _ in range( 8 )]
        for i, contourExtractionMapper in enumerate( self._contourExtractionMappers ):
            contourExtractionMapper.SetInputConnection( self._contourExtractions[i].GetOutputPort() )
            contourExtractionMapper.ScalarVisibilityOff()

        self._contourExtractionActors = [vtkActor() for _ in range( 8 )]
        for i, contourExtractionActor in enumerate( self._contourExtractionActors ):
            contourExtractionActor.SetMapper( self._contourExtractionMappers[i] )
            contourExtractionActor.GetProperty().SetColor( self._colors.GetColor3d( "Head" ) )

    ############################################################################

    def _createContourExtractionActor( self ):
        """
        Creates an actor that removes a cubic part of the contour. Initially,
        the whole contour is shown. Used in the "Automatic" interaction style.
        """
        self._box = vtkBox()
        self._box.SetBounds( 0, 0, 0, 0, 0, 0 )

        self._contourExtraction = vtkExtractGeometry()
        self._contourExtraction.SetInputConnection( self._contour.GetOutputPort() )
        self._contourExtraction.SetImplicitFunction( self._box )
        self._contourExtraction.ExtractInsideOff()
        self._contourExtraction.ExtractBoundaryCellsOn()

        self._contourExtractionMapper = vtkDataSetMapper()
        self._contourExtractionMapper.SetInputConnection( self._contourExtraction.GetOutputPort() )
        self._contourExtractionMapper.ScalarVisibilityOff()

        self._contourExtractionActor = vtkActor()
        self._contourExtractionActor.SetMapper( self._contourExtractionMapper )
        self._contourExtractionActor.GetProperty().SetColor( self._colors.GetColor3d( "Head" ) )

    ############################################################################

    def _createImageResliceActors( self ):
        """
        Creates three orthogonal planes that cut through the volumetric data.
        """
        self._center = self._reader.GetOutput().GetCenter()

        coronal = vtkMatrix4x4()
        coronal.DeepCopy( (0, 0, 1, self._center[0],
                           1, 0, 0, self._center[1],
                           0, 1, 0, self._center[2],
                           0, 0, 0, 1) )

        sagittal = vtkMatrix4x4()
        sagittal.DeepCopy( (0, 1, 0, self._center[0],
                            0, 0, 1, self._center[1],
                            1, 0, 0, self._center[2],
                            0, 0, 0, 1) )

        transverse = vtkMatrix4x4()
        transverse.DeepCopy( (1, 0, 0, self._center[0],
                              0, 1, 0, self._center[1],
                              0, 0, 1, self._center[2],
                              0, 0, 0, 1) )

        orientations = [coronal, sagittal, transverse]

        self._imageResliceLut = vtkLookupTable()
        self._imageResliceLut.SetRange( 0, 255 )
        self._imageResliceLut.SetValueRange( 0.0, 1.0 )
        self._imageResliceLut.SetSaturationRange( 0.0, 0.0 )
        self._imageResliceLut.SetRampToLinear()
        self._imageResliceLut.Build()

        self._imageReslices = [vtkImageReslice() for _ in range( 3 )]
        for i, imageReslice in enumerate( self._imageReslices ):
            imageReslice.SetInputConnection( self._reader.GetOutputPort() )
            imageReslice.SetResliceAxes( orientations[i] )
            imageReslice.SetOutputDimensionality( 2 )
            imageReslice.SetInterpolationModeToLinear()

        self._imageResliceMappers = [vtkImageMapToColors() for _ in range( 3 )]
        for i, imageResliceMapper in enumerate( self._imageResliceMappers ):
            imageResliceMapper.SetLookupTable( self._imageResliceLut )
            imageResliceMapper.SetInputConnection( self._imageReslices[i].GetOutputPort() )

        self._imageResliceActors = [vtkImageActor() for _ in range( 3 )]
        for i, imageResliceActor in enumerate( self._imageResliceActors ):
            imageResliceActor.GetMapper().SetInputConnection( self._imageResliceMappers[i].GetOutputPort() )
            imageResliceActor.SetUserMatrix( orientations[i] )

    ############################################################################

    def _createRendererAndInteractor( self ):
        """
        Create a renderer and interactor for the scene.
        """
        self._renderer = vtkRenderer()
        self._renderer.SetBackground( self._colors.GetColor3d( "Background" ) )
        self._interactor = self._renderWindow.GetInteractor()

        self._renderWindow.AddRenderer( self._renderer )

        self._interactor.Initialize()
        self._interactor.Start()

    ############################################################################

    def _createEmptyRenderer( self ):
        """
        Creates an empty renderer for the scene.
        """
        self._renderer = vtkRenderer()
        self._renderer.SetBackground( self._colors.GetColor3d( "Background" ) )

        self._renderWindow.AddRenderer( self._renderer )
        self._renderWindow.Render()

    ############################################################################

    def _updateContourExtractionActors( self ):
        """
        Update the contour extraction actors such that the actors split up the
        original contour into 8 pieces, depending on the location of the current
        image plane(s). Used in the "Interactive" interaction style.
        """
        slices = [None for _ in range( 3 )]

        # If slicing along an axis is disabled, cut the contour right in the
        # middle. This will make sure all 8 actors are used instead of removing
        # some. The handling of 1/2/4/8 as one will be done in the
        # MouseInteractorToggleOpacity class.
        for i, slice in enumerate( self._slices ):
            if slice is None: slices[i] = (self._min[i] + self._max[i]) // 2
            else: slices[i] = slice

        xRanges = ((self._min[0], slices[0]), (slices[0], self._max[0]))
        yRanges = ((self._min[1], slices[1]), (slices[1], self._max[1]))
        zRanges = ((self._min[2], slices[2]), (slices[2], self._max[2]))

        for i, xRange in enumerate( xRanges ):
            for j, yRange in enumerate( yRanges ):
                for k, zRange in enumerate( zRanges ):
                    self._boxes[4 * i + 2 * j + k].SetBounds( *xRange, *yRange, *zRange )

    ############################################################################

    def _updateContourExtractionActor( self, DOP = None, force = False ):
        """
        Update the contour extraction actor such that the cubic region facing
        the camera is removed from the contour. Updates the actor on sign
        changes of the DOP vector (Direction Of Projection). Forcing an update
        is also supported to allow e.g. changes in slicing. Used in the
        "Automatic" interaction style.
        """
        logger.debug( f"_updateContourExtractionActor( {DOP}, {force} )" )

        if force:
            bounds = [0 for _ in range( 6 )]

            for i in range( 3 ):
                if self._slices[i] is not None:
                    if self._DOP[i] >= 0:
                        bounds[2 * i : 2 * i + 2] = (self._min[i], self._slices[i])
                    else:
                        bounds[2 * i : 2 * i + 2] = (self._slices[i], self._max[i])
                else:
                    bounds[2 * i : 2 * i + 2] = (self._min[i], self._max[i])

            self._box.SetBounds( *bounds )
            return

        for i in range( 3 ):
            if self._slices[i] is not None:
                if self._DOP[i] >= 0:
                    if DOP[i] < 0:
                        bounds = list( self._box.GetBounds() )
                        bounds[2 * i ] = self._slices[i]
                        bounds[2 * i + 1] = self._max[i]
                        self._box.SetBounds( *bounds )
                elif DOP[i] >= 0:
                    bounds = list( self._box.GetBounds() )
                    bounds[2 * i ] = self._min[i]
                    bounds[2 * i + 1] = self._slices[i]
                    self._box.SetBounds( *bounds )

    ############################################################################

    def _updateImageResliceActors( self ):
        """
        Update the position of the image planes that cut through the volumetric
        data.
        """
        logger.debug( f"_updateImageResliceActors()" )

        for i, (slice, imageReslice) in enumerate( zip( self._slices, self._imageReslices ) ):
            if slice is None:
                self._imageResliceActors[i].SetVisibility( False )
            else:
                self._imageResliceActors[i].SetVisibility( True )
                matrix = imageReslice.GetResliceAxes()
                matrix.SetElement( i, 3, self._slices[i] )

    ############################################################################

    def _onCameraMoved( self, camera, event ):
        """
        Update the contour extraction actor and the current direction of
        projection. Used in the "Automatic" interaction style.
        """
        logger.debug( f"_onCameraMoved()" )

        DOP = camera.GetDirectionOfProjection()

        self._updateContourExtractionActor( DOP )

        self._DOP = DOP

################################################################################
################################################################################

class MouseInteractorToggleOpacity( vtkInteractorStyleTrackballCamera ):

    ############################################################################

    def __init__( self, renderer, actors, slices, parent = None ):
        """
        Custom mouse interactor used for the "Interactive" interaction style of
        the BasicScene. Toggles the opacity of the picked actor (or group of
        actors when slicing is disabled along a particular axis) on a middle-
        mouse click.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        self._renderer, self._actors, self._slices = renderer, actors, slices
        self._renderWindow = self._renderer.GetRenderWindow()
        self._opacity = 0.4

        self.AddObserver( "MiddleButtonPressEvent", self._onMiddleButtonPress )
        self.AddObserver( "MiddleButtonReleaseEvent", self._onMiddleButtonRelease )

    ############################################################################

    def updateSlices( self, slices ):
        """
        Updating the slices will require this method.
        """
        self._slices = list( slices )

    ############################################################################

    def getOpacity( self ):
        """
        Get the current opacity value.
        """
        return self._opacity

    ############################################################################

    def setOpacity( self, value ):
        """
        Set the current opacity value.
        """
        self._opacity = value

        for actor in self._actors:
            if not actor.GetProperty().GetOpacity() == 1:
                actor.GetProperty().SetOpacity( self._opacity )

    ############################################################################

    def _onMiddleButtonPress( self, object, event ):
        """
        Override to prevent other middle mouse button interactions.
        """
        logger.debug( "_onMiddleButtonPress()" )
        pass

    ############################################################################

    def _onMiddleButtonRelease( self, object, event ):
        """
        Toggle the opacity of the closest picked actor(s).
        """
        logger.debug( "_onMiddleButtonRelease()" )

        clickPosition = self.GetInteractor().GetEventPosition()

        picker = vtkPointPicker()
        picker.Pick( *clickPosition[:2], 0, self._renderer )
        pickPosition = picker.GetPickPosition()

        pickedActors = picker.GetActors()
        pickedActors.InitTraversal()

        actor = pickedActors.GetNextActor()
        if actor is None: return

        # Find the closest actor to the picked position.
        closestActor = actor
        closestDistance = vtkMath.Distance2BetweenPoints( pickPosition, actor.GetCenter() )

        while actor is not None:
            actor = pickedActors.GetNextActor()
            if actor in self._actors:
                distance = vtkMath.Distance2BetweenPoints( pickPosition, actor.GetCenter() )
                if distance < closestDistance:
                    closestDistance, closestActor = distance, actor

        # Group pieces when slicing along a particular axis has been disabled.
        # ID's of the contour extraction actors  are labeled from 0 to 7.
        idOfClosestActor = self._actors.index( closestActor )
        idsToToggle = [idOfClosestActor]

        ids = ((0, 1, 2, 3), (0, 1, 4, 5), (0, 2, 4, 6))

        for i in range( 3 ):
            idsToAppend = []
            if self._slices[i] is None:
                for id in idsToToggle:
                    if id in ids[i]: idsToAppend.append( id + 2 ** ( 2 - i ) )
                    else: idsToAppend.append( id - 2 ** ( 2 - i ) )
            idsToToggle.extend( idsToAppend )

        for id in idsToToggle:
            if self._actors[id].GetProperty().GetOpacity() == 1:
                self._actors[id].GetProperty().SetOpacity( self._opacity )
            else:
                self._actors[id].GetProperty().SetOpacity( 1 )

        self._renderWindow.Render()

################################################################################
################################################################################
