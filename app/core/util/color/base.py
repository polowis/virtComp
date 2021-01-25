class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger(object):
    def error(self, message: str):
        """Display error messsage"""
        print('\033[31m' + message + '\033[0m')

    def info(self, message: str):
        """Display info message"""
        print('\033[92m' + message + '\033[0m')

    def warn(self, message: str):
        """Display warn message"""
        print('\033[93m' + message + '\033[0m')