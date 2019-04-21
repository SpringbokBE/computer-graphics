from logging import getLogger

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

from Neuroviz.Gui import Gui

logger = getLogger( __name__ )

################################################################################
################################################################################

class App( QApplication ):

    def __init__( self, *args, **kwargs ):
        """
        Initialize the Neuroviz application.
        """
        logger.info( f"Creating {__class__.__name__}..." )

        super().__init__( *args, **kwargs )

        self.settings = QSettings( "Neuroviz.ini", QSettings.IniFormat )

        self._gui = Gui()

    ############################################################################

    def onAppQuit( self ):
        """
        """
        logger.debug( f"onAppQuit()" )

        # self.settings.sync()

################################################################################
################################################################################
