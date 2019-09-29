import time
import subprocess
# from OutputChannel import OutputChannel


class BColors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'


try:
    from subprocess import STDOUT, check_output, CalledProcessError                                                                                                                          
except ImportError:  # pragma: no cover
    # python 2.6 doesn't include check_output
    # monkey patch it in!
    import subprocess
    STDOUT = subprocess.STDOUT

    def check_output(*p_open_args, **kwargs):
        if 'stdout' in kwargs:  # pragma: no cover
            raise ValueError('stdout argument not allowed, '
                             'it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE,
                                   *p_open_args, **kwargs)
        output, _ = process.communicate()
        return_code = process.poll()
        if return_code:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = p_open_args[0]
            raise subprocess.CalledProcessError(return_code, cmd,
                                                output=output)
        return output
    subprocess.check_output = check_output

    # overwrite CalledProcessError due to `output`
    # keyword not being available (in 2.6)
    class CalledProcessError(Exception):

        def __init__(self, return_code, cmd, output=None):
            self.m_return_code = return_code
            self.cmd = cmd
            self.output = output

        def __str__(self):
            return "Command '%s' returned non-zero exit status %d" % (
                self.cmd, self.m_return_code)
    subprocess.CalledProcessError = CalledProcessError


class TestCase:
    def __init__(self, cid, inp, exp):
        self.caseId = cid
        self.name = "TC#"+str(cid)
        self.inputStr = inp
        self.expected = exp
        self.result = False
        self.verbose = False
        self.elapsedTime = 0
        self.actual = 0

    def execute(self, command):
        if self.verbose:
            print(BColors.HEADER+"Executing " + self.name + ":" + BColors.END_C)
            print("input   : " + self.inputStr)
            print("expected: " + self.expected)
        try:
            start_time = time.time()
            self.actual = subprocess.check_output([command, self.inputStr]).strip()
            self.result = (self.expected == self.actual)
            self.elapsedTime = time.time() - start_time
            if self.verbose:
                color = BColors.OK_GREEN if self.result else BColors.FAIL
                print("actual  : "+color+self.actual+BColors.END_C)
                print("result  : "+color+str(self.result)+BColors.END_C+" Elapsed time: %.3f sec" % self.elapsedTime)
        except Exception as e:
            print(BColors.WARNING+"ERROR::"+self.name+": "+str(e)+BColors.END_C)
        if self.verbose:
            print("----------------------------------------------------------")

