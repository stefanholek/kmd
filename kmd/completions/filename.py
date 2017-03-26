"""File and directory name completion."""

from __future__ import absolute_import

import os
import sys
import unicodedata

from rl import completer
from rl import completion
from rl import print_exc

from .quoting import QUOTE_CHARACTERS
from .quoting import BASH_QUOTE_CHARACTERS
from .quoting import char_is_quoted
from .quoting import dequote_filename
from .quoting import quote_filename
from .quoting import backslash_quote_filename


def decompose(text):
    """Return fully decomposed UTF-8 for HFS Plus."""
    if sys.version_info[0] >= 3:
        return unicodedata.normalize('NFD', text)
    else:
        return unicodedata.normalize('NFD', text.decode('utf-8')).encode('utf-8')


def compose(text):
    """Return fully composed UTF-8."""
    if sys.version_info[0] >= 3:
        return unicodedata.normalize('NFC', text)
    else:
        return unicodedata.normalize('NFC', text.decode('utf-8')).encode('utf-8')


class FilenameCompletion(object):
    """Complete file and directory names.
    The 'quote_char' argument specifies the preferred quoting style.
    Available styles are single-quote, double-quote, and backslash (the default).
    """

    def __init__(self, quote_char='\\'):
        """Configure the readline completer.
        """
        completer.quote_characters = QUOTE_CHARACTERS
        completer.char_is_quoted_function = self.char_is_quoted
        completer.filename_dequoting_function = None # We dequote manually
        completer.filename_quoting_function = self.quote_filename
        if quote_char == "'":
            completer.quote_characters = BASH_QUOTE_CHARACTERS
        elif quote_char == '\\':
            completer.filename_quoting_function = self.backslash_quote_filename
        elif quote_char != '"':
            raise ValueError('quote_char must be one of " \' \\')
        completer.directory_rewrite_hook = self.rewrite_directory
        completer.filename_rewrite_hook = self.rewrite_filename
        completer.filename_stat_hook = self.rewrite_directory

    def __call__(self, text):
        """Return filenames matching 'text'.
        Starts at the current working directory.
        """
        matches = []
        # Dequoting early allows us to skip some hooks
        if completion.found_quote:
            text = self.dequote_filename(text, completion.quote_character)
        if text.startswith('~') and (os.sep not in text):
            matches = completion.complete_username(text)
        if not matches:
            matches = completion.complete_filename(text)
            # HFS Plus and readline < 6.1
            if sys.platform == 'darwin' and completer.filename_rewrite_hook is None:
                if not matches:
                    matches = completion.complete_filename(decompose(text))
                matches = [compose(x) for x in matches]
        return matches

    @print_exc
    def char_is_quoted(self, text, index):
        """char_is_quoted(text, index)
        Return True if the character at 'index' is quoted.
        Installed as :attr:`rl.completer.char_is_quoted_function <rl:rl.Completer.char_is_quoted_function>`.
        """
        return char_is_quoted(text, index)

    def dequote_filename(self, text, quote_char):
        """dequote_filename(text, quote_char)
        Return a backslash-dequoted version of 'text'.
        Called from Python and not installed as a readline hook.
        """
        return dequote_filename(text, quote_char)

    @print_exc
    def quote_filename(self, text, single_match, quote_char):
        """quote_filename(text, single_match, quote_char)
        Return a quote-char quoted version of 'text'.
        Installed as :attr:`rl.completer.filename_quoting_function <rl:rl.Completer.filename_quoting_function>`
        if the preferred quoting style is single- or double-quote.
        """
        return quote_filename(text, single_match, quote_char)

    @print_exc
    def backslash_quote_filename(self, text, single_match, quote_char):
        """backslash_quote_filename(text, single_match, quote_char)
        Return a backslash-quoted version of 'text'.
        Installed as :attr:`rl.completer.filename_quoting_function <rl:rl.Completer.filename_quoting_function>`
        if the preferred quoting style is backslash (the default).
        """
        return backslash_quote_filename(text, single_match, quote_char)

    @print_exc
    def rewrite_directory(self, text):
        """rewrite_directory(text)
        Convert a filename the user typed to a format suitable for passing to 'opendir' and 'stat'.
        Installed as :attr:`rl.completer.directory_rewrite_hook <rl:rl.Completer.directory_rewrite_hook>`
        and :attr:`rl.completer.filename_stat_hook <rl:rl.Completer.filename_stat_hook>`.
        """
        if sys.version_info[0] >= 3:
            return text # Force locale encoding -> fs encoding

    @print_exc
    def rewrite_filename(self, text):
        """rewrite_filename(text)
        Convert a filename read from the filesystem to a format suitable for comparing
        against the completion word.
        Installed as :attr:`rl.completer.filename_rewrite_hook <rl:rl.Completer.filename_rewrite_hook>`.
        On Mac OS X this converts decomposed UTF-8 used by the HFS Plus filesystem
        to fully composed UTF-8.
        """
        if sys.platform == 'darwin':
            return compose(text)
        if sys.version_info[0] >= 3:
            return text # Force fs encoding -> locale encoding

