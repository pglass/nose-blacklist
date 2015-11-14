import unittest

from utils import run_cmd, Results, TEST_DIR


class TestResultsParsing(unittest.TestCase):

    def test_collect_only(self):
        out, err, ret = run_cmd('nosetests', '--collect-only', '-v', TEST_DIR)
        results = Results(err)
        self.assertEqual(results.test_status, 'OK')
        self.assertEqual(results.n_skips, 0)
        self.assertEqual(results.n_failures, 0)
        self.assertEqual(results.n_errors, 0)
        self.assertEqual(results.n_tests, 6)
        self.assertGreater(results.test_time, 0)

        short_results_status = set([r.status for r in results.shortresults])
        short_results_names = set([r.name for r in results.shortresults])
        self.assertEqual(short_results_status, set(['ok']))

        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_mini",
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.MiniTest.test_failure",
            "sampletests.test_mini.MiniTest.test_set_to_mini",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
            "sampletests.test_mini.test_unbound_function",
        ])
        self.assertEqual(short_results_names, expected_test_list)

    def test_nose_output_with_failures(self):
        out, err, ret = run_cmd('nosetests', '-v', TEST_DIR)
        results = Results(err)
        self.assertEqual(results.n_skips, 0)
        self.assertEqual(results.n_failures, 3)
        self.assertEqual(results.n_errors, 0)
        self.assertEqual(results.n_tests, 6)

        short_results_status = [r.status for r in results.shortresults]
        self.assertEqual(short_results_status.count('FAIL'), 3)
        self.assertEqual(short_results_status.count('ok'), 3)

        short_results_names = set([r.name for r in results.shortresults])
        expected_test_list = set([
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_mini",
            "sampletests.v1.test_wumbo.WumboTest.test_set_to_wumbo",
            "sampletests.test_mini.MiniTest.test_failure",
            "sampletests.test_mini.MiniTest.test_set_to_mini",
            "sampletests.test_mini.MiniTest.test_set_to_wumbo",
            "sampletests.test_mini.test_unbound_function",
        ])
        self.assertEqual(short_results_names, expected_test_list)
