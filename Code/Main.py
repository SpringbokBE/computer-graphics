from logging import (CRITICAL, DEBUG, FileHandler, Formatter, Logger,
                     StreamHandler, getLogger)
from sys import argv, exit

from PyQt5.QtCore import QSettings

from Neuroviz.App import App

logger = getLogger( __name__ )

################################################################################
################################################################################

def setupLogger():
    """
    Setup the logger(s) according to the user preferences.
    """
    logger.info( f"Setting up the loggers..." )

    settings = QSettings( "Neuroviz.ini", QSettings.IniFormat )

    if not settings.value( "Logging/Enabled", False, type = bool ): return

    rootLogger = getLogger()
    rootLogger.setLevel( DEBUG )

    if settings.value( "Logging/LogToFile", False, type = bool ):
        setupFileLogger( settings )

    if settings.value( "Logging/LogToConsole", False, type = bool ):
        setupConsoleLogger( settings )

    setupModulesToLog( settings )

    logger.info( "Logging started!" )

################################################################################

def setupFileLogger( settings ):
    """
    Setup the logging to a file conform to the given settings.
    """
    logger.info( f"Setting up a file logger..." )

    logToFileName = settings.value( "Logging/LogToFileName" )
    logToFileFormat = settings.value( "Logging/LogToFileFormat" )

    if logToFileName and logToFileFormat:
        fileHandler = FileHandler( logToFileName, mode = "a" )
        fileHandler.setLevel( DEBUG )
        fileHandler.setFormatter( Formatter( logToFileFormat ) )

        getLogger().addHandler( fileHandler )
    else:
        logger.error( "Could not find 'Logging/logToFileFormat' in "\
                      "Neuroviz.ini! Logging to file has been disabled!" )

################################################################################

def setupConsoleLogger( settings ):
    """
    Setup the logging to a console conform to the given settings.
    """
    logger.info( f"Setting up a console logger..." )

    logToConsoleFormat = settings.value( "Logging/LogToConsoleFormat" )

    if logToConsoleFormat:
        consoleHandler = StreamHandler()
        consoleHandler.setLevel( DEBUG )
        consoleHandler.setFormatter( Formatter( logToConsoleFormat ) )

        getLogger().addHandler( consoleHandler )
    else:
        logger.error( "Could not find 'Logging/logToConsoleFormat' in "\
                      "Neuroviz.ini! Logging to console has been disabled!")

################################################################################

def setupModulesToLog( settings ):
    """
    Setup the individual modules that need to be logged, conform to the given
    settings. Hides logging from other modules, except from level "Critical".
    """
    logger.info( f"Setting up the modules to be logged..." )

    modulesToLog = settings.value( "Logging/ModulesToLog" )
    loggingLevels = {"critical" : 50, "error" : 40, "warning" : 30,
                     "info" : 20, "debug" : 10, "notset" : 0 }

    for module in Logger.manager.loggerDict.keys():
        if module == "__main__": continue
        getLogger( module ).setLevel( CRITICAL )

    # Handle the empty and one-element list of modules.
    if not isinstance( modulesToLog , list ):
        if not modulesToLog: return
        modulesToLog = (modulesToLog,)

    for logItem in modulesToLog:
        module, level = (x.strip() for x in logItem.split( "->" ))
        getLogger( module ).setLevel( loggingLevels[level.lower()] )

################################################################################
################################################################################

if __name__ == "__main__":
    setupLogger()
    app = App( argv )
    exit( app.exec_() )
