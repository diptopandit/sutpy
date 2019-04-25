import time
import subprocess
#from OutputChannel import OutputChannel

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

try:
    from subprocess import STDOUT, check_output, CalledProcessError                                                                                                                          
except ImportError:  # pragma: no cover
    # python 2.6 doesn't include check_output
    # monkey patch it in!
    import subprocess
    STDOUT = subprocess.STDOUT

    def check_output(*popenargs, **kwargs):
        if 'stdout' in kwargs:  # pragma: no cover
            raise ValueError('stdout argument not allowed, '
                             'it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE,
                                   *popenargs, **kwargs)
        output, _ = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd,
                                                output=output)
        return output
    subprocess.check_output = check_output

    # overwrite CalledProcessError due to `output`
    # keyword not being available (in 2.6)
    class CalledProcessError(Exception):

        def __init__(self, returncode, cmd, output=None):
            self.returncode = returncode
            self.cmd = cmd
            self.output = output

        def __str__(self):
            return "Command '%s' returned non-zero exit status %d" % (
                self.cmd, self.returncode)
    subprocess.CalledProcessError = CalledProcessError



class TestCase:
    def __init__(self,cid,inp, exp):
        self.caseId = cid
        self.name = "TC#"+str(cid)
        self.inputStr = inp
        self.expected = exp
        self.result = False
        self.verbose = False
        self.elapsedTime = 0

    def execute(self,command):
        if self.verbose:
            print bcolors.HEADER+"Executing "+self.name+":"+bcolors.ENDC 
            print "input   : "+self.inputStr
            print "expected: "+self.expected
        try:
            start_time = time.time()
            self.actual = subprocess.check_output([command,self.inputStr]).strip()
            self.result = (self.expected == self.actual)
            self.elapsedTime = time.time() - start_time
            if self.verbose:
                color = bcolors.OKGREEN if self.result else bcolors.FAIL
                print "actual  : "+color+self.actual+bcolors.ENDC
                print "result  : "+color+str(self.result)+bcolors.ENDC+" Elapsed time: %.3f sec" % (self.elapsedTime)
        except Exception as e:
            print bcolors.WARNING+"ERROR::"+self.name+": "+str(e)+bcolors.ENDC
        if self.verbose:
            print "----------------------------------------------------------"

