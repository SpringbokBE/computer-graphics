from logging import getLogger

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox,
                             QDoubleSpinBox, QGridLayout, QGroupBox, QLabel,
                             QSizePolicy, QSlider, QSpacerItem, QVBoxLayout,
                             QWidget)

from Neuroviz.UiComponents import SliderGroup

logger = getLogger( __name__ )

################################################################################
################################################################################

class BasicWidget( QWidget ):

    ############################################################################

    def __init__( self, dockWidget ,*args, **kwargs ):
        """
        Creates a widget for the basic visualization scene. Adds it to the
        provided dock widget.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        self._dockWidget = dockWidget
        self._settings = QApplication.instance().settings

        super().__init__( *args, **kwargs )

        self._createLayout()

    ############################################################################

    def activate( self ):
        """
        Activate the interactor widget.
        """
        self._dockWidget.setWidget( self )

    ############################################################################

    def _createLayout( self ):
        """
        Creates the actual layout.
        """
        self._labelInteractionStyle = QLabel( "Interaction style", self )

        self.comboBoxInteractionStyle = QComboBox( self )
        self.comboBoxInteractionStyle.addItem( "Opacity" )
        self.comboBoxInteractionStyle.addItem( "Interactive" )
        self.comboBoxInteractionStyle.addItem( "Automatic" )

        self._labelActiveContour = QLabel( "Active contour", self )

        self.comboBoxActiveContour = QComboBox( self )

        self._labelOpacity = QLabel( "Opacity", self )

        self.sliderOpacity = QSlider( Qt.Horizontal, self )
        self.sliderOpacity.setMinimum( 0 )
        self.sliderOpacity.setMaximum( 99 )

        self.sliderGroupCoronal = SliderGroup( "CoronalCut", self )
        self.sliderGroupCoronal.setText( "Coronal cut" )
        self.sliderGroupSagittal = SliderGroup( "SagittalCut", self )
        self.sliderGroupSagittal.setText( "Sagittal cut" )
        self.sliderGroupTransverse = SliderGroup( "TransverseCut", self )
        self.sliderGroupTransverse.setText( "Transverse cut" )

        self._groupBoxSliders = QGroupBox( "Volumetric cuts", self )
        self._groupBoxSliders.setFlat( True )

        self._spacerItem = QSpacerItem( 20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding )

        groupBoxSlidersLayout = QVBoxLayout()
        groupBoxSlidersLayout.addWidget( self.sliderGroupCoronal )
        groupBoxSlidersLayout.addWidget( self.sliderGroupSagittal )
        groupBoxSlidersLayout.addWidget( self.sliderGroupTransverse )

        self._groupBoxSliders.setLayout( groupBoxSlidersLayout )

        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget( self._labelInteractionStyle )
        verticalLayout.addWidget( self.comboBoxInteractionStyle )
        verticalLayout.addWidget( self._labelActiveContour )
        verticalLayout.addWidget( self.comboBoxActiveContour )
        verticalLayout.addWidget( self._labelOpacity )
        verticalLayout.addWidget( self.sliderOpacity )
        verticalLayout.addWidget( self._groupBoxSliders )
        verticalLayout.addItem( self._spacerItem )
        self.setLayout( verticalLayout )

################################################################################
################################################################################

class EEGWidget( QWidget ):

    ############################################################################

    def __init__( self, dockWidget, *args, **kwargs ):
        """
        """
        logger.info( f"Creating {__class__.__name__}..." )

        self._dockWidget = dockWidget
        self._settings = QApplication.instance().settings

        super().__init__( *args, **kwargs )

        self._createLayout()

    ############################################################################

    def activate( self ):
        """
        Activate the interactor widget.
        """
        self._dockWidget.setWidget( self )

    ############################################################################

    def _createLayout( self ):
        """
        """
        self.sliderGroupAnimations = SliderGroup( "Animations", self )
        self.sliderGroupAnimations.setText( "Update interval" )

        self._groupBoxAnimations = QGroupBox( "Animations", self )
        self._groupBoxAnimations.setFlat( True )

        self._spacerItem = QSpacerItem( 20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding )

        groupBoxAnimationsLayout = QVBoxLayout()
        groupBoxAnimationsLayout.addWidget( self.sliderGroupAnimations )

        self._groupBoxAnimations.setLayout( groupBoxAnimationsLayout )

        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget( self._groupBoxAnimations )
        verticalLayout.addItem( self._spacerItem )
        self.setLayout( verticalLayout )

################################################################################
################################################################################

class DSAWidget( QWidget ):

    ############################################################################

    def __init__( self, dockWidget, *args, **kwargs ):
        """
        """
        logger.info( f"Creating {__class__.__name__}..." )

        self._dockWidget = dockWidget
        self._settings = QApplication.instance().settings

        super().__init__( *args, **kwargs )

        self._createLayout()

    ############################################################################

    def activate( self ):
        """
        Activate the interactor widget.
        """
        self._dockWidget.setWidget( self )

    ############################################################################

    def _createLayout( self ):
        """
        """
        self._labelDataSet = QLabel( "Dataset", self )
        self.comboBoxDataSet = QComboBox( self )

        self._labelHueMultiplier = QLabel( "Color range", self )
        self.spinBoxHueMultiplier = QDoubleSpinBox( self )
        self.spinBoxHueMultiplier.setRange( 0.5, 1.5 )
        self.spinBoxHueMultiplier.setDecimals( 2 )
        self.spinBoxHueMultiplier.setSingleStep( 0.01 )

        self._labelHueConstant = QLabel( "Color offset", self )
        self.spinBoxHueConstant = QDoubleSpinBox( self )
        self.spinBoxHueConstant.setRange( 0.0, 1.0 )
        self.spinBoxHueConstant.setDecimals( 2 )
        self.spinBoxHueConstant.setSingleStep( 0.01 )

        self._labelValueMultiplier = QLabel( "Detail", self )
        self.spinBoxValueMultiplier = QDoubleSpinBox( self )
        self.spinBoxValueMultiplier.setRange( 0.5, 10.0 )
        self.spinBoxValueMultiplier.setDecimals( 2 )
        self.spinBoxValueMultiplier.setSingleStep( 0.01 )

        self._spacerItem = QSpacerItem( 20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding )

        gridLayout = QGridLayout()
        gridLayout.addWidget( self._labelDataSet, 0, 0, 1, 2 )
        gridLayout.addWidget( self.comboBoxDataSet, 1, 0, 1, 2 )
        gridLayout.addWidget( self._labelHueMultiplier, 2, 0, 1, 1 )
        gridLayout.addWidget( self.spinBoxHueMultiplier, 2, 1, 1, 1 )
        gridLayout.addWidget( self._labelHueConstant, 3, 0, 1, 1 )
        gridLayout.addWidget( self.spinBoxHueConstant, 3, 1, 1, 1 )
        gridLayout.addWidget( self._labelValueMultiplier, 4, 0, 1, 1 )
        gridLayout.addWidget( self.spinBoxValueMultiplier, 4, 1, 1, 1 )
        gridLayout.addItem( self._spacerItem )
        self.setLayout( gridLayout )

################################################################################
################################################################################
