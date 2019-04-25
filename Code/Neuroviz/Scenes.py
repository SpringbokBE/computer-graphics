
from logging import getLogger
from math import sqrt
from os import getcwd
from os.path import isfile, realpath
from random import choice

from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import QApplication

from vtk import (vtkActor, vtkBox, vtkCamera, vtkContourFilter,
                 vtkDataSetMapper, vtkExtractPolyDataGeometry, vtkFloatArray,
                 vtkGenericDataObjectReader, vtkImageActor,
                 vtkImageGaussianSmooth, vtkImageMapToColors, vtkImageReslice,
                 vtkInteractorStyleTrackballCamera, vtkLookupTable, vtkMath,
                 vtkMatrix4x4, vtkNamedColors, vtkOutlineFilter, vtkPlane,
                 vtkPointPicker, vtkPolyData, vtkPolyDataMapper,
                 vtkPolyDataNormals, vtkRenderer, vtkScalarBarActor,
                 vtkSphereSource, vtkStripper, vtkWindowedSincPolyDataFilter,
                 vtkWorldPointPicker)

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

        self._observedObjectsAndTags = []   # To be able to change interaction style.
        self._slices = [None, None, None]   # Contains the index of the x, y and z slices.

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

        self._readContourInfo()
        self._createContours()
        self._createContourActors()
        self._createOctants()
        self._createOctantActors()

        self._createImageResliceActors()
        self._createRendererAndInteractor()

        if interactionStyle is None:
            interactionStyle = self._settings.value( f"{__class__.__name__}/InteractionStyle", "Opacity", type = str )

        self.setInteractionStyle( interactionStyle )
        self._settings.setValue( f"{__class__.__name__}/InteractionStyle", self._style )

    ############################################################################

    def updateSlices( self, slices = [None, None, None]):
        """
        Updates the (inter)actors that depend on the position of the slices.
        """
        logger.debug( f"updateSlices( {slices} )" )

        self._slices = list( slices )

        if self._style == "Interactive":
            self._updateOctantActors()
            self._interactor.GetInteractorStyle().updateSlices( self._slices )
        elif self._style == "Automatic":
            self._updateOctantActors()

        self._updateImageResliceActors()

        self._renderWindow.Render()

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
        for actor in self._imageResliceActors: self._renderer.AddActor( actor )
        self._interactor.SetInteractorStyle( vtkInteractorStyleTrackballCamera() )

        if interactionStyle == "Opacity":
            self._style = "Opacity"
            self._renderer.AddActor( self._outlineActor )
            for actor in self._contourActors:
                self._renderer.AddActor( actor )
        elif interactionStyle == "Interactive":
            self._style = "Interactive"
            self._renderer.AddActor( self._outlineActor )
            for actor in self._octantActors:
                actor.SetVisibility( True )
                self._renderer.AddActor( actor )
            for actor in self._contourActors[1:]:
                self._renderer.AddActor( actor )
            interactor = MouseInteractorToggleOpacity( self._renderer, self._octantActors, self._slices )
            self._interactor.SetInteractorStyle( interactor )
        else:
            self._style = "Automatic"
            self._renderer.AddActor( self._outlineActor )
            for actor in self._octantActors:
                actor.GetProperty().SetOpacity( 1 )
                self._renderer.AddActor( actor )
            for actor in self._contourActors[1:]:
                self._renderer.AddActor( actor )
            cam = self._renderer.GetActiveCamera()
            tag = cam.AddObserver( "ModifiedEvent", self._onCameraMoved )
            self._observedObjectsAndTags.append( (cam, tag) )
            self._DOP = cam.GetDirectionOfProjection()

        self._renderer.ResetCamera()
        self._renderWindow.Render()

        self._activeContourName = self._settings.value( f"{__class__.__name__}/ActiveContour", "Brain", type = str )
        self.setActiveContour( self._activeContourName )
        self._opacity = self._settings.value( f"{__class__.__name__}/Opacity", 0.4, type = float )
        self.setOpacity( self._opacity )

        # Bounds become initialized only after the actors have been added.
        bounds = self.getBounds()
        self._min, self._max = bounds[::2], bounds[1::2]

        if self._style == "Interactive":
            self._updateOctantActors()
        elif self._style == "Automatic":
            self._updateOctantActors()

        self._renderWindow.Render()

    ############################################################################

    def getBounds( self ):
        """
        Get the bounds of the scene.
        """
        extent = self._reader.GetOutput().GetExtent()
        spacing = self._reader.GetOutput().GetSpacing()

        return [ extent[i] * spacing[i // 2] for i in range( 6 ) ]

    ############################################################################

    def getContourNames( self ):
        """
        Get the names of the contours, except the "Head" contour.
        """
        return self._contourNames[1:]

    ############################################################################

    def getActiveContourName( self ):
        """
        Get the name of the active contour.
        """
        return self._activeContourName

    ############################################################################

    def setActiveContour( self, contourName ):
        """
        Set the active contour based on its name. Name "None" will display
        nothing but the "Head" contour.
        """
        for contour in self._contourActors[1:]: contour.SetVisibility( False )

        if contourName != "None":
            newContourIndex = self._contourNames.index( contourName )
            self._contourActors[newContourIndex].SetVisibility( True )

        self._activeContourName = contourName
        self._renderWindow.Render()

    ############################################################################

    def getOpacity( self ):
        """
        Get the opacity value that is used in the current interaction style.
        """
        if self._style == "Automatic": return 1

        return self._opacity

    ############################################################################

    def setOpacity( self, value ):
        """
        Set the opacity value if used in the current interaction style.
        """
        if self._style == "Automatic": return

        self._opacity = value

        if self._style == "Opacity":
            self._contourActors[0].GetProperty().SetOpacity( self._opacity )
        else:
            self._interactor.GetInteractorStyle().setOpacity( self._opacity )

        self._renderWindow.Render()
        self._settings.setValue( f"{__class__.__name__}/Opacity", self._opacity )

    ############################################################################

    def resetOpacity( self ):
        """
        Reset the opacity of the first contour actor.
        """
        if not self._style == "Opacity":
            for actor in self._octantActors:
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
        self._colors.SetColor( "Head", (1.0000, 1.0000, 1.0000, 1.0000) )
        self._colors.SetColor( "Grey matter", (1.0000, 0.6200, 0.0000, 1.0000) )
        self._colors.SetColor( "Brain", (0.0300, 1.0000, 0.0000, 1.0000) )
        self._colors.SetColor( "Lesion", (0.0000, 0.3100, 1.0000, 1.0000) )
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

    def _readContourInfo( self ):
        """
        Read the contour values (name, value) and smoothings (name, values) from
        the settings.
        """
        self._contourNames = []
        namesAndValues = self._settings.value( f"{__class__.__name__}/ContourValues", "Head->127", type = list )
        namesAndSmoothings = self._settings.value( f"{__class__.__name__}/ContourSmoothings", "Head->2/1.0/100/0.05/45.0", type = list )

        # Handle the empty and one-element list cases.
        if not isinstance( namesAndValues , list ):
            if not namesAndValues: return
            namesAndValues = (namesAndValues,)

        if not isinstance( namesAndSmoothings, list ):
            if not namesAndSmoothings: return
            namesAndSmoothings = (namesAndSmoothings, )

        # Create the dictionary that maps the contour value to the name of the contour.
        self._contourValues = {}
        for nameAndValue in namesAndValues:
            name, value = (x.strip() for x in nameAndValue.split( "->" ))
            self._contourValues[name] = int( value )
            self._contourNames.append( name )

        # Create the dictionary that maps the smoothing values to the name of the contour.
        self._contourSmoothings = {}
        for nameAndSmoothing in namesAndSmoothings:
            name, smoothing = (x.strip() for x in nameAndSmoothing.split( "->" ))
            s = smoothing.split( "/" )
            smoothing = tuple( (int( s[0] ), float( s[1] ), int( s[2] ), float( s[3] ), float( s[4] )) )
            self._contourSmoothings[name] = smoothing

        self._nContours = len( self._contourNames )

    ############################################################################

    def _createContours( self ):
        """
        Create the smoothed contours (isosurfaces). Smoothing is done on the
        input data using a Gaussian filter, and on the isosurfaces thenselves
        using a windowed sinc filter.
        """
        self._gaussians    = [None for _ in range( self._nContours )]
        self._tempContours = [None for _ in range( self._nContours )]
        self._filters      = [None for _ in range( self._nContours )]
        self._normals      = [None for _ in range( self._nContours )]
        self._contours     = [None for _ in range( self._nContours )]

        for i, (name, value) in enumerate( self._contourValues.items() ):
            if name in self._contourSmoothings:
                self._tempContours[i] = vtkContourFilter()

                radius, stdDev, iters, passBand, angle = self._contourSmoothings[name]

                if radius != 0 and stdDev != 0:
                    self._gaussians[i] = vtkImageGaussianSmooth()
                    self._gaussians[i].SetInputConnection( self._reader.GetOutputPort() )
                    self._gaussians[i].SetRadiusFactors( radius, radius, radius )
                    self._gaussians[i].SetStandardDeviations( stdDev, stdDev, stdDev )
                    self._tempContours[i].SetInputConnection( self._gaussians[i].GetOutputPort() )
                else:
                    self._tempContours[i].SetInputConnection( self._reader.GetOutputPort() )

                self._tempContours[i].SetValue( 0, value )
                self._tempContours[i].ComputeScalarsOff()
                self._tempContours[i].ComputeGradientsOff()
                self._tempContours[i].ComputeNormalsOff()

                self._filters[i] = vtkWindowedSincPolyDataFilter()
                self._filters[i].SetInputConnection( self._tempContours[i].GetOutputPort() )
                self._filters[i].SetNumberOfIterations( iters )
                self._filters[i].BoundarySmoothingOff()
                self._filters[i].FeatureEdgeSmoothingOff()
                self._filters[i].SetFeatureAngle( angle )
                self._filters[i].SetPassBand( passBand )
                self._filters[i].NonManifoldSmoothingOn()
                self._filters[i].NormalizeCoordinatesOn()
                self._filters[i].Update()

                self._normals[i] = vtkPolyDataNormals()
                self._normals[i].SetInputConnection( self._filters[i].GetOutputPort() )
                self._normals[i].SetFeatureAngle( angle )

                self._contours[i] = vtkStripper()
                self._contours[i].SetInputConnection( self._normals[i].GetOutputPort() )
            else:
                self._contours[i] = vtkContourFilter()
                self._contours[i].SetInputConnection( self._reader.GetOutputPort() )
                self._contours[i].SetValue( 0 , value )
                self._contours[i].ComputeScalarsOff()
                self._contours[i].ComputeGradientsOff()
                self._contours[i].ComputeNormalsOff()

    ############################################################################

    def _createContourActors( self ):
        """
        Creates actors from the smoothed isosurfaces (contours). Used in all
        interaction styles.
        """
        self._contourMappers = [vtkPolyDataMapper() for _ in range( self._nContours ) ]
        for i, contourMapper in enumerate( self._contourMappers ):
            contourMapper.SetInputConnection( self._contours[i].GetOutputPort() )
            contourMapper.ScalarVisibilityOff()

        self._contourActors = [vtkActor() for _ in range( self._nContours ) ]
        for i, contourActor in enumerate( self._contourActors ):
            contourActor.SetMapper( self._contourMappers[i] )
            contourActor.GetProperty().SetColor( self._colors.GetColor3d( self._contourNames[i] ) )
            contourActor.GetProperty().SetOpacity( self._colors.GetColor4d( self._contourNames[i] )[-1] )

    ############################################################################

    def _createOctants( self ):
        """
        """
        name = self._contourNames[0]

        self._boxes = [vtkBox() for _ in range( 8 )]
        for box in self._boxes: box.SetBounds( 0, 0, 0, 0, 0, 0 )

        self._contour = vtkContourFilter()
        self._contour.SetInputConnection( self._reader.GetOutputPort() )
        self._contour.SetValue( 0 , self._contourValues[name] )
        self._contour.ComputeScalarsOff()
        self._contour.ComputeGradientsOff()
        self._contour.ComputeNormalsOff()

        self._extractions = [vtkExtractPolyDataGeometry() for _ in range( 8 )]
        for i, extraction in enumerate( self._extractions ):
            extraction.SetInputConnection( self._contour.GetOutputPort() )
            extraction.SetImplicitFunction( self._boxes[i] )
            extraction.ExtractInsideOn()
            extraction.ExtractBoundaryCellsOn()

        if name in self._contourSmoothings:
            radius, stdDev, iters, passBand, angle = self._contourSmoothings[name]

            self._extractionFilters = [vtkWindowedSincPolyDataFilter() for _ in range( 8 )]
            for i, extractionFilter in enumerate( self._extractionFilters ):
                extractionFilter.SetInputConnection( self._extractions[i].GetOutputPort() )
                extractionFilter.SetNumberOfIterations( iters )
                extractionFilter.BoundarySmoothingOff()
                extractionFilter.FeatureEdgeSmoothingOff()
                extractionFilter.SetFeatureAngle( angle )
                extractionFilter.SetPassBand( passBand )
                extractionFilter.NonManifoldSmoothingOn()
                extractionFilter.NormalizeCoordinatesOn()
                extractionFilter.Update()

            self._extractionNormals = [vtkPolyDataNormals() for _ in range( 8 )]
            for i, extractionNormal in enumerate( self._extractionNormals ):
                extractionNormal.SetInputConnection( self._extractionFilters[i].GetOutputPort() )
                extractionNormal.SetFeatureAngle( angle )

            self._octants = [vtkStripper() for _ in range( 8 )]
            for i, octant in enumerate( self._octants ):
                octant.SetInputConnection( self._extractionNormals[i].GetOutputPort() )
        else:
            self._octants = self._extractions

    ############################################################################

    def _createOctantActors( self ):
        """
        """
        self._octantMappers = [vtkPolyDataMapper() for _ in range( 8 )]
        for i, octantMapper in enumerate( self._octantMappers ):
            octantMapper.SetInputConnection( self._octants[i].GetOutputPort() )
            octantMapper.ScalarVisibilityOff()

        self._octantActors = [vtkActor() for _ in range( 8 )]
        for i, octantActor in enumerate( self._octantActors ):
            octantActor.SetMapper( self._octantMappers[i] )
            octantActor.GetProperty().SetColor( self._colors.GetColor3d( "Head" ) )

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

    def _updateOctantActors( self ):
        """
        Update the octant actors so they match the current slice positions.
        """
        slices = [None for _ in range( 3 )]

        # If slicing along an axis is disabled, cut the contour right in the
        # middle. This will make sure all octants are used instead of removing
        # some. The handling of the octants as one will be done in the
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

        if self._style == "Automatic":
            self._updateOctantActorsVisibility( force = True )

    ############################################################################

    def _updateOctantActorsVisibility( self, DOP = None, force = False ):
        """
        Update the octant actor such that the octant facing the camera is
        not shown. Updates the octants on sign changes of the DOP vector
        (Direction Of Projection). Forcing an update is also supported to allow
        e.g. changes in slicing. Used in the "Automatic" interaction style.
        """
        logger.debug( f"_updateOctantActorsVisibility( {force} )" )

        if not force:
            signChanged = False

            for i in range( 3 ):
                if self._slices[i] is not None:
                    if self._DOP[i] >= 0:
                        if DOP[i] < 0: signChanged = True
                    elif DOP[i] >= 0: signChanged = True

            if signChanged: self._DOP = DOP
            else: return

        notToShow = set( range( 8 ) )

        if self._slices[0] is not None:
            if self._DOP[0] >= 0: notToShow &= {0, 1, 2, 3}
            else: notToShow &= {4, 5, 6, 7}

        if self._slices[1] is not None:
            if self._DOP[1] >= 0: notToShow &= {0, 1, 4, 5}
            else: notToShow &= {2, 3, 6, 7}

        if self._slices[2] is not None:
            if self._DOP[2] >= 0: notToShow &= {0, 2, 4, 6}
            else: notToShow &= {1, 3, 5, 7}

        toShow = set( range( 8 ) ) - notToShow

        for index in toShow:
            self._octantActors[index].SetVisibility( True )

        for index in notToShow:
            self._octantActors[index].SetVisibility( False )

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
        # logger.debug( f"_onCameraMoved()" )

        DOP = camera.GetDirectionOfProjection()
        self._updateOctantActorsVisibility( DOP )

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

        pickedProp3Ds = picker.GetProp3Ds()
        pickedProp3Ds.InitTraversal()

        pickedActors = set()

        prop3D = pickedProp3Ds.GetNextProp3D()
        while prop3D is not None:
            actor = vtkActor.SafeDownCast( prop3D )
            if actor: pickedActors.add( actor )
            prop3D = pickedProp3Ds.GetNextProp3D()

        closestActor, closestDistance = None, float( "inf" )

        for actor in pickedActors:
            distance = vtkMath.Distance2BetweenPoints( pickPosition, actor.GetCenter() )
            if distance < closestDistance:
                closestDistance, closestActor = distance, actor

        if closestActor is None: return

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

class EEGScene( QObject ):

    ############################################################################

    def __init__( self, renderWindow, *args, **kwargs ):
        """
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, **kwargs )

        self._renderWindow = renderWindow
        self._settings = QApplication.instance().settings

        self._electrodeActors = []
        self._electrodePositions = []
        self._electrodeValues = []

        self.initializeScene()

        self._timer = QTimer()
        self._timer.timeout.connect( self._onTimeout )

    ############################################################################

    def initializeScene( self, fileName = None ):
        """
        """
        logger.debug( f"initializeScene( {fileName} )" )

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
        self._readContourInfo()
        self._createContour()
        self._interpolateContour()
        self._smoothContour()
        self._createContourActor()
        self._createRendererAndInteractor()

        interactor = MouseInteractorAddElectrode( self._renderer, self._contourActor, self.addElectrode )
        self._interactor.SetInteractorStyle( interactor )

        ###

        self._scalarBarActor = vtkScalarBarActor()
        self._scalarBarActor.SetLookupTable( self._contourMapper.GetLookupTable() )
        self._scalarBarActor.SetNumberOfLabels( 5 )

        ###
        self._renderer.AddActor( self._outlineActor )
        self._renderer.AddActor( self._contourActor )
        self._renderer.AddActor2D( self._scalarBarActor )
        self._renderer.ResetCamera()
        self._renderWindow.Render()

    ############################################################################

    def addElectrode( self, position ):
        """
        """
        self._sphere = vtkSphereSource()
        self._sphere.SetCenter( position )
        self._sphere.SetRadius( 5.0 )

        self._sphereMapper = vtkPolyDataMapper()
        self._sphereMapper.SetInputConnection( self._sphere.GetOutputPort() )

        self._sphereActor = vtkActor()
        self._sphereActor.SetMapper( self._sphereMapper )

        self._renderer.AddActor( self._sphereActor )

        if len( self._electrodeActors ) < 8:
            self._electrodeActors.append( self._sphereActor )
            self._electrodePositions.append( position )
            self._electrodeValues.append( choice( (0.0, 0.5, 1.0) ) )
            if len( self._electrodeActors ) == 8:
                self._renderWindow.Render()
                self._interpolateContour()
                self._timer.start( 5_000 )
        else:
            self._renderer.RemoveActor( self._electrodeActors[0] )
            self._electrodeActors = self._electrodeActors[1:] + [ self._sphereActor ]
            self._electrodePositions = self._electrodePositions[1:] + [ position ]
            self._electrodeValues = self._electrodeValues[1:] + [ choice( (0.0, 0.5, 1.0) ) ]
            self._renderWindow.Render() # Show the actor before interpolating.
            self._interpolateContour()

        self._renderWindow.Render()

    ############################################################################

    def getBounds( self ):
        """
        Get the bounds of the scene.
        """
        extent = self._reader.GetOutput().GetExtent()
        spacing = self._reader.GetOutput().GetSpacing()

        return [ extent[i] * spacing[i // 2] for i in range( 6 ) ]

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

    def _readContourInfo( self ):
        """
        """
        self._contourValue = self._settings.value( f"{__class__.__name__}/ContourValue", "169", type = int )
        self._contourSmoothing = self._settings.value( f"{__class__.__name__}/ContourSmoothing", "0/0.0/20/0.5/45.0", type = str )
        s = tuple( x.strip() for x in self._contourSmoothing.split( "/" ) )
        self._contourSmoothing = tuple( (int( s[0] ), float( s[1] ), int( s[2] ), float( s[3] ), float( s[4] )) )

    ############################################################################

    def _createContour( self ):
        """
        """
        self._gaussian = vtkImageGaussianSmooth()
        self._contour = vtkContourFilter()

        radius, stdDev, iters, passBand, angle = self._contourSmoothing

        if radius != 0 and stdDev != 0:
            self._gaussian.SetInputConnection( self._reader.GetOutputPort() )
            self._gaussian.SetRadiusFactors( radius, radius, radius )
            self._gaussian.SetStandardDeviations( stdDev, stdDev, stdDev )
            self._contour.SetInputConnection( self._gaussian.GetOutputPort() )
        else:
            self._contour.SetInputConnection( self._reader.GetOutputPort() )

        self._contour.SetValue( 0, self._contourValue )
        self._contour.ComputeScalarsOff()
        self._contour.ComputeGradientsOff()
        self._contour.ComputeNormalsOff()
        self._contour.Update() # !!!

    ############################################################################

    def _interpolateContour( self ):
        """
        """
        if not self._electrodePositions:
            self._filter = vtkWindowedSincPolyDataFilter()
            self._filter.SetInputData( self._contour.GetOutput() )
            return

        logger.debug( "Interpolating..." )
        nElectrodes = len( self._electrodeActors )
        nPoints = self._contour.GetOutput().GetNumberOfPoints()

        self._scalars = vtkFloatArray()
        self._scalars.SetNumberOfValues( nPoints )

        self._interpolatedContour = vtkPolyData()
        self._interpolatedContour.DeepCopy( self._contour.GetOutput() )

        p = [0.0, 0.0, 0.0]

        for i in range( 0, nPoints ):
            self._interpolatedContour.GetPoint( i, p )
            dists = tuple( vtkMath.Distance2BetweenPoints( self._electrodePositions[j], p ) for j in range( nElectrodes ) )

            if 0 in dists:
                id = self._electrodePositions.index( tuple( p ) )
                self._scalars.SetValue( i, self._electrodeValues[id] )
                continue

            inverseDists = tuple( 1 / dists[j] for j in range( nElectrodes ) )
            value = 0
            for j in range( nElectrodes ):
                value += inverseDists[j] * self._electrodeValues[j]

            self._scalars.SetValue( i, value / sum( inverseDists ) )

        self._interpolatedContour.GetPointData().SetScalars( self._scalars )
        self._filter.SetInputData( self._interpolatedContour )

    ############################################################################

    def _smoothContour( self ):
        """
        """
        radius, stdDev, iters, passBand, angle = self._contourSmoothing

        self._filter.SetNumberOfIterations( iters )
        self._filter.BoundarySmoothingOff()
        self._filter.FeatureEdgeSmoothingOff()
        self._filter.SetFeatureAngle( angle )
        self._filter.SetPassBand( passBand )
        self._filter.NonManifoldSmoothingOn()
        self._filter.NormalizeCoordinatesOn()
        self._filter.Update()

        self._normal = vtkPolyDataNormals()
        self._normal.SetInputConnection( self._filter.GetOutputPort() )
        self._normal.SetFeatureAngle( angle )

        self._smoothedContour = vtkStripper()
        self._smoothedContour.SetInputConnection( self._normal.GetOutputPort() )

    ############################################################################

    def _createContourActor( self ):
        """
        """
        self._contourMapper = vtkPolyDataMapper()
        self._contourMapper.SetInputConnection( self._smoothedContour.GetOutputPort() )
        self._contourMapper.ScalarVisibilityOn()
        self._contourMapper.SetScalarModeToUsePointData()
        self._contourMapper.SetColorModeToMapScalars()

        self._contourActor = vtkActor()
        self._contourActor.SetMapper( self._contourMapper )

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

    def _onTimeout( self ):
        """
        """
        logger.debug( f"_onTimeout()" )

        self._renderWindow.Render()

        self._electrodeValues = [ choice( (0.0, 0.5, 1.0) ) for _ in range( len( self._electrodeActors ) ) ]

        print( f"Values = {self._electrodeValues}" )

        self._interpolateContour()

################################################################################
################################################################################

class MouseInteractorAddElectrode( vtkInteractorStyleTrackballCamera ):

    ############################################################################

    def __init__( self, renderer, brain, callback, parent = None ):
        """
        """
        logger.info( f"Creating {__class__.__name__}..." )

        self._electrodeActors, self._electrodePositions, self._electrodeValues = [], [], []
        self._renderer, self._brain, self._callback = renderer, brain, callback
        self._renderWindow = self._renderer.GetRenderWindow()
        self.AddObserver( "MiddleButtonPressEvent", self._onMiddleButtonPress )
        self.AddObserver( "MiddleButtonReleaseEvent", self._onMiddleButtonRelease )

    ############################################################################

    def getElectrodePositions( self ):
        """
        """
        return self._electrodePositions

    ############################################################################

    def getElectrodeValues( self ):
        """
        """
        return self._electrodeValues

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
        Add a new electrode.
        """
        logger.debug( "_onMiddleButtonRelease()" )

        clickPosition = self.GetInteractor().GetEventPosition()

        picker = vtkPointPicker()
        picker.Pick( *clickPosition[:2], 0, self._renderer )
        pickPosition = picker.GetPickPosition()

        pickedProp3Ds = picker.GetProp3Ds()
        pickedProp3Ds.InitTraversal()

        pickedActors = set()

        prop3D = pickedProp3Ds.GetNextProp3D()
        while prop3D is not None:
            actor = vtkActor.SafeDownCast( prop3D )
            if actor: pickedActors.add( actor )
            prop3D = pickedProp3Ds.GetNextProp3D()

        if not self._brain in pickedActors: return

        worldPicker = vtkWorldPointPicker()
        worldPicker.Pick( *clickPosition[:2], 0, self._renderer )
        xyz = worldPicker.GetPickPosition()

        self._callback( xyz )

################################################################################
################################################################################
