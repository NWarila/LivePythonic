import logging, logging.handlers
from datetime import datetime

class CustomLogger():
    nlog = logging.getLogger()

    def __new__(self) -> logging.Logger:
        self.addLoggingLevel(levelName='VERBOSE',levelNumber=15)
        self.addLoggingLevel(levelName='FATAL',levelNumber=15,exitAfter=True,force=True)
        self.addLoggingLevel(levelName='TRACE',levelNumber=9)

        self.nlog.setLevel(logging.WARNING)

        # create console handler with a higher log level
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(self.CustomFormatter())
        self.nlog.addHandler(consoleHandler)

        #If we should enable tracing funtions.
        self.nlogTrace = logging.TRACE >= self.nlog.getEffectiveLevel()
        return self.nlog

    def addLoggingLevel(levelName:str, levelNumber:int, methodName:str=None, exitAfter:bool=False,force:bool=False):
        """
        Comprehensively adds a new logging level to the `logging` module and the currently configured logging class.
        `levelName` becomes an attribute of the `logging` module with the value
        `levelNum`. `methodName` becomes a convenience method for both `logging`
        itself and the class returned by `logging.getLoggerClass()` (usually just
        `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
        used.
        To avoid accidental clobberings of existing attributes, this method will
        raise an `AttributeError` if the level name is already an attribute of the
        `logging` module or if the method name is already present
        Example
        -------
        >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
        >>> logging.getLogger(__name__).setLevel("TRACE")
        >>> logging.getLogger(__name__).trace('that worked')
        >>> logging.trace('so did this')
        >>> logging.TRACE
        5
        """
        if not methodName:
            methodName = levelName.lower()

        levelName = levelName.upper()

        if force != True:
            if hasattr(logging, levelName):
                print('\x1b[33;21m' + f"Warning: '{levelName}'' already defined in logging module" + '\033[0m')
                return
            if hasattr(logging, methodName):
                print('\x1b[33;21m' + f"Warning: '{methodName}'' already defined in logging module" + '\033[0m')
                return
            if hasattr(logging.getLoggerClass(), methodName):
                print('\x1b[33;21m' + f"Warning: {methodName} already defined in logger class" + '\033[0m')
                return

        # This method was inspired by the answers on Stack Overflow post
        # http://stackoverflow.com/q/2183233/2988730, especially
        # http://stackoverflow.com/a/13638084/2988730
        if exitAfter == True:
            def logForLevel(self, msg, *args, **kwargs):
                if self.isEnabledFor(levelNumber):
                    self._log(levelNumber, msg, args, **kwargs)
                exit()
        else:
            def logForLevel(self, msg, *args, **kwargs):
                if self.isEnabledFor(levelNumber):
                    self._log(levelNumber, msg, args, **kwargs)

        def logToRoot(msg, *args, **kwargs):
            logging.log(levelNumber, msg, args, **kwargs)

        logging.addLevelName(levelNumber, levelName)
        setattr(logging, levelName, levelNumber)
        setattr(logging.getLoggerClass(), methodName, logForLevel)
        setattr(logging, methodName, logToRoot)

    class CustomFormatter(logging.Formatter):
        """
        Logging Formatter to add colors and count warning / errors

        'Grey' = "\x1b[38;21m"; 'Yellow' = "\x1b[33;21m"; 'Red' = "\x1b[31;21m"; 'boldRed' = "\x1b[31;1m"; 'Reset' = "\x1b[0m"
        """

        def format(self, record):
            FORMATS = {
                logging.TRACE:    "\x1b[38;21m" + '%(asctime)s.%(msecs)03d ' + '%(lineno)04d:%(module)-10.10s ' + '%(threadName)-10.10s ' + '[%(levelname)-8s] ' + '%(message)s' + "\x1b[0m",
                logging.VERBOSE:  "\x1b[38;21m" + '%(asctime)s.%(msecs)03d ' + '%(lineno)04d:%(module)-10.10s ' + '%(threadName)-10.10s ' + '[%(levelname)-8s] ' + '%(message)s' + "\x1b[0m",
                logging.DEBUG:    "\x1b[38;21m" + '%(asctime)s.%(msecs)03d ' + '%(lineno)04d:%(module)-10.10s ' + '%(threadName)-10.10s ' + '[%(levelname)-8s] ' + '%(message)s' + "\x1b[0m",
                logging.INFO:     "\x1b[38;21m" + '%(asctime)s.%(msecs)03d ' + '%(lineno)04d:%(module)-10.10s ' + '%(threadName)-10.10s ' + '[%(levelname)-8s] ' + '%(message)s' + "\x1b[0m",
                logging.WARNING:  "\x1b[33;21m" + '%(asctime)s.%(msecs)03d ' + '%(lineno)04d:%(module)-10.10s ' + '%(threadName)-10.10s ' + '[%(levelname)-8s] ' + '%(message)s' + "\x1b[0m",
                logging.ERROR:    "\x1b[31;21m" + '%(asctime)s.%(msecs)03d ' + '%(lineno)04d:%(module)-10.10s ' + '%(threadName)-10.10s ' + '[%(levelname)-8s] ' + '%(message)s' + "\x1b[0m",
                logging.CRITICAL: "\x1b[31;1m"  + '%(asctime)s.%(msecs)03d ' + '%(lineno)04d:%(module)-10.10s ' + '%(threadName)-10.10s ' + '[%(levelname)-8s] ' + '%(message)s' + "\x1b[0m",
                logging.FATAL:    "\x1b[31;1m"  + '%(asctime)s.%(msecs)03d ' + '%(lineno)04d:%(module)-10.10s ' + '%(threadName)-10.10s ' + '[%(levelname)-8s] ' + '%(message)s' + "\x1b[0m"
            }
            #Establish new time format.
            convertedTimeStamp = datetime.fromtimestamp(record.created)
            logDateFmt = convertedTimeStamp.strftime("%Y-%m-%d %H:%M:%S")

            #Determine correct string format based on level.
            logFormat = FORMATS.get(record.levelno)

            #Set new format.
            formatter = logging.Formatter(fmt=logFormat,datefmt=logDateFmt)
            return formatter.format(record)
