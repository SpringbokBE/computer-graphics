"""
File name:  UiComponents.py
Author:     Gerbrand De Laender
Date:       01/05/2019
Email:      gerbrand.delaender@ugent.be
Brief:      E016712, Project, Neuroviz
About:      Classes that contain custom widgets (components) for the Neuroviz
            graphical user interface.
"""

################################################################################
################################################################################

from logging import getLogger

from PyQt5.QtCore import QSettings, Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QSlider,
                             QSpinBox, QWidget)

logger = getLogger( __name__ )

################################################################################
################################################################################

class SliderGroup( QWidget ):

    """
    Groups the behaviour of a QSlider, QSpinBox and a QCheckBox.
    Updates the spinbox whenever the slider changes (and vice versa), and
    enables/disables the group based on the state of the checkbox.
    """

    ############################################################################

    valueChanged = pyqtSignal( int )
    toggled = pyqtSignal( bool )

    ############################################################################

    def __init__( self, name, *args, **kwargs ):
        """
        Initialize the widget.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, *kwargs )

        self.setObjectName( name )
        self._settings = QApplication.instance().settings

        self._createLayout()
        self._applyInitialSettings()

        self._slider.valueChanged.connect( self._onSliderValueChanged )
        self._spinBox.valueChanged.connect( self._onSpinBoxValueChanged )
        self._checkBox.toggled.connect( self._onCheckBoxToggled )

        # Only write to the settings after timeout for smoother interaction.
        self._sliderTimer = QTimer()
        self._sliderTimer.setSingleShot( True )
        self._sliderTimer.timeout.connect( lambda : \
            self._settings.setValue(f"{self.objectName()}/Value", self.getValue() ) )

    ############################################################################

    def getEnabled( self  ):
        """
        Get the state of the whole widget (enabled/disabled).
        """
        return self.isEnabled()

    ############################################################################

    def setEnabled( self, isEnabled ):
        """
        Set the state of the whole widget (enabled/disabled).
        """
        super().setEnabled( isEnabled )

    ############################################################################

    def getChecked( self ):
        """
        Get the checkbox state (checked/unchecked).
        """
        return self._checkBox.isChecked()

    ############################################################################

    def setChecked( self, checked ):
        """
        Set the checkbox state (checked/unchecked).
        """
        self._checkBox.setChecked( checked )

        self._settings.setValue( f"{self.objectName()}/Checked", checked )

    ############################################################################

    def getValue( self ):
        """
        Get the current value.
        """
        if self._checkBox.isChecked(): return self._slider.value()
        return None

    ############################################################################

    def setValue( self, value ):
        """
        Set the current value.
        """
        self._slider.setValue( value )

        self._settings.setValue( f"{self.objectName()}/Value", value )

    ############################################################################

    def getText( self ):
        """
        Get the checkbox text.
        """
        return self._checkBox.text()

    ############################################################################

    def setText( self, text ):
        """
        Set the checkbox text.
        """
        self._checkBox.setText( text )

        self._settings.setValue( f"{self.objectName()}/Text", text )

    ############################################################################

    def getRange( self ):
        """
        Get the current range.
        """
        return self._slider.minimum(), self._slider.maximum()

    ############################################################################

    def setRange( self, minimum, maximum ):
        """
        Set the current range.
        """
        self._slider.setMinimum( minimum )
        self._slider.setMaximum( maximum )
        self._spinBox.setMinimum( minimum )
        self._spinBox.setMaximum( maximum )

        self._settings.setValue( f"{self.objectName()}/Min", minimum )
        self._settings.setValue( f"{self.objectName()}/Max", maximum )

    ############################################################################

    def _createLayout( self ):
        """
        Creates the actual widget layout.
        """
        self._slider = QSlider( Qt.Horizontal, self )
        self._spinBox = QSpinBox( self )
        self._checkBox = QCheckBox( self )

        gridLayout = QGridLayout( self )
        gridLayout.addWidget( self._slider, 0, 0, 1, 2 )
        gridLayout.addWidget( self._spinBox, 1, 1, 1, 1 )
        gridLayout.addWidget( self._checkBox, 1, 0, 1, 1 )

        self.setLayout( gridLayout )

    ############################################################################

    def _applyInitialSettings( self ):
        """
        Applies the initial settings.
        """
        self._settings.beginGroup( self.objectName() )
        checked = self._settings.value( "Checked", False, type = bool )
        text = self._settings.value( "Text", self.objectName(), type = str )
        value = self._settings.value( "Value", 0, type = int )
        min = self._settings.value( "Min", 0, type = int )
        max = self._settings.value( "Max", 100, type = int )
        self._settings.endGroup()

        self._slider.setEnabled( checked )
        self._slider.setMinimum( min )
        self._slider.setMaximum( max )
        self._slider.setValue( value )

        self._spinBox.setEnabled( checked )
        self._spinBox.setMinimum( min )
        self._spinBox.setMaximum( max )
        self._spinBox.setValue( value )

        self._checkBox.setChecked( checked )
        self._checkBox.setText( text )

    ############################################################################

    @pyqtSlot( bool )
    def _onCheckBoxToggled( self, isChecked ):
        """
        Enable or disable the slider/spinbox depending on the checkbox state.
        """
        logger.debug( f"_onCheckBoxToggled( {isChecked} )" )

        self._slider.setEnabled( isChecked )
        self._spinBox.setEnabled( isChecked )
        self.toggled.emit( isChecked )

        self._settings.setValue( f"{self.objectName()}/Checked", isChecked )

    ############################################################################

    @pyqtSlot( int )
    def _onSliderValueChanged( self, value ):
        """
        Update the spinbox when the sliders value has changed.
        """
        logger.debug( f"_onSliderValueChanged( {value} )" )

        self._spinBox.blockSignals( True )
        self._spinBox.setValue( value )
        self._spinBox.blockSignals( False )
        self.valueChanged.emit( value )

        self._sliderTimer.start( 500 )

    ############################################################################

    @pyqtSlot( int )
    def _onSpinBoxValueChanged( self, value ):
        """
        Update the slider when the spinbox' value has changed.
        """
        logger.debug( f"_onSpinboxValueChanged( {value} )" )

        self._slider.setValue( value )

################################################################################
################################################################################
