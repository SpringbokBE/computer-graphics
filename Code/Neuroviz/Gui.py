from distutils.dep_util import newer
from importlib import import_module
from logging import getLogger
from os import getcwd
from os.path import basename, isfile, normpath, relpath, splitext

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import compileUi

from Neuroviz.SceneAndInteractors import BasicSceneAndInteractor

logger = getLogger( __name__ )

################################################################################
################################################################################

class Gui( QMainWindow ):

    def __init__( self, *args, **kwargs ):
        """
        Initialize the Neuroviz GUI.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, **kwargs )

        self._settings = QApplication.instance().settings
        self._readSettings()

        self._ui = self._recompileUi()
        self._ui.setupUi( self )

        self._basicSceneInteractor = BasicSceneAndInteractor( self._ui )

        self.show()

        # # Add the VTK scenes to the GUI.
        # widgetName = settings.value( "BasicVisualization/WidgetName" )
        # if widgetName:
        #     renderWindow1 = getattr( self.ui, widgetName ).GetRenderWindow()
        #     self.scene1 = SceneBasicVisualization( renderWindow1, self.settings )
        # else:
        #     logger.critical( "Could not find 'BasicVisualization/WidgetName' "\
        #                      "in Neuroviz.ini!" )
        #     raise Exception()
        #
        # # Connect the signals to their slots.
        # self.scene1.planeWidgetXChanged.connect( self.onScene1PlaneWidgetXChange )
        # self.ui.nvSliderGroup1.valueChanged.connect( self.onNvSliderGroup1Change )

    ############################################################################

    def _readSettings( self ):
        """
        Reads the appropriate settings from the QApplication.
        """
        self._settings.beginGroup( "GUI" )
        self._sPyFileName = self._settings.value( "PyFileName", "Ui.py", type = str )
        self._sPyFileName = normpath( getcwd() + self._sPyFileName )
        self._sUiFileName = self._settings.value( "UiFileName", "Ui.ui", type = str )
        self._sUiFileName = normpath( getcwd() + self._sUiFileName )
        self._sUiClassName = self._settings.value( "UiClassName", "Ui_qmwMain", type = str )
        self._settings.endGroup()

    ############################################################################

    def _writeSettings( self ):
        """
        Writes the appropriate settings to the QApplication.
        """
        self._settings.beginGroup( "GUI" )
        if not self._settings.value( "SaveState", False, type = bool ): return
        self._settings.setValue( "PyFileName", "/" + relpath( self._sPyFileName, getcwd() ) )
        self._settings.setValue( "UiFileName", "/" + relpath( self._sUiFileName, getcwd() ) )
        self._settings.setValue( "UiClassName", self._sUiClassName )
        self._settings.endGroup()
        self._settings.sync()

    ############################################################################

    def _recompileUi( self ):
        """
        Generates a new Python file from a UI file created with e.g. Qt Designer
        when necessary. Imports it dynamically as well.
        """
        if not isfile( self._sPyFileName ) or newer( self._sUiFileName, self._sPyFileName ):
            logger.info( f"Recompiling {self._sUiFileName} -> {self._sPyFileName}..." )
            with open( self._sPyFileName, "w+" ) as file:
                compileUi( self._sUiFileName, file )

        module = "Neuroviz." + splitext( basename( self._sPyFileName ) )[0]
        return getattr( import_module( module ), self._sUiClassName )()

    ############################################################################

    def closeEvent( self, e ):
        """
        Save the settings before closing the window.
        """
        logger.debug( f"closeEvent()" )

        self._writeSettings()

################################################################################
################################################################################
