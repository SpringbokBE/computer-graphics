"""
File name:  Gui.py
Author:     Gerbrand De Laender
Date:       02/05/2019
Email:      gerbrand.delaender@ugent.be
Brief:      E016712, Project, Neuroviz
About:      Class that constitutes the main window to be shown in the Neuroviz
            application.
"""

################################################################################
################################################################################

from distutils.dep_util import newer
from importlib import import_module
from logging import getLogger
from os import getcwd
from os.path import basename, isfile, normpath, relpath, splitext

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import compileUi

from Neuroviz.SceneAndInteractors import (BasicSceneAndInteractor,
                                          DSASceneAndInteractor,
                                          EEGSceneAndInteractor)

logger = getLogger( __name__ )

################################################################################
################################################################################

class Gui( QMainWindow ):

    def __init__( self, *args, **kwargs ):
        """
        Initialize the GUI.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, **kwargs )

        self._settings = QApplication.instance().settings

        self._ui = self._recompileUi()
        self._ui.setupUi( self )

        self._scenesAndInteractors = [None for _ in range( 3 )]

        # Preloading all scenes will increase startup time, but provides a
        # allows for rapid tab changes.
        if self._settings.value( f"{__class__.__name__}/Preload", False, type = bool ):
            self._scenesAndInteractors[0] = BasicSceneAndInteractor( self._ui )
            self._scenesAndInteractors[1] = EEGSceneAndInteractor( self._ui )
            self._scenesAndInteractors[2] = DSASceneAndInteractor( self._ui )

        # Initialize the scene in the active tab.
        self._ui.tabWidget.currentChanged.connect( self._onTabWidgetCurrentChanged )
        self._onTabWidgetCurrentChanged( self._ui.tabWidget.currentIndex() )

        self.show()

    ############################################################################

    def _recompileUi( self ):
        """
        Generates a new Python file from a UI file created with e.g. Qt Designer
        when necessary. Imports it dynamically as well.
        """
        self._settings.beginGroup( f"{__class__.__name__}" )
        self._pyFileName = self._settings.value( "PyFileName", "/Neuroviz/Ui.py", type = str )
        self._pyFileName = normpath( getcwd() + self._sPyFileName )
        self._uiFileName = self._settings.value( "UiFileName", "/../UI/Neuroviz.ui", type = str )
        self._uiFileName = normpath( getcwd() + self._sUiFileName )
        self._uiClassName = self._settings.value( "UiClassName", "Ui_qmwMain", type = str )
        self._settings.endGroup()

        if not isfile( self._pyFileName ) or newer( self._uiFileName, self._pyFileName ):
            logger.info( f"Recompiling {self._uiFileName} -> {self._pyFileName}..." )
            with open( self._pyFileName, "w+" ) as file:
                compileUi( self._uiFileName, file )

        module = "Neuroviz." + splitext( basename( self._pyFileName ) )[0]
        return getattr( import_module( module ), self._uiClassName )()

    ############################################################################

    @pyqtSlot( int )
    def _onTabWidgetCurrentChanged( self, index ):
        """
        When a different visualization tab has been selected.
        """
        if index == 0:
            if not self._scenesAndInteractors[0]:
                self._scenesAndInteractors[0] = BasicSceneAndInteractor( self._ui )
            self._scenesAndInteractors[0].activate()
        elif index == 1:
            if not self._scenesAndInteractors[1]:
                self._scenesAndInteractors[1] = EEGSceneAndInteractor( self._ui )
            self._scenesAndInteractors[1].activate()
        elif index == 2:
            if not self._scenesAndInteractors[2]:
                self._scenesAndInteractors[2] = DSASceneAndInteractor( self._ui )
            self._scenesAndInteractors[2].activate()

################################################################################
################################################################################
