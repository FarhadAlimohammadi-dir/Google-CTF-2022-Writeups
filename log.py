from datetime import datetime
from  colors import *

# Log class for console when we are going to print results

class Log:

    @classmethod
    def info(self, text):
        print( bcolors.OKCYAN  + "[" + datetime.now().strftime("%H:%M:%S") + "] ["  + "INFO" +  "] " + text + bcolors.ENDC)

    @classmethod
    def warning(self, text):
        print( bcolors.WARNING  + "[" + datetime.now().strftime("%H:%M:%S") + "] ["  + "INFO" +  "] " + text + bcolors.ENDC)

    @classmethod
    def high(self, text):
        print( bcolors.FAIL  + "[" + datetime.now().strftime("%H:%M:%S") + "] ["  + "INFO" +  "] " + text + bcolors.ENDC)
