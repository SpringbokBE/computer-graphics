from logging import getLogger

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QComboBox, QGroupBox, QLabel,
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

        self._settings = QApplication.instance().settings

        super().__init__( *args, **kwargs )

        self._createLayout()

        dockWidget.setWidget( self )

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
