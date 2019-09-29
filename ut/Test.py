from TestCase import TestCase


# from OutputChannel import OutputChannel


class BColors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'


class Test:
    def __init__(self, tid, verbose=False):
        self.testId = tid
        self.testCases = list()
        self.requestedCases = list()
        self.numberOfRequestedCases = 0
        self.result = True
        self.elapsedTime = 0
        self.totalCases = 0
        self.passedCases = 0
        self.maxTime = 0
        self.ready = False
        self.error = "ERROR::" + self.testId + ":No command specified.\nERROR::" + self.testId + ":No test case available.\n"
        self.verbose = verbose
        self.command_str = ""
        # self.outchannel = OutChannel()
        # self.out = self.outchannel.out

    def execute(self, req_cases=[], skip=[]):
        if self.command_str:
            if self.totalCases == 0:
                self.error = "ERROR::" + self.testId + ":No test case available.\n"
                return False

            if not req_cases:
                self.requestedCases = self.testCases
                self.numberOfRequestedCases = self.totalCases
            else:
                for case in req_cases:
                    self.requestedCases.append(self.testCases[case - 1])
                    self.numberOfRequestedCases = self.numberOfRequestedCases + 1
            if skip:
                for case in skip:
                    if self.testCases[case - 1] in self.requestedCases:
                        self.requestedCases.remove(self.testCases[case - 1])
                        self.numberOfRequestedCases = self.numberOfRequestedCases - 1

            # self.out(OutChannel.SPLOUT,"Running test : %s | %d test cases",self.testId,self.totalCases)
            # self.out(OutChannel.STDOUT,"==========================================================")
            print("Running test : %s | %d test cases" % (self.testId, self.numberOfRequestedCases))
            print("==========================================================")
            for testCase in self.requestedCases:
                testCase.execute(self.command_str)
                if not testCase.result:
                    self.result = False
                self.elapsedTime += testCase.elapsedTime
                self.maxTime = max(self.maxTime, testCase.elapsedTime)
                if testCase.result:
                    self.passedCases += 1
            print("Test " + self.testId + " Completed")
            print("==========================================================")
            print("Passed: %d, Failed %d (%d%% success)" % (self.passedCases,
                                                            (self.numberOfRequestedCases - self.passedCases),
                                                            ((self.passedCases * 100) / self.numberOfRequestedCases)))
            print("Test result: " +
                  (BColors.OK_GREEN + "PASSED" + BColors.END_C if self.result else BColors.FAIL + "FAILED" +
                   BColors.END_C) + ", Elapsed time: %.3f sec" % self.elapsedTime)
            print("Max time: %.3f sec, Average time: %.3f sec" % (
                self.maxTime, self.elapsedTime / self.numberOfRequestedCases))
            print("==========================================================")
            return self.result
        else:
            self.error = "ERROR::" + self.testId + ": No command specified.\n"
            return False

    def test_file(self, tc_file):
        test_case_id = 0
        try:
            with open(tc_file) as fp:
                for line in fp:
                    line = line.strip()
                    if (not line) or (line[0] is '#'):
                        continue
                    test_case_id = test_case_id + 1
                    exp = fp.next()
                    tc = TestCase(test_case_id, line.strip(), exp.strip())
                    tc.verbose = self.verbose
                    self.testCases.append(tc)
                    self.totalCases += 1
        except StopIteration:
            print("WARN::" + tc_file + ": Incomplete test case")
        if not self.command_str:
            self.ready = False
            self.error = "ERROR::" + self.testId + ":No command specified.\n"
        else:
            self.ready = True
        return len(self.testCases) == self.totalCases

    def command(self, cmd):
        self.command_str = cmd
        if self.totalCases != 0:
            self.ready = True
        else:
            self.error = "ERROR::" + self.testId + ":No test case available.\n"
            self.ready = False
