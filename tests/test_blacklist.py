import os
import unittest
import uuid

from utils import run_cmd, Results, TEST_DIR, rm_file


def run_nose(*args):
    """Run nose against our sample dir of tests."""
    cmd = ['nosetests'] + list(args) + ['-v', TEST_DIR]
    _, err, _ = run_cmd(*cmd)
    return Results(err)


class TestBlacklist(unittest.TestCase):

    def test_blacklist_by_method_name(self):
        results = run_nose('--with-blacklist', '--blacklist=test_set_to_wumbo')
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_mini",
            "sampletests.test_mini.MiniTest.test_failure",
            "sampletests.test_mini.MiniTest.test_set_to_mini",
            "sampletests.test_mini.test_unbound_function",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_multiple_blacklist_arguments(self):
        results = run_nose(
            '--with-blacklist',
            '--blacklist=test_failure',
            '--blacklist=test_set_to_mini',
            '--blacklist=test_unbound_function',
        )
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_blacklist_by_class(self):
        results = run_nose('--with-blacklist', '--blacklist=MiniTest')
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_mini",
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.test_unbound_function",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_blacklist_by_qualified_class(self):
        results = run_nose(
            '--with-blacklist', '--blacklist=test_mini.MiniTest',
        )
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_mini",
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.test_unbound_function",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_blacklist_by_qualified_function(self):
        results = run_nose(
            '--with-blacklist', '--blacklist=MiniTest.test_set_to_mini',
        )
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_mini",
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.MiniTest.test_failure",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
            "sampletests.test_mini.test_unbound_function",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_blacklist_by_module(self):
        results = run_nose(
            '--with-blacklist', '--blacklist=test_mini'
        )
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_mini",
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_blacklist_by_qualified_module(self):
        results = run_nose(
            '--with-blacklist', '--blacklist=v1.test_wumbo'
        )
        expected_test_list = set([
            "sampletests.test_mini.MiniTest.test_failure",
            "sampletests.test_mini.MiniTest.test_set_to_mini",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
            "sampletests.test_mini.test_unbound_function",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_blacklist_by_fullly_qualified_names(self):
        results = run_nose(
            '--with-blacklist',
            '--blacklist=sampletests.v1.test_wumbo.WumboTest.test_set_to_mini',
            '--blacklist=sampletests.test_mini.test_unbound_function',
        )
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.MiniTest.test_failure",
            "sampletests.test_mini.MiniTest.test_set_to_mini",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_everything_gets_blacklisted(self):
        results = run_nose(
            '--with-blacklist',
            '--blacklist=sampletests',
        )
        expected_test_list = set([])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)


class TestBlacklistFile(unittest.TestCase):

    def setUp(self):
        self.uuid = str(uuid.uuid4())
        self.blacklist_filepath = os.path.join(
            TEST_DIR, 'black-%s.txt' % self.uuid
        )

    def tearDown(self):
        rm_file(self.blacklist_filepath)

    def write_blacklist_file(self, *lines):
        with open(self.blacklist_filepath, 'w') as f:
            f.write("\n".join(lines))

    def test_empty_blacklist_file(self):
        self.write_blacklist_file("")
        results = run_nose(
            '--with-blacklist',
            '--blacklist-file=%s' % self.blacklist_filepath,
        )
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_mini",
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.MiniTest.test_failure",
            "sampletests.test_mini.MiniTest.test_set_to_mini",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
            "sampletests.test_mini.test_unbound_function",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_blacklist_file_only_comments(self):
        self.write_blacklist_file(
            "# wumbo",
            "# mini",
        )
        results = run_nose(
            '--with-blacklist',
            '--blacklist-file=%s' % self.blacklist_filepath,
        )
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_mini",
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.MiniTest.test_failure",
            "sampletests.test_mini.MiniTest.test_set_to_mini",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
            "sampletests.test_mini.test_unbound_function",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_blacklist_file(self):
        self.write_blacklist_file(
            "test_unbound",
            "# wumbo",
            "MiniTest.test_failure",
        )
        results = run_nose(
            '--with-blacklist',
            '--blacklist-file=%s' % self.blacklist_filepath,
        )
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_mini",
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.MiniTest.test_set_to_mini",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_blacklist_file_with_blacklist_arguments(self):
        self.write_blacklist_file("test_unbound")
        results = run_nose(
            '--with-blacklist',
            '--blacklist-file=%s' % self.blacklist_filepath,
            '--blacklist=test_set_to_mini',
        )
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.MiniTest.test_failure",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)

    def test_blacklist_file_with_blacklist_arguments_and_processes(self):
        self.write_blacklist_file("test_unbound")
        results = run_nose(
            '--with-blacklist',
            '--processes=2',
            '--blacklist-file=%s' % self.blacklist_filepath,
            '--blacklist=test_set_to_mini',
        )
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.MiniTest.test_failure",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
        ])
        testnames = set([r.name for r in results.shortresults])
        self.assertEqual(expected_test_list, testnames)
