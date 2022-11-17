"""File and directory name completion."""

from __future__ import absolute_import

import os
import sys
import unicodedata

from rl import completer
from rl import completion
from rl import print_exc

from kmd.quoting import QUOTE_CHARACTERS
from kmd.quoting import WORD_BREAK_CHARACTERS
from kmd.quoting import FILENAME_QUOTE_CHARACTERS

from kmd.quoting import char_is_quoted
from kmd.quoting import quote_filename
from kmd.quoting import backslash_quote_filename
from kmd.quoting import backslash_dequote_filename


def compose(text):
    """Return fully composed UTF-8."""
    if sys.version_info[0] >= 3:
        return unicodedata.normalize('NFC', text)
    else:
        return unicodedata.normalize('NFC', text.decode('utf-8')).encode('utf-8')


class FilenameCompletion(object):
    """Complete file and directory names.
    The ``quote_char`` argument specifies the preferred quoting style.
    Available styles are single-quote, double-quote, and backslash (the
    default).

    To ensure proper configuration of readline, :class:`~FilenameCompletion`
    should always be instantiated before other completions.
    """

    def __init__(self, quote_char='\\'):
        """Configure the readline completer.
        """
        completer.quote_characters = QUOTE_CHARACTERS
        completer.word_break_characters = WORD_BREAK_CHARACTERS
        completer.special_prefixes = ''
        completer.filename_quote_characters = FILENAME_QUOTE_CHARACTERS

        completer.char_is_quoted_function = self.char_is_quoted
        completer.filename_quoting_function = self.quote_filename
        completer.filename_dequoting_function = self.dequote_filename

        completer.directory_rewrite_hook = self.rewrite_dirname
        completer.filename_rewrite_hook = self.rewrite_filename
        completer.filename_stat_hook = self.stat_filename

        self.backslash_quoting = False
        if quote_char == '\\':
            self.backslash_quoting = True
        elif quote_char == "'":
            completer.quote_characters = QUOTE_CHARACTERS[::-1]
        elif quote_char != '"':
            raise ValueError('quote_char must be single-quote, double-quote, or backslash')

    def __call__(self, text):
        """Return filenames matching ``text``.
        Starts at the current working directory.
        """
        matches = []
        if text.startswith('~') and (os.sep not in text):
            matches = completion.complete_username(text)
        if not matches:
            matches = completion.complete_filename(text)
        return matches

    @print_exc
    def char_is_quoted(self, text, index):
        """char_is_quoted(text, index)
        Return True if the character at ``index`` is quoted.
        Installed as :attr:`rl.completer.char_is_quoted_function <rl:rl.Completer.char_is_quoted_function>`.
        """
        return char_is_quoted(text, index)

    @print_exc
    def quote_filename(self, text, single_match, quote_char):
        """quote_filename(text, single_match, quote_char)
        Return a quoted version of ``text``. Installed as
        :attr:`rl.completer.filename_quoting_function <rl:rl.Completer.filename_quoting_function>`.
        """
        if self.backslash_quoting:
            return backslash_quote_filename(text, single_match, quote_char)
        else:
            return quote_filename(text, single_match, quote_char)

    @print_exc
    def dequote_filename(self, text, quote_char):
        """dequote_filename(text, quote_char)
        Return a dequoted version of ``text``. Installed as
        :attr:`rl.completer.filename_dequoting_function <rl:rl.Completer.filename_dequoting_function>`.
        """
        return backslash_dequote_filename(text, quote_char)

    @print_exc
    def rewrite_dirname(self, text):
        """rewrite_dirname(text)
        Convert a directory name the user typed to a format suitable for passing
        to ``opendir()``.
        Installed as :attr:`rl.completer.directory_rewrite_hook <rl:rl.Completer.directory_rewrite_hook>`.
        """
        # Dequote dirname
        if completion.found_quote:
            return backslash_dequote_filename(text, completion.quote_character)

        # Convert locale encoding -> fs encoding
        if sys.version_info[0] >= 3:
            return text

    @print_exc
    def rewrite_filename(self, text):
        """rewrite_filename(text)
        Convert a filename read from the filesystem to a format suitable for
        comparing against the completion word.
        Installed as :attr:`rl.completer.filename_rewrite_hook <rl:rl.Completer.filename_rewrite_hook>`.
        """
        # Compose filename received from HFS Plus
        if sys.platform == 'darwin':
            return compose(text)

        # Convert fs encoding -> locale encoding
        if sys.version_info[0] >= 3:
            return text

    @print_exc
    def stat_filename(self, text):
        """stat_filename(text)
        Convert a filename the user typed to a format suitable for passing
        to ``stat()``.
        Installed as :attr:`rl.completer.filename_stat_hook <rl:rl.Completer.filename_stat_hook>`.
        """
        # Convert locale encoding -> fs encoding
        if sys.version_info[0] >= 3:
            return text

