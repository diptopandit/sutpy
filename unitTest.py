#!/usr/bin/python

from ut import Test
from optparse import OptionParser
import sys
import os

if __name__ == "__main__":
    parser = OptionParser()                                                                                                                                                                  
    parser.add_option("-f","--testfile",dest="testFile", help="Test case file with path.")
    parser.add_option("-c","--command",dest="command", help="Command to execute. Can be executable with path.")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False)
    parser.add_option("-t", "--testcases", dest="tcs", help="Comma separed list of test cases to run from the test file.", default="")
    parser.add_option("-x", "--exclude", dest="exs", help="Comma separed list of test cases to exclude from the test file. Takes precedence over cases to run.", default="")
    (options, args) = parser.parse_args()

    if not options.testFile:
        print "ERROR: Test case not specified\nUsage: "+os.path.basename(__file__)+" [-v][-t <test_cases_to_run>] [-x <test_cases_to_exclude>] -f <test_file> -c <command_to_run> <test_name>"
        sys.exit(0)

    if not options.command:
        print "ERROR: Command not specified\nUsage: "+os.path.basename(__file__)+" [-v] [-t <test_cases_to_run>] [-x <test_cases_to_exclude>] -f <test_file> -c <command_to_run> <test_name>"
        sys.exit(0)
    if not (args and args[0]):
        print "ERROR: Test name not specified\nUsage: "+os.path.basename(__file__)+" [-v] [-t <test_cases_to_run>] [-x <test_cases_to_exclude>] -f <test_file> -c <command_to_run> <test_name>"
        sys.exit(0)

    if not os.path.exists(options.testFile):
        print "ERROR: Could not find %s" %(options.testFile)
        sys.exit(0)

    if not os.path.exists(options.command):
        print "ERROR: Could not find %s" %(options.command)
        sys.exit(0)
    testCases=[]
    excludes=[]
    if options.tcs:
        testCases=map(int,options.tcs.split(','))
    if options.exs:
        excludes=map(int,options.exs.split(','))

    thisTest = Test(args[0],options.verbose)
    thisTest.command(options.command)
    thisTest.testFile(options.testFile)

    if thisTest.ready:
        thisTest.execute(testCases,excludes);
    else:
        print "Test is not redy to execute.\n"+thisTest.error

#end of main
