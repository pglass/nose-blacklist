import logging
import os
import re
import subprocess
import six

TEST_DIR = os.path.join(os.path.dirname(__file__), 'sampletests')
LOG = logging.getLogger(__name__)


def indent(s):
    if isinstance(s, six.binary_type):
        s = s.decode()
    indent = "  "
    lines = s.split('\n')
    return indent + "\n{0}".format(indent).join(lines)


def rm_file(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def run_cmd(*args):
    cmd = list(args)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    LOG.info('executed `%s`', " ".join(cmd))
    LOG.info(' - exit code %s', p.returncode)
    LOG.info('------- stdout -------\n%s', indent(out))
    LOG.info('------- stderr -------\n%s', indent(err))
    return (out.decode('utf-8'), err.decode('utf-8'), p.returncode)


def run_regex(text, regex):
    LOG.debug("----- scanning the following text -----\n%s", indent(text))
    m = regex.search(text)
    if not m:
        LOG.debug("  regex '%s' failed to match", regex.pattern)
    else:
        groups = m.groups()
        LOG.debug("  parsed %s", groups)
        return groups


class ShortResult(object):

    def __init__(self, name, status):
        """
        :param name: the fully-qualified test name
        :param status: either 'ok', 'FAIL', or 'ERROR'
        """
        self.name = name
        self.status = status

    def __str__(self):
        return "%s: %s" % (self.status, self.name)

    def __repr__(self):
        return str(self)


class Results(object):
    """
    This class is used for parsing verbose nose test results. It's strict and
    assumes the particular set of test cases employed to test this plugin.

    WHAT WILL IT PARSE?

    YES: It will parse the regular output of the tests list.
        -- self.shortresults will contain these parsed lines

        test_set_to_mini (sampletests.v1.test_wumbo.WumboTest) ... ok
        test_set_to_wumbo (sampletests.v1.test_wumbo.WumboTest) ... ok
        ...

    YES: It will parse the "footer" of the nose output.
        -- self.n_tests is the number of tests run
        -- self.test_time is the test time found here
        -- self.test_status is the 'OK' or 'FAILED' result string
        -- self.n_failures is found from 'failures=2'
        -- self.n_skips is found from 'SKIP=2'
        -- self.n_errors is found from 'errors=2'


        ----------------------------------------------------------------------
        Ran 5 tests in 0.001s

        OK


        ----------------------------------------------------------------------
        Ran 1 test in 0.216s

        FAILED (errors=1)

    NO: It will not correctly parse docstrings descriptions that nose prints.

        check the mini thing... ok
        check the wumbo thing ... FAIL
        ...

    NO: It will not correctly parse nose's "dot" output.

        .....
        ----------------------------------------------------------------------
        Ran 5 tests in 0.000s

        OK

    NO: It will not parse exception output.

        ======================================================================
        FAIL: test_set_to_wumbo (sampletests.test_mini.MiniTest)
        ----------------------------------------------------------------------
        Traceback (most recent call last):
          File "/root/nose-blacklist/tests/sampletests/test_mini.py", ...
            self.assertFalse(True)
        AssertionError: True is not false
    """

    def __init__(self, raw):
        self.raw = raw
        self.shortresults = []

        # if any of these are still None after parsing, then parsing failed
        self.test_status = None
        self.test_time = None
        self.n_tests = None
        self.n_skips = None
        self.n_failures = None
        self.n_errors = None
        self.parse()

    def parse(self):
        LOG.debug('parsing results')

        parts = self.raw.strip().split('\n\n')
        if not parts:
            LOG.error("  nothing to parse!")
            return

        LOG.debug(parts)

        if len(parts) == 2:
            # there were no tests run
            self.parse_footer(parts[-2], parts[-1])
        else:
            # <testname> ... <status>
            self.parse_shortresults(parts[0])

            # --------------------------------------
            # Ran <N> tests in <X>s
            #
            # FAILED (failures=2)
            self.parse_footer(parts[-2], parts[-1])

    def parse_shortresults(self, text):
        regex_method = re.compile(r"(.+) \((.+)\) ... (\w+)")
        regex_function = re.compile(r"(.+) ... (\w+)")
        for line in text.split('\n'):
            # try to parse a normal result line
            groups = run_regex(line, regex_method)
            if groups is not None:
                method_name, class_name, status = groups
                test_name = "{0}.{1}".format(class_name, method_name)
                self.shortresults.append(ShortResult(test_name, status))
                continue

            groups = run_regex(line, regex_function)
            if groups is not None:
                self.shortresults.append(ShortResult(*groups))
                continue

            raise Exception("ERROR during test result parsing")

    def parse_footer(self, footer_start, footer_end):
        # parse the "Ran N tests in Xs" portion
        regex = re.compile(r"Ran (\d+) tests in (.+)s")
        groups = run_regex(footer_start, regex)
        self.n_tests = int(groups[0])
        self.test_time = float(groups[1])

        # parse the "FAILED (SKIP=1, failures=2)" portion
        #  - this may just be the string "OK"
        #  - this may just have "(failures=2)" with no skips
        self.test_status = str(footer_end.split(' ')[0].strip())
        self.n_skips = 0
        self.n_errors = 0
        self.n_failures = 0

        # parse the "(SKIP=1, failures=2)" portion
        regex = re.compile(r"(\w+=\d+)")
        groups = run_regex(footer_end, regex) or []
        for item in groups:
            parts = item.split('=')
            key = parts[0].lower()
            if 'failure' in key:
                self.n_failures = int(parts[1].strip())
            elif 'skip' in key:
                self.n_skips = int(parts[1].strip())
            elif 'error' in key:
                self.n_errors = int(parts[1].strip())
            else:
                LOG.error("Ignoring footer result element: %s", item)

    def __str__(self):
        data = self.__dict__
        del data['raw']
        return str(data)
