# -*- coding: utf-8 -*-

import unittest
import os

from os.path import join

from rl import completion
from rl import generator
from rl import readline
from rl import print_exc

from kmd import Kmd
from kmd.testing import JailSetup
from kmd.testing import reset

from kmd.completions.hostname import HostnameCompletion

TAB = '\t'

HOSTSFILE = """\
127.0.0.1   localhost
0.0.0.0     fred
0.0.0.0     barney
"""

HOSTSFILE2 = """\
127.0.0.1   localhost
0.0.0.0     freeport
0.0.0.0     barcelona
"""


class TestKmd(Kmd):

    def __init__(self, hostsfile=None):
        Kmd.__init__(self)
        self.hostsfile = hostsfile

    def preloop(self):
        Kmd.preloop(self)
        self.completehostname = HostnameCompletion(self.hostsfile)

    @print_exc
    @generator
    def complete(self, text):
        return self.completehostname(text)


class CompleterTests(JailSetup):

    def setUp(self):
        JailSetup.setUp(self)
        reset()
        self.mkhosts(HOSTSFILE)
        self.cmd = TestKmd(hostsfile=join(self.tempdir, 'hosts'))
        self.cmd.preloop()

    def mkhosts(self, content):
        f = open('hosts', 'wt')
        f.write(content)
        f.close()

    def complete(self, text):
        completion.line_buffer = text
        readline.complete_internal(TAB)
        return completion.line_buffer

    def test_simple(self):
        self.assertEqual(self.complete('bar'), '@barney ')

    def test_with_at(self):
        self.assertEqual(self.complete('@bar'), '@barney ')

    def test_at_is_delimiter(self):
        self.assertEqual(self.complete('foo@bar'), 'foo@barney ')

    def test_auto_refresh(self):
        self.assertEqual(self.complete('@bar'), '@barney ')
        self.mkhosts(HOSTSFILE2)
        self.assertEqual(self.complete('@bar'), '@barcelona ')

    def test_missing_file(self):
        os.remove('hosts')
        self.assertEqual(self.complete('bar'), 'bar')

