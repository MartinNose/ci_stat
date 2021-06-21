class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[37m'

bcolor = ['\033[31m', '\033[32m', '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[31m', '\033[34m', '\033[35m', '\033[37m']

def PURPLE(str):
     return '\033[95m' + str + '\033[0m'
def BLUE(str):
     return '\033[94m' + str + '\033[0m'
def CYAN(str):
     return '\033[96m' + str + '\033[0m'
def GREEN(str):
     return '\033[92m' + str + '\033[0m'
def YELLOW(str):
     return '\033[93m' + str + '\033[0m'
def RED(str):
     return '\033[91m' + str + '\033[0m'
def BOLD(str):
     return '\033[1m' + str + '\033[0m'
def UNDERLINE(str):
     return '\033[4m' + str + '\033[0m'
def WHITE(str):
     return '\033[37m' + str + '\033[0m'

class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr