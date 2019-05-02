"""
File name:  App.py
Author:     Gerbrand De Laender
Date:       02/05/2019
Email:      gerbrand.delaender@ugent.be
Brief:      E016712, Project, Neuroviz
About:      Class that makes up the main application.
"""

################################################################################
################################################################################

from logging import getLogger

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

from Neuroviz.Gui import Gui

logger = getLogger( __name__ )

################################################################################
################################################################################

class App( QApplication ):

    """
    Main Neuroviz application.
    """

    ############################################################################

    def __init__( self, *args, **kwargs ):
        """
        Initialize the application.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, **kwargs )

        # Create a settings file.
        self.settings = QSettings( "Neuroviz.ini", QSettings.IniFormat )

        self._gui = Gui()

################################################################################
################################################################################
