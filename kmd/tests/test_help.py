import unittest

from StringIO import StringIO
from kmd import Kmd


class TestKmd(Kmd):

    def do_echo(self, args):
        """Usage: echo $<variablename>"""

    def do_cat(self, args):
        pass

    def help_cat(self, topic):
        self.stdout.write('Usage: cat <filename>\n')

    def do_chdir(self, args):
        pass

    def help_chdir(self):
        self.stdout.write('Usage: chdir <dirname>\n')


class HelpTests(unittest.TestCase):

    def test_docstring(self):
        shell = TestKmd(stdout=StringIO())
        shell.do_help('echo')
        self.assertEqual(shell.stdout.getvalue(), 'Usage: echo $<variablename>\n')

    def test_helpfunc_w_topic_parm(self):
        shell = TestKmd(stdout=StringIO())
        shell.do_help('cat')
        self.assertEqual(shell.stdout.getvalue(), 'Usage: cat <filename>\n')

    def test_helpfunc_wo_topic_parm(self):
        shell = TestKmd(stdout=StringIO())
        shell.do_help('chdir')
        self.assertEqual(shell.stdout.getvalue(), 'Usage: chdir <dirname>\n')


class StderrTests(unittest.TestCase):

    def test_helpdefault_via_do_help(self):
        shell = TestKmd(stderr=StringIO())
        shell.do_help('foo')
        self.assertEqual(shell.stderr.getvalue(), '*** No help on foo\n')

    def test_default(self):
        shell = TestKmd(stderr=StringIO())
        shell.default('foo')
        self.assertEqual(shell.stderr.getvalue(), '*** Unknown syntax: foo\n')

    def test_default_via_onecmd(self):
        shell = TestKmd(stderr=StringIO())
        shell.onecmd('foo')
        self.assertEqual(shell.stderr.getvalue(), '*** Unknown syntax: foo\n')

