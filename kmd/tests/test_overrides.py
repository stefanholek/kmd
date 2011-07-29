import unittest

from kmd import Kmd


class OverrideTests(unittest.TestCase):

    def test_completekey(self):
        shell = Kmd(completekey='X')
        self.assertEqual(shell.completekey, 'X')

    def test_stdin(self):
        shell = Kmd(stdin='X')
        self.assertEqual(shell.stdin, 'X')

    def test_stdout(self):
        shell = Kmd(stdout='X')
        self.assertEqual(shell.stdout, 'X')

    def test_all(self):
        shell = Kmd('X', 'Y', 'Z')
        self.assertEqual(shell.completekey, 'X')
        self.assertEqual(shell.stdin, 'Y')
        self.assertEqual(shell.stdout, 'Z')
