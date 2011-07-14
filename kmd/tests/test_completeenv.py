# -*- coding: utf-8 -*-

import unittest

from rl import completion
from rl import generator
from rl import readline
from rl import print_exc

from kmd import Kmd
from kmd.testing import reset

from kmd.completions.environment import EnvironmentCompletion

TAB = '\t'


class TestKmd(Kmd):

    def preloop(self):
        Kmd.preloop(self)
        self.completeenviron = EnvironmentCompletion()

    @print_exc
    @generator
    def complete(self, text):
        return self.completeenviron(text)


class CompleterTests(unittest.TestCase):

    def setUp(self):
        reset()
        self.cmd = TestKmd()
        self.cmd.preloop()

    def complete(self, text):
        completion.line_buffer = text
        readline.complete_internal(TAB)
        return completion.line_buffer

    def test_simple(self):
        self.assertEqual(self.complete('SHE'), '$SHELL ')

    def test_with_dollar(self):
        self.assertEqual(self.complete('$SHE'), '$SHELL ')

    def test_dollar_is_delimiter(self):
        self.assertEqual(self.complete('FOO$SHE'), 'FOO$SHELL ')

