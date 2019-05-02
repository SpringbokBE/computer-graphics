"""
File name:  SceneAndInteractors.py
Author:     Gerbrand De Laender
Date:       01/05/2019
Email:      gerbrand.delaender@ugent.be
Brief:      E016712, Project, Neuroviz
About:      Classes that group the behaviour of a scene (VTK render window,
            actors, ...) and an interactor (Qt widgets, interaction, ...). For
            each of the three tasks, a different class exists.
"""

################################################################################
################################################################################


from glob import glob
from logging import getLogger

from PyQt5.QtCore import QObject, QTimer, pyqtSlot
from PyQt5.QtWidgets import QApplication

from Neuroviz.Interactors import BasicWidget, DSAWidget, EEGWidget
from Neuroviz.Scenes import BasicScene, DSAScene, EEGScene

logger = getLogger( __name__ )

################################################################################
################################################################################

class BasicSceneAndInteractor( QObject ):

    """
    Groups the behaviour of the scene (VTK render window, actors, ...) and the
    interactor (Qt widgets, interaction, ...) for the "Basic Visualization"
    task.
    """

    ############################################################################

    def __init__( self, ui, *args, **kwargs ):
        """
        Initialize the scene and interactor and connect them.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, **kwargs )

        self._settings = QApplication.instance().settings

        self._scene = BasicScene( ui.qvtkBasic.GetRenderWindow() )
        self._interactor = BasicWidget( ui.qdwDock )

        self._updateInteractorFromScene()
        self._updateSceneFromInteractor()
        self._connectSignalsToSlots()

    ############################################################################

    def activate( self ):
        """
        Activate the (scene and) interactor.
        """
        self._interactor.activate()

    ############################################################################

    def _updateInteractorFromScene( self ):
        """
        Update the interactor with information from the scene.
        """
        # Update the interaction style combobox.
        index = self._interactor.comboBoxInteractionStyle.findText( self._scene.getInteractionStyle() )
        self._interactor.comboBoxInteractionStyle.setCurrentIndex( index )

        # Update the active contour combobox.
        self._interactor.comboBoxActiveContour.addItem( "None" )
        for name in self._scene.getContourNames():
            self._interactor.comboBoxActiveContour.addItem( name )

        index = self._interactor.comboBoxActiveContour.findText( self._scene.getActiveContourName() )
        self._interactor.comboBoxActiveContour.setCurrentIndex( index )

        # Update the slider group ranges.
        sliderRanges = self._scene.getBounds()
        self._interactor.sliderGroupCoronal.setRange( *sliderRanges[0:2] )
        self._interactor.sliderGroupSagittal.setRange( *sliderRanges[2:4] )
        self._interactor.sliderGroupTransverse.setRange( *sliderRanges[4:6] )

        # Update the opacity slider value.
        self._interactor.sliderOpacity.setEnabled( self._scene.getInteractionStyle() != "Automatic" )
        self._interactor.sliderOpacity.setValue( int( 100 * self._scene.getOpacity() ) )

    ############################################################################

    def _updateSceneFromInteractor( self ):
        """
        Update the scene with information from the interactor.
        """
        # Update the image slices.
        sliceValues = (self._interactor.sliderGroupCoronal.getValue(),
                       self._interactor.sliderGroupSagittal.getValue(),
                       self._interactor.sliderGroupTransverse.getValue())

        self._scene.updateSlices( sliceValues )

    ############################################################################

    def _connectSignalsToSlots( self ):
        """
        Connect the signals to their slots.
        """
        # Comboboxes.
        self._interactor.comboBoxInteractionStyle.activated.connect( self._onComboBoxInteractionStyleActivated )
        self._interactor.comboBoxActiveContour.activated.connect( self._onComboBoxActiveContourActivated )

        # Slider group changes.
        self._interactor.sliderGroupCoronal.valueChanged.connect( self._onSliderGroupChanged )
        self._interactor.sliderGroupSagittal.valueChanged.connect( self._onSliderGroupChanged )
        self._interactor.sliderGroupTransverse.valueChanged.connect( self._onSliderGroupChanged )

        # Slider group toggles.
        self._interactor.sliderGroupCoronal.toggled.connect( self._onSliderGroupToggled )
        self._interactor.sliderGroupSagittal.toggled.connect( self._onSliderGroupToggled )
        self._interactor.sliderGroupTransverse.toggled.connect( self._onSliderGroupToggled )

        # Opacity slider changes.
        self._interactor.sliderOpacity.valueChanged.connect( self._onSliderOpacityChanged )

        # Add a timer for smoother interaction in the "Automatic" and "Interactive" interaction mode.
        self._sliderGroupTimer = QTimer()
        self._sliderGroupTimer.setSingleShot( True )
        self._sliderGroupTimer.timeout.connect( self._onSliderGroupTimeout )

    ############################################################################

    @pyqtSlot( int )
    def _onComboBoxInteractionStyleActivated( self, index ):
        """
        When the interaction style combobox has been changed by the user.
        """
        logger.debug( f"_onComboBoxInteractionStyleActivated( {index} )" )

        style = self._interactor.comboBoxInteractionStyle.itemText( index )
        self._scene.setInteractionStyle( style )

        self._interactor.sliderOpacity.setEnabled( style != "Automatic" )

        self._settings.setValue( f"{type( self._scene ).__name__}/InteractionStyle", style )

    ############################################################################

    @pyqtSlot( int )
    def _onComboBoxActiveContourActivated( self, index ):
        """
        When the active contour combobox has been changed by the user.
        """
        logger.debug( f"_onComboBoxActiveContourActivated( {index} )" )

        contour = self._interactor.comboBoxActiveContour.itemText( index )
        self._scene.setActiveContour( contour )

        self._settings.setValue( f"{type( self._scene ).__name__}/ActiveContour", contour )

    ############################################################################

    @pyqtSlot( int )
    def _onSliderGroupChanged( self, _ ):
        """
        When any of the slider groups has changed.
        """
        logger.debug( f"_onSliderGroupChanged( {_} )" )

        if self._scene.getInteractionStyle == "Interactive":
            self._sliderGroupTimer.start( 200 )
        else:
            self._onSliderGroupTimeout()

    ############################################################################

    @pyqtSlot( bool )
    def _onSliderGroupToggled( self, _ ):
        """
        When any of the slider groups has been toggled.
        """
        logger.debug( f"_onSliderGroupToggled( {_})" )

        sliceValues = (self._interactor.sliderGroupCoronal.getValue(),
                       self._interactor.sliderGroupSagittal.getValue(),
                       self._interactor.sliderGroupTransverse.getValue())

        self._scene.resetOpacity()
        self._scene.updateSlices( sliceValues )

    ############################################################################

    @pyqtSlot( int )
    def _onSliderOpacityChanged( self, value ):
        """
        When the opacity slider has been changed.
        """
        logger.debug( f"_onSliderOpacityChanged( {value} )" )

        self._scene.setOpacity( value / 100 )

        self._settings.setValue( f"{type( self._scene ).__name__}/Opacity", value / 100 )

    ############################################################################

    @pyqtSlot()
    def _onSliderGroupTimeout( self ):
        """
        Update the slices in the scene.
        """
        logger.debug( f"_onSliderGroupTimeout()" )

        sliceValues = (self._interactor.sliderGroupCoronal.getValue(),
                       self._interactor.sliderGroupSagittal.getValue(),
                       self._interactor.sliderGroupTransverse.getValue())

        self._scene.updateSlices( sliceValues )

################################################################################
################################################################################

class EEGSceneAndInteractor( QObject ):

    """
    Groups the behaviour of the scene (VTK render window, actors, ...) and the
    interactor (Qt widgets, interaction, ...) for the "EEG Visualization"
    task.
    """

    ############################################################################

    def __init__( self, ui, *args, **kwargs ):
        """
        Initialize the scene and interactor and connect them.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, **kwargs )

        self._settings = QApplication.instance().settings

        self._scene = EEGScene( ui.qvtkEEG.GetRenderWindow(), ui.qvtkXY.GetRenderWindow() )
        self._interactor = EEGWidget( ui.qdwDock )

        self._updateSceneFromInteractor()
        self._connectSignalsToSlots()

    ############################################################################

    def activate( self ):
        """
        Activate the (scene and) interactor.
        """
        self._interactor.activate()

    ############################################################################

    def _updateSceneFromInteractor( self ):
        """
        Update the scene with information from the interactor.
        """
        if self._interactor.sliderGroupAnimations.getChecked():
            self._scene.setUpdateInterval( self._interactor.sliderGroupAnimations.getValue() )
        else:
            self._scene.setUpdateInterval( None )

    ############################################################################

    def _connectSignalsToSlots( self ):
        """
        Connect the signals to their slots.
        """
        # Slider group changes.
        self._interactor.sliderGroupAnimations.toggled.connect( self._onSliderGroupAnimationsToggled )
        self._interactor.sliderGroupAnimations.valueChanged.connect( self._onSliderGroupAnimationsChanged )

    ############################################################################

    @pyqtSlot( bool )
    def _onSliderGroupAnimationsToggled( self, state ):
        """
        When the animation slider group has been toggled.
        """
        logger.debug( f"_onSliderGroupAnimationsToggled( {state} )" )
        if state:
            self._scene.setUpdateInterval( self._interactor.sliderGroupAnimations.getValue() )
        else:
            self._scene.setUpdateInterval( None )

    ############################################################################

    @pyqtSlot( int )
    def _onSliderGroupAnimationsChanged( self, value ):
        """
        When the animation slider group has changed.
        """
        logger.debug( f"_onSliderGroupAnimationsChanged( {value} )" )

        self._scene.setUpdateInterval( value )

################################################################################
################################################################################

class DSASceneAndInteractor( QObject ):

    """
    Groups the behaviour of the scene (VTK render window, actors, ...) and the
    interactor (Qt widgets, interaction, ...) for the "DSA Visualization"
    task.
    """

    ############################################################################

    def __init__( self, ui, *args, **kwargs ):
        """
        Initialize the scene and interactor and connect them.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, **kwargs )

        self._settings = QApplication.instance().settings

        self._scene = DSAScene( ui.qvtkDSA.GetRenderWindow() )
        self._interactor = DSAWidget( ui.qdwDock )

        self._initializeInteractor()
        self._updateSceneFromInteractor()
        self._connectSignalsToSlots()

    ############################################################################

    def activate( self ):
        """
        Activate the (scene and) interactor.
        """
        self._interactor.activate()

    ############################################################################

    def _initializeInteractor( self ):
        """
        Initialize the interactor.
        """
        # Read in the datasets and update the combobox.
        dataSetName = self._settings.value( f"{__class__.__name__}/DataSetName", "", type = str )

        self._dataSetNames = sorted( glob( dataSetName ) )

        for dataSet in self._dataSetNames:
            self._interactor.comboBoxDataSet.addItem( dataSet.split( "/" )[-1] )

    ############################################################################

    def _updateSceneFromInteractor( self ):
        """
        Update the scene with information from the interactor.
        """
        hueMultiplier = self._settings.value( f"{__class__.__name__}/HueMultiplier", 0.85, type = float )
        hueConstant = self._settings.value( f"{__class__.__name__}/HueConstant", 0.1, type = float )
        valueMultiplier = self._settings.value( f"{__class__.__name__}/ValueMultiplier", 0.85, type = float )

        self._interactor.spinBoxHueMultiplier.setValue( hueMultiplier )
        self._interactor.spinBoxHueConstant.setValue( hueConstant )
        self._interactor.spinBoxValueMultiplier.setValue( valueMultiplier )

        self._scene.hueMultiplier = hueMultiplier
        self._scene.hueConstant = hueConstant
        self._scene.valueMultiplier = valueMultiplier

        self._scene.readDataSet( self._dataSetNames[self._interactor.comboBoxDataSet.currentIndex()] )
        self._scene.calculateRGBImage()
        self._scene.showRGBImage()

    ############################################################################

    def _connectSignalsToSlots( self ):
        """
        Connect the signals to their slots.
        """
        # Combobox changes.
        self._interactor.comboBoxDataSet.activated.connect( self._onComboBoxDataSetActivated )

        # Spinbox changes.
        self._interactor.spinBoxHueMultiplier.valueChanged.connect( self._onSpinBoxChanged )
        self._interactor.spinBoxHueConstant.valueChanged.connect( self._onSpinBoxChanged )
        self._interactor.spinBoxValueMultiplier.valueChanged.connect( self._onSpinBoxChanged )

        # Add a timer to the spinboxes for smoother interaction.
        self._spinBoxTimer = QTimer()
        self._spinBoxTimer.setSingleShot( True )
        self._spinBoxTimer.timeout.connect( self._onSpinBoxTimeout )

    ############################################################################

    @pyqtSlot( int )
    def _onComboBoxDataSetActivated( self, index ):
        """
        When the dataset combobox has been changed by the user.
        """
        logger.debug( f"_onComboBoxDataSetActivated( {index} )" )

        self._scene.readDataSet( self._dataSetNames[index] )
        self._scene.calculateRGBImage()
        self._scene.showRGBImage()

    ############################################################################

    @pyqtSlot( float )
    def _onSpinBoxChanged( self, _ ):
        """
        When any of the spinboxes has changed value.
        """
        logger.debug( f"_onSpinBoxChanged( {_} )" )

        self._spinBoxTimer.start( 1_000 )

    ###########################################################################

    @pyqtSlot()
    def _onSpinBoxTimeout( self ):
        """
        Update the multipliers/constant in the scene.
        """
        logger.debug( f"_onSpinBoxTimeout()" )

        self._scene.hueMultiplier = self._interactor.spinBoxHueMultiplier.value()
        self._scene.hueConstant = self._interactor.spinBoxHueConstant.value()
        self._scene.valueMultiplier = self._interactor.spinBoxValueMultiplier.value()

        self._scene.calculateRGBImage()
        self._scene.showRGBImage()

        self._settings.setValue( f"{__class__.__name__}/HueMultiplier", self._scene.hueMultiplier )
        self._settings.setValue( f"{__class__.__name__}/HueConstant", self._scene.hueConstant )
        self._settings.setValue( f"{__class__.__name__}/ValueMultiplier", self._scene.valueMultiplier )

################################################################################
################################################################################
