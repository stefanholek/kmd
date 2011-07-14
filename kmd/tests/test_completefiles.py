# -*- coding: utf-8 -*-

import unittest

from rl import completer
from rl import completion
from rl import generator
from rl import readline
from rl import print_exc

from kmd import Kmd
from kmd.testing import JailSetup
from kmd.testing import reset

from kmd.completions.filename import FilenameCompletion

TAB = '\t'


class TestKmd(Kmd):

    def __init__(self, quote_char='\\'):
        Kmd.__init__(self)
        self.quote_char = quote_char

    def preloop(self):
        Kmd.preloop(self)
        self.completefilename = FilenameCompletion(self.quote_char)

    @print_exc
    @generator
    def complete(self, text):
        return self.completefilename(text)


class InitQuoteCharactersTests(unittest.TestCase):

    def setUp(self):
        reset()

    def test_double_quote(self):
        self.cmd = TestKmd(quote_char='"')
        self.cmd.preloop()
        self.assertEqual(completer.quote_characters, '"\'')

    def test_single_quote(self):
        self.cmd = TestKmd(quote_char="'")
        self.cmd.preloop()
        self.assertEqual(completer.quote_characters, '\'"')

    def test_backslash(self):
        self.cmd = TestKmd(quote_char='\\')
        self.cmd.preloop()
        self.assertEqual(completer.quote_characters, '"\'')

    def test_reconfigure(self):
        self.cmd = TestKmd(quote_char='"')
        self.cmd.preloop()
        self.assertEqual(completer.quote_characters, '"\'')
        self.cmd = TestKmd(quote_char="'")
        self.cmd.preloop()
        self.assertEqual(completer.quote_characters, '\'"')
        self.cmd = TestKmd(quote_char='"')
        self.cmd.preloop()
        self.assertEqual(completer.quote_characters, '"\'')
        self.cmd = TestKmd(quote_char="'")
        self.cmd.preloop()
        self.assertEqual(completer.quote_characters, '\'"')
        self.cmd = TestKmd(quote_char='\\')
        self.cmd.preloop()
        self.assertEqual(completer.quote_characters, '"\'')

    def test_invalid(self):
        self.cmd = TestKmd(quote_char='A')
        self.assertRaises(ValueError, self.cmd.preloop)


class CompleterTests(JailSetup):

    def setUp(self):
        JailSetup.setUp(self)
        reset()
        self.cmd = TestKmd(quote_char='"')
        self.cmd.preloop()
        self.mkfiles()

    def complete(self, text):
        completion.line_buffer = text
        readline.complete_internal(TAB)
        return completion.line_buffer

    def mkfiles(self):
        self.mkfile("Al'Hambra.txt")
        self.mkfile('Foo\\"Peng\\".txt')
        self.mkfile('Foo\\Bar.txt')
        self.mkfile('Foo\\Baz.txt')
        self.mkfile('Hello World.txt')
        self.mkfile('Lee "Scratch" Perry.txt')
        self.mkfile('Mädchen.txt')
        self.mkfile('Simple.txt')
        self.mkfile('Tilde.tx~')
        self.mkfile('~StartsWithTilde.txt')

    def test_simple(self):
        self.assertEqual(self.complete('Simple'),
                                       'Simple.txt ')

    def test_hello(self):
        self.assertEqual(self.complete('Hell'),
                                       '"Hello World.txt" ')

    def test_hello_double_quote(self):
        self.assertEqual(self.complete('"Hello '),
                                       '"Hello World.txt" ')

    def test_hello_single_quote(self):
        self.assertEqual(self.complete("'Hello "),
                                       "'Hello World.txt' ")

    def test_lee(self):
        self.assertEqual(self.complete('Lee'),
                                       '"Lee \\"Scratch\\" Perry.txt" ')

    def test_lee_double_quote(self):
        self.assertEqual(self.complete('"Lee \\"'),
                                       '"Lee \\"Scratch\\" Perry.txt" ')

    def test_lee_single_quote(self):
        self.assertEqual(self.complete(''''Lee "'''),
                                       ''''Lee "Scratch" Perry.txt' ''')

    def test_foobar(self):
        self.assertEqual(self.complete('Foo'),
                                       'Foo\\\\')

    def test_foobar_double_quote(self):
        self.assertEqual(self.complete('"Foo'),
                                       '"Foo\\\\')

    def test_foobar_single_quote(self):
        self.assertEqual(self.complete("'Foo"),
                                       "'Foo\\")

    def test_alhambra(self):
        self.assertEqual(self.complete('Al'),
                                     '''"Al'Hambra.txt" ''')

    def test_alhambra_double_quote(self):
        self.assertEqual(self.complete('"Al'),
                                     '''"Al'Hambra.txt" ''')

    def test_alhambra_single_quote(self):
        self.assertEqual(self.complete("'Al"),
                                       "'Al'\\''Hambra.txt' ")

    def test_foopeng(self):
        self.assertEqual(self.complete('Foo\\\\\\"'),
                                       'Foo\\\\\\"Peng\\\\\\".txt ')

    def test_foopeng_double_quote(self):
        self.assertEqual(self.complete('"Foo\\\\\\"'),
                                       '"Foo\\\\\\"Peng\\\\\\".txt" ')

    def test_foopeng_single_quote(self):
        self.assertEqual(self.complete(''''Foo\\"'''),
                                       ''''Foo\\"Peng\\".txt' ''')

    def test_tilde(self):
        self.assertEqual(self.complete('Tilde'),
                                       'Tilde.tx~ ')

    def test_starts_with_tilde(self):
        self.assertEqual(self.complete('~Starts'),
                                       '~StartsWithTilde.txt ')

    def test_returned_umlaut(self):
        self.assertEqual(self.complete('M'),
                                       'Mädchen.txt ')

    def test_typed_umlaut(self):
        self.assertEqual(self.complete('Mä'),
                                       'Mädchen.txt ')


class CharIsQuotedTests(unittest.TestCase):

    def setUp(self):
        reset()
        self.cmd = TestKmd(quote_char='"')
        self.cmd.preloop()
        self.is_quoted = self.cmd.completefilename.char_is_quoted

    def test_backslash_quoted_double_quote(self):
        self.assertEqual(self.is_quoted('\\"', 1), True)
        self.assertEqual(self.is_quoted('\\"', 0), False)
        self.assertEqual(self.is_quoted('\\ \\"', 3), True)
        self.assertEqual(self.is_quoted('\\ \\"', 2), False)
        self.assertEqual(self.is_quoted('\\ \\"', 1), True)
        self.assertEqual(self.is_quoted('\\ \\"', 0), False)

    def test_backslash_quoted_single_quote(self):
        self.assertEqual(self.is_quoted("\\'", 1), True)
        self.assertEqual(self.is_quoted("\\'", 0), False)

    def test_quoted_by_other_quote_character(self):
        self.assertEqual(self.is_quoted("""'foo "bar"'""", 0), False)
        self.assertEqual(self.is_quoted("""'foo "bar"'""", 5), True)
        self.assertEqual(self.is_quoted("""'foo "bar"'""", 9), True)
        self.assertEqual(self.is_quoted("""'foo "bar"'""", 10), False)

    def test_quoted_by_quoted_other_quote_character(self):
        self.assertEqual(self.is_quoted("""\\'foo "bar"\\'""", 0), False)
        self.assertEqual(self.is_quoted("""\\'foo "bar"\\'""", 1), True)
        self.assertEqual(self.is_quoted("""\\'foo "bar"\\'""", 5), False)
        self.assertEqual(self.is_quoted("""\\'foo "bar"\\'""", 6), False)
        self.assertEqual(self.is_quoted("""\\'foo "bar"\\'""", 10), False)
        self.assertEqual(self.is_quoted("""\\'foo "bar"\\'""", 11), False)
        self.assertEqual(self.is_quoted("""\\'foo "bar"\\'""", 12), True)

    def test_backslash_quoted_double_quote_preceeded_by_1_backslash(self):
        self.assertEqual(self.is_quoted('\\\\"', 2), False)
        self.assertEqual(self.is_quoted('\\\\"', 1), True)
        self.assertEqual(self.is_quoted('\\\\"', 0), False)

    def test_backslash_quoted_double_quote_preceeded_by_2_backslashes(self):
        self.assertEqual(self.is_quoted('\\\\\\"', 3), True)
        self.assertEqual(self.is_quoted('\\\\\\"', 2), False)
        self.assertEqual(self.is_quoted('\\\\\\"', 1), True)
        self.assertEqual(self.is_quoted('\\\\\\"', 0), False)

    def test_backslash_quoted_double_quote_preceeded_by_3_backslashes(self):
        self.assertEqual(self.is_quoted('\\\\\\\\"', 4), False)
        self.assertEqual(self.is_quoted('\\\\\\\\"', 3), True)
        self.assertEqual(self.is_quoted('\\\\\\\\"', 2), False)
        self.assertEqual(self.is_quoted('\\\\\\\\"', 1), True)
        self.assertEqual(self.is_quoted('\\\\\\\\"', 0), False)

    def test_normaldir(self):
        self.assertEqual(self.is_quoted('normaldir/\\"', 11), True)
        self.assertEqual(self.is_quoted('normaldir/\\"', 10), False)
        self.assertEqual(self.is_quoted('normaldir/\\"', 9), False)

    def test_normaldir_hello(self):
        self.assertEqual(self.is_quoted('normaldir/\\"Hello ', 17), False)
        self.assertEqual(self.is_quoted('normaldir/\\"Hello ', 11), True)
        self.assertEqual(self.is_quoted('normaldir/\\"Hello ', 10), False)

    def test_normaldir_hello_quoted(self):
        self.assertEqual(self.is_quoted('"normaldir/\\"Hello ', 18), True)
        self.assertEqual(self.is_quoted('"normaldir/\\"Hello ', 12), True)
        self.assertEqual(self.is_quoted('"normaldir/\\"Hello ', 11), True)

    def test_normaldir_hello_quoted_space(self):
        self.assertEqual(self.is_quoted('normaldir/\\"Hello\\ ', 18), True)
        self.assertEqual(self.is_quoted('normaldir/\\"Hello\\ ', 17), False)
        self.assertEqual(self.is_quoted('normaldir/\\"Hello\\ ', 11), True)
        self.assertEqual(self.is_quoted('normaldir/\\"Hello\\ ', 10), False)


class DirectoryCompletionHookTests(JailSetup):

    def setUp(self):
        JailSetup.setUp(self)
        reset()
        self.cmd = TestKmd(quote_char='\\')
        self.cmd.preloop()
        self.mkfiles()

    def complete(self, text):
        completion.line_buffer = text
        readline.complete_internal(TAB)
        return completion.line_buffer

    def mkfiles(self):
        self.mkdir('funny dir')
        self.mkfile('funny dir/foo.txt')
        self.mkfile('funny dir/foo.gif')

    def test_dir_completion(self):
        self.assertEqual(self.complete('fun'),
                                       'funny\\ dir/')

    def test_no_dir_completion_hook(self):
        # The current implementation works without a
        # directory_completion_hook.
        completer.directory_completion_hook = None
        self.assertEqual(self.complete('funny\\ dir/f'),
                                       'funny\\ dir/foo.')

    def test_dir_completion_hook(self):
        # Even if a hook is installed, it never receives a
        # quoted directory name.
        called = []
        def hook(text):
            called.append((text,))
            return text

        completer.directory_completion_hook = hook
        self.assertEqual(self.complete('funny\\ dir/f'),
                                       'funny\\ dir/foo.')
        self.assertEqual(called, [('funny dir/',)])

