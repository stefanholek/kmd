# -*- coding: utf-8 -*-

import unittest

from rl import completer
from rl import completion
from rl import generator
from rl import readline
from rl import print_exc

from kmd import Kmd

from kmd.quoting import backslash_dequote
from kmd.quoting import backslash_quote
from kmd.quoting import is_fully_quoted
from kmd.quoting import char_is_quoted
from kmd.quoting import backslash_dequote_string
from kmd.quoting import quote_string
from kmd.quoting import backslash_quote_string
from kmd.quoting import backslash_dequote_filename
from kmd.quoting import quote_filename
from kmd.quoting import backslash_quote_filename

from kmd.testing import JailSetup
from kmd.testing import reset

TAB = '\t'


@print_exc
@generator
def completefilename(text):
    # Use the built-in filename completion
    return completion.complete_filename(text)


class FileSetup(JailSetup):

    def setUp(self):
        JailSetup.setUp(self)
        self.mkfiles()

    def complete(self, text):
        completion.line_buffer = text
        readline.complete_internal(TAB)
        return completion.line_buffer

    def mkfiles(self):
        self.mkfile("Al'Hambra.txt")
        self.mkfile('Foo\\"Peng\\".txt')
        #self.mkfile('Foo\\Bar.txt')
        #self.mkfile('Foo\\Baz.txt')
        self.mkfile('Hello World.txt')
        #self.mkfile('Lee "Scratch" Perry.txt')
        #self.mkfile('Mädchen.txt')
        #self.mkfile('Simple.txt')
        self.mkfile('Sys$Home.txt')
        self.mkfile('Tilde.tx~')
        self.mkfile('~StartsWithTilde.txt')


class BackslashDequoteTests(unittest.TestCase):

    def setUp(self):
        reset()
        self.cmd = Kmd()
        self.cmd.preloop()

    def test_backslash_dequote(self):
        self.assertEqual(backslash_dequote(''), '')
        self.assertEqual(backslash_dequote(' '), ' ')
        self.assertEqual(backslash_dequote('\\ '), ' ')
        self.assertEqual(backslash_dequote('a'), 'a')
        self.assertEqual(backslash_dequote('\\@'), '@')

    def test_backslash_dequote_string(self):
        self.assertEqual(backslash_dequote(r'\ foo\ bar\#baz\&'), r' foo bar#baz&')

    def test_backslash_dequote_backslash(self):
        self.assertEqual(backslash_dequote(r'foo\\\\\ bar'), r'foo\\ bar')
        self.assertEqual(backslash_dequote(r'foo\\\\ bar'), r'foo\ bar')
        self.assertEqual(backslash_dequote(r'foo\\\ bar'), r'foo\ bar')
        self.assertEqual(backslash_dequote(r'foo\\ bar'), r'foo bar')
        self.assertEqual(backslash_dequote(r'foo\ bar'), r'foo bar')

    def test_backslash_dequote_unknown_char(self):
        self.assertEqual(backslash_dequote('\\€'), '\\€') # NB: not dequoted


class BackslashQuoteTests(unittest.TestCase):

    def setUp(self):
        reset()
        self.cmd = Kmd()
        self.cmd.preloop()

    def test_backslash_quote(self):
        self.assertEqual(backslash_quote(''), '')
        self.assertEqual(backslash_quote(' '), '\\ ')
        self.assertEqual(backslash_quote('a'), 'a')
        self.assertEqual(backslash_quote('@'), '\\@')

    def test_backslash_quote_string(self):
        self.assertEqual(backslash_quote(r' foo bar#baz&'), r'\ foo\ bar\#baz\&')

    def test_backslash_quote_backslash(self):
        self.assertEqual(backslash_quote(r'foo bar'), r'foo\ bar')
        self.assertEqual(backslash_quote(r'foo\ bar'), r'foo\\\ bar')
        self.assertEqual(backslash_quote(r'foo\\ bar'), r'foo\\\\\ bar')

    def test_backslash_quote_unknown_char(self):
        self.assertEqual(backslash_quote('€'), '€')


class FullyQuotedTests(unittest.TestCase):

    def setUp(self):
        reset()
        self.cmd = Kmd()
        self.cmd.preloop()

    def test_fully_quoted(self):
        self.assertEqual(is_fully_quoted(r'foo\ bar\"baz\&'), True)
        self.assertEqual(is_fully_quoted(r'foo\ bar\"baz\\'), True)

    def test_not_fully_quoted(self):
        self.assertEqual(is_fully_quoted('foo&bar'), False)
        self.assertEqual(is_fully_quoted('foo\\&bar\\'), False)


class CharIsQuotedTests(unittest.TestCase):

    TRUE = (
        '" ',
        '"foo ',
        'f"oo ',
        'fo"o ',
        'foo" ',
        '\' ',
        '\'foo ',
        'f\'oo ',
        'fo\'o ',
        'foo\' ',
        '\\ ',
        'foo\\ ',
        '"foo\\ ',
        '"foo\\" ',
        '"foo\\"\\ ',
        '"foo"\\ ',
        '"foo\' ',
        '"foo\\\' ',
        '\'foo\\ ',
        '\'foo\\\'\\ ',
        '\'foo" ',
        '\'foo\\" ',
        '"foo \'bar\' ',
        '\'foo "bar" ',
        '"foo \'bar\'',
        '\'foo "bar"',
        '"foo \'bar\'\'',
        '\'foo "bar""',
        '\'foo\\\'"\'',
        '\'foo"\'"\'',
        # Backslashes
        'foo \\\\',
        'foo \\a',
    )

    FALSE = (
        'foo ',
        'fo\\o ',
        'foo\\\\ ',
        '"" ',
        '"foo" ',
        '"foo\'" ',
        '\'\' ',
        '\'foo\' ',
        '\'foo\\\' ',
        '\'foo"\' ',
        '\'foo\'\'',
        '\'foo\\\'\'',
        '\'foo"\'\'',
        '\'foo\\\'\'\'',
        # A closing quote character does not count as "quoted"
        '\'foo"\'\'\'',
        '"foo \'bar\'"',
        '\'foo "bar"\'',
        # Backslashes
        'foo \\',
        'foo \\\\\\',
        'foo \\\\a',
        'foo a',
    )

    def setUp(self):
        reset()
        completer.quote_characters = '"\''

    def test_true(self):
        # Expect the last character in s to be quoted
        for s in self.TRUE:
            self.assertEqual(char_is_quoted(s, len(s)-1), True, 'not True: %r' % s)

    def test_false(self):
        # Expect the last character in s to not be quoted
        for s in self.FALSE:
            self.assertEqual(char_is_quoted(s, len(s)-1), False, 'not False: %r' % s)


class DequoteStringTests(FileSetup):

    def setUp(self):
        FileSetup.setUp(self)
        reset()
        self.cmd = Kmd()
        self.cmd.preloop()
        completer.completer = completefilename
        completer.filename_dequoting_function = print_exc(backslash_dequote_string)
        completer.filename_quoting_function = lambda x,y,z: x

    def test_dequote_string(self):
        self.assertEqual(self.complete(''), '')
        self.assertEqual(self.complete(r'Hello'), r'Hello World.txt ')
        self.assertEqual(self.complete(r'Hello\ '), r'Hello World.txt ')
        self.assertEqual(self.complete(r"Al\'"), r"Al'Hambra.txt ")
        self.assertEqual(self.complete(r'Foo\\\"'), r'Foo\"Peng\".txt ')
        self.assertEqual(self.complete(r'Sys\$'), r'Sys$Home.txt ')
        self.assertEqual(self.complete(r'Tilde.tx\~'), r'Tilde.tx~ ')
        self.assertEqual(self.complete(r'\~'), r'~StartsWithTilde.txt ')

    def test_dequote_if_single_quote_default(self):
        completer.quote_characters = "'\""
        self.assertEqual(self.complete(''), '')
        self.assertEqual(self.complete(r'Hello'), r'Hello World.txt ')
        self.assertEqual(self.complete(r'Hello\ '), r'Hello World.txt ')
        self.assertEqual(self.complete(r"Al\'"), r"Al'Hambra.txt ")
        self.assertEqual(self.complete(r'Foo\\\"'), r'Foo\"Peng\".txt ')
        self.assertEqual(self.complete(r'Sys\$'), r'Sys$Home.txt ')
        self.assertEqual(self.complete(r'Tilde.tx\~'), r'Tilde.tx~ ')
        self.assertEqual(self.complete(r'\~'), r'~StartsWithTilde.txt ')


class QuoteStringTests(FileSetup):

    def setUp(self):
        FileSetup.setUp(self)
        reset()
        self.cmd = Kmd()
        self.cmd.preloop()
        completer.completer = completefilename
        completer.filename_dequoting_function = print_exc(backslash_dequote_string)
        completer.filename_quoting_function = print_exc(quote_string)

    def test_quote_string(self):
        self.assertEqual(self.complete(''), '')
        self.assertEqual(self.complete(r'Hello'), r'"Hello World.txt" ')
        self.assertEqual(self.complete(r'Hello\ '), r'"Hello World.txt" ')
        self.assertEqual(self.complete(r"Al\'"), r'''"Al'Hambra.txt" ''')
        self.assertEqual(self.complete(r'Foo\\\"'), r'Foo\\\"Peng\\\".txt ')
        self.assertEqual(self.complete(r'Sys\$'), r'Sys\$Home.txt ')
        self.assertEqual(self.complete(r'Tilde.tx\~'), r'Tilde.tx~ ')
        self.assertEqual(self.complete(r'\~'), r'~StartsWithTilde.txt ')

    def test_user_quote_string(self):
        self.assertEqual(self.complete('"'), '"')
        self.assertEqual(self.complete('"Hello'), '"Hello World.txt" ')
        self.assertEqual(self.complete('"Hello '), '"Hello World.txt" ')
        self.assertEqual(self.complete("\"Al'"), '''"Al'Hambra.txt" ''')
        self.assertEqual(self.complete(r'"Foo\\\"'), r'"Foo\\\"Peng\\\".txt" ')
        self.assertEqual(self.complete(r'"Sys\$'), r'"Sys\$Home.txt" ')
        self.assertEqual(self.complete('"Tilde.tx~'), '"Tilde.tx~" ')
        self.assertEqual(self.complete('"~'), '"~StartsWithTilde.txt" ')

    def test_quote_directory(self):
        self.mkdir('funny dir')
        self.assertEqual(self.complete('fun'), '"funny dir"/') # NB: slash appended by readline

    def test_user_quote_directory(self):
        self.mkdir('funny dir')
        self.assertEqual(self.complete('"fun'), '"funny dir"/') # NB: slash appended by readline


class BackslashQuoteStringTests(FileSetup):

    def setUp(self):
        FileSetup.setUp(self)
        reset()
        self.cmd = Kmd()
        self.cmd.preloop()
        completer.completer = completefilename
        completer.filename_dequoting_function = print_exc(backslash_dequote_string)
        completer.filename_quoting_function = print_exc(backslash_quote_string)

    def test_backslash_quote_string(self):
        self.assertEqual(self.complete(''), '')
        self.assertEqual(self.complete(r'Hello'), r'Hello\ World.txt ')
        self.assertEqual(self.complete(r'Hello\ '), r'Hello\ World.txt ')
        self.assertEqual(self.complete(r"Al\'"), r"Al\'Hambra.txt ")
        self.assertEqual(self.complete(r'Foo\\\"'), r'Foo\\\"Peng\\\".txt ')
        self.assertEqual(self.complete(r'Sys\$'), r'Sys\$Home.txt ')
        self.assertEqual(self.complete(r'Tilde.tx\~'), r'Tilde.tx~ ')
        self.assertEqual(self.complete(r'\~'), r'~StartsWithTilde.txt ')

    def test_user_quote_string(self):
        self.assertEqual(self.complete('"'), '"')
        self.assertEqual(self.complete('"Hello'), '"Hello World.txt" ')
        self.assertEqual(self.complete('"Hello '), '"Hello World.txt" ')
        self.assertEqual(self.complete("\"Al'"), '''"Al'Hambra.txt" ''')
        self.assertEqual(self.complete(r'"Foo\\\"'), r'"Foo\\\"Peng\\\".txt" ')
        self.assertEqual(self.complete(r'"Sys\$'), r'"Sys\$Home.txt" ')
        self.assertEqual(self.complete('"Tilde.tx~'), '"Tilde.tx~" ')
        self.assertEqual(self.complete('"~'), '"~StartsWithTilde.txt" ')

    def test_backslash_quote_directory(self):
        self.mkdir('funny dir')
        self.assertEqual(self.complete('fun'), 'funny\\ dir/') # NB: slash appended by readline

    def test_user_quote_directory(self):
        self.mkdir('funny dir')
        self.assertEqual(self.complete('"fun'), '"funny dir"/') # NB: slash appended by readline


class DequoteFilenameTests(FileSetup):

    def setUp(self):
        FileSetup.setUp(self)
        reset()
        self.cmd = Kmd()
        self.cmd.preloop()
        completer.completer = completefilename
        completer.filename_dequoting_function = print_exc(backslash_dequote_filename)
        completer.filename_quoting_function = lambda x,y,z: x

    def test_dequote_filename(self):
        self.assertEqual(self.complete(''), '')
        self.assertEqual(self.complete(r'Hello'), r'Hello World.txt ')
        self.assertEqual(self.complete(r'Hello\ '), r'Hello World.txt ')
        self.assertEqual(self.complete(r"Al\'"), r"Al'Hambra.txt ")
        self.assertEqual(self.complete(r'Foo\\\"'), r'Foo\"Peng\".txt ')
        self.assertEqual(self.complete(r'Sys\$'), r'Sys$Home.txt ')
        self.assertEqual(self.complete(r'Tilde.tx\~'), r'Tilde.tx~ ')
        self.assertEqual(self.complete(r'\~'), r'~StartsWithTilde.txt ')

    def test_dequote_if_single_quote_default(self):
        completer.quote_characters = "'\""
        self.assertEqual(self.complete(''), '')
        self.assertEqual(self.complete(r'Hello'), r'Hello World.txt ')
        self.assertEqual(self.complete(r'Hello\ '), r'Hello World.txt ')
        self.assertEqual(self.complete(r"Al\'"), r"Al'Hambra.txt ")
        self.assertEqual(self.complete(r'Foo\\\"'), r'Foo\"Peng\".txt ')
        self.assertEqual(self.complete(r'"Sys\$'), r'"Sys$Home.txt" ')
        self.assertEqual(self.complete(r'Tilde.tx\~'), r'Tilde.tx~ ')
        self.assertEqual(self.complete(r'\~'), r'~StartsWithTilde.txt ')


class QuoteFilenameTests(FileSetup):

    def setUp(self):
        FileSetup.setUp(self)
        reset()
        self.cmd = Kmd()
        self.cmd.preloop()
        completer.completer = completefilename
        completer.filename_dequoting_function = print_exc(backslash_dequote_filename)
        completer.filename_quoting_function = print_exc(quote_filename)

    def test_quote_filename(self):
        self.assertEqual(self.complete(''), '')
        self.assertEqual(self.complete(r'Hello'), r'"Hello World.txt" ')
        self.assertEqual(self.complete(r'Hello\ '), r'"Hello World.txt" ')
        self.assertEqual(self.complete(r"Al\'"), r'''"Al'Hambra.txt" ''')
        self.assertEqual(self.complete(r'Foo\\\"'), r'Foo\\\"Peng\\\".txt ')
        self.assertEqual(self.complete(r'Sys\$'), r'Sys\$Home.txt ')
        self.assertEqual(self.complete(r'Tilde.tx\~'), r'Tilde.tx~ ')
        self.assertEqual(self.complete(r'\~'), r'~StartsWithTilde.txt ')

    def test_user_quote_filename(self):
        self.assertEqual(self.complete('"'), '"')
        self.assertEqual(self.complete('"Hello'), '"Hello World.txt" ')
        self.assertEqual(self.complete('"Hello '), '"Hello World.txt" ')
        self.assertEqual(self.complete("\"Al'"), '''"Al'Hambra.txt" ''')
        self.assertEqual(self.complete(r'"Foo\\\"'), r'"Foo\\\"Peng\\\".txt" ')
        self.assertEqual(self.complete(r'"Sys\$'), r'"Sys\$Home.txt" ')
        self.assertEqual(self.complete('"Tilde.tx~'), '"Tilde.tx~" ')
        self.assertEqual(self.complete('"~'), '"~StartsWithTilde.txt" ')

    def test_quote_directory(self):
        self.mkdir('funny dir')
        self.assertEqual(self.complete('fun'), '"funny dir/') # NB: No closing quote on dir

    def test_user_quote_directory(self):
        self.mkdir('funny dir')
        self.assertEqual(self.complete('"fun'), '"funny dir/') # NB: no closing quote on dir


class BackslashQuoteFilenameTests(FileSetup):

    def setUp(self):
        FileSetup.setUp(self)
        reset()
        self.cmd = Kmd()
        self.cmd.preloop()
        completer.completer = completefilename
        completer.filename_dequoting_function = print_exc(backslash_dequote_filename)
        completer.filename_quoting_function = print_exc(backslash_quote_filename)

    def test_backslash_quote_filename(self):
        self.assertEqual(self.complete(''), '')
        self.assertEqual(self.complete(r'Hello'), r'Hello\ World.txt ')
        self.assertEqual(self.complete(r'Hello\ '), r'Hello\ World.txt ')
        self.assertEqual(self.complete(r"Al\'"), r"Al\'Hambra.txt ")
        self.assertEqual(self.complete(r'Foo\\\"'), r'Foo\\\"Peng\\\".txt ')
        self.assertEqual(self.complete(r'Sys\$'), r'Sys\$Home.txt ')
        self.assertEqual(self.complete(r'Tilde.tx\~'), r'Tilde.tx~ ')
        self.assertEqual(self.complete(r'\~'), r'~StartsWithTilde.txt ')

    def test_user_quote_filename(self):
        self.assertEqual(self.complete('"'), '"')
        self.assertEqual(self.complete('"Hello'), '"Hello World.txt" ')
        self.assertEqual(self.complete('"Hello '), '"Hello World.txt" ')
        self.assertEqual(self.complete("\"Al'"), '''"Al'Hambra.txt" ''')
        self.assertEqual(self.complete(r'"Foo\\\"'), r'"Foo\\\"Peng\\\".txt" ')
        self.assertEqual(self.complete(r'"Sys\$'), r'"Sys\$Home.txt" ')
        self.assertEqual(self.complete('"Tilde.tx~'), '"Tilde.tx~" ')
        self.assertEqual(self.complete('"~'), '"~StartsWithTilde.txt" ')

    def test_backslash_quote_directory(self):
        self.mkdir('funny dir')
        self.assertEqual(self.complete('fun'), 'funny\\ dir/')

    def test_user_quote_directory(self):
        self.mkdir('funny dir')
        self.assertEqual(self.complete('"fun'), '"funny dir/') # NB: no closing quote on dir


class SetTests(unittest.TestCase):

    def test_union(self):
        self.assertEqual(set('abc').union('def'), set('abcdef'))

    def test_operator(self):
        self.assertEqual(set('abc') | set('def'), set('abcdef'))

    def test_iterate(self):
        i = 0
        for x in set('abc'):
            i += 1
        self.assertEqual(i, 3)

