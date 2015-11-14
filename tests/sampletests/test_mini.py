import unittest


def test_unbound_function():
    assert 1 == 2


class MiniTest(unittest.TestCase):

    def test_set_to_mini(self):
        self.assertTrue(True)

    def test_set_to_wumbo(self):
        self.assertFalse(True)

    def test_failure(self):
        self.assertFalse(True)
