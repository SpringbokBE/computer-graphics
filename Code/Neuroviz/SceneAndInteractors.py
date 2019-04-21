from logging import getLogger

from PyQt5.QtCore import QObject, QTimer

from Neuroviz.Interactors import BasicWidget
from Neuroviz.Scenes import BasicScene

logger = getLogger( __name__ )

################################################################################
################################################################################

class BasicSceneAndInteractor( QObject ):

    ############################################################################

    def __init__( self, ui, *args, **kwargs ):
        """
        Initialize the scene and interactor (widget) and connect all signals
        to their respective slots.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, **kwargs )

        self._scene = BasicScene( ui.qvtkBasic.GetRenderWindow() )
        self._interactor = BasicWidget( ui.qdwDock )

        # Update the slider group ranges to match the scene.
        sliderRanges = self._scene.getBounds()
        self._interactor.sliderGroupCoronal.setRange( *sliderRanges[0:2] )
        self._interactor.sliderGroupSagittal.setRange( *sliderRanges[2:4] )
        self._interactor.sliderGroupTransverse.setRange( *sliderRanges[4:6] )

        # Update the image slices in the scene to match the slider groups.
        sliceValues = (self._interactor.sliderGroupCoronal.getValue(),
                       self._interactor.sliderGroupSagittal.getValue(),
                       self._interactor.sliderGroupTransverse.getValue())

        self._scene.updateSlices( sliceValues )

        # Connect all signals and their slots.
        self._interactor.sliderGroupCoronal.valueChanged.connect( self._onSliderGroupChanged )
        self._interactor.sliderGroupSagittal.valueChanged.connect( self._onSliderGroupChanged )
        self._interactor.sliderGroupTransverse.valueChanged.connect( self._onSliderGroupChanged )

        self._interactor.sliderGroupCoronal.toggled.connect( self._onSliderGroupToggled )
        self._interactor.sliderGroupSagittal.toggled.connect( self._onSliderGroupToggled )
        self._interactor.sliderGroupTransverse.toggled.connect( self._onSliderGroupToggled )

        # Add a timer for smoother interaction in the "Interactive" interaction
        # mode.
        self._sliderGroupTimer = QTimer()
        self._sliderGroupTimer.setSingleShot( True )
        self._sliderGroupTimer.timeout.connect( self._onSliderGroupTimeout )

    ############################################################################

    def _onSliderGroupChanged( self, _ ):
        """
        When any of the slider groups has changed.
        """
        logger.debug( f"_onSliderGroupChanged()" )

        if self._scene.getInteractionStyle == "Interactive":
            self._sliderGroupTimer.start( 200 )
        else:
            self._onSliderGroupTimeout()

    ############################################################################

    def _onSliderGroupToggled( self, _ ):
        """
        When any of the slider groups has been toggled.
        """
        logger.debug( f"_onSliderGroupToggled()" )

        sliceValues = (self._interactor.sliderGroupCoronal.getValue(),
                       self._interactor.sliderGroupSagittal.getValue(),
                       self._interactor.sliderGroupTransverse.getValue())

        self._scene.resetOpacity()
        self._scene.updateSlices( sliceValues )

    ############################################################################

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
