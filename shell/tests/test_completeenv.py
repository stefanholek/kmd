# -*- coding: utf-8 -*-

import unittest

from rl import completion
from rl import generator
from rl import readline
from rl import print_exc

from shell import Shell
from shell.testing import reset

from shell.completions.environment import EnvironmentCompletion

TAB = '\t'


class TestShell(Shell):

    def preloop(self):
        Shell.preloop(self)
        self.completeenviron = EnvironmentCompletion()

    @print_exc
    @generator
    def complete(self, text):
        return self.completeenviron(text)


class CompleterTests(unittest.TestCase):

    def setUp(self):
        reset()
        self.cmd = TestShell()
        self.cmd.preloop()

    def complete(self, text):
        completion.line_buffer = text
        readline.complete_internal(TAB)
        return completion.line_buffer

    def test_simple(self):
        self.assertEqual(self.complete('SHE'), '$SHELL ')

    def test_with_dollar(self):
        self.assertEqual(self.complete('$SHE'), '$SHELL ')

