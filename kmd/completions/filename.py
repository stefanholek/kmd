import os
import sys
import unicodedata

from rl import completer
from rl import completion
from rl import print_exc

from quoting import QUOTE_CHARACTERS
from quoting import BASH_QUOTE_CHARACTERS
from quoting import backslash_dequote
from quoting import backslash_quote
from quoting import char_is_quoted
from quoting import is_fully_quoted


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


def dequote_filename(text, quote_char):
    """Return a dequoted version of text."""
    if len(text) > 1:
        qc = quote_char
        # Don't backslash-dequote characters between single quotes,
        # except single quotes.
        if qc == "'":
            text = text.replace("'\\''", "'")
        elif '\\' in text:
            text = backslash_dequote(text)
    return text


def quote_filename(text, single_match, quote_char):
    """Return a quoted version of text."""
    if text:
        qc = quote_char or completer.quote_characters[0]
        # Don't backslash-quote backslashes between single quotes
        if qc == "'":
            text = text.replace("'", "'\\''")
        else:
            text = backslash_quote(text, '\\'+qc)
        # Don't add quotes if the filename is already fully quoted
        if qc == "'" or quote_char or not is_fully_quoted(text):
            # Quoting inhibits tilde-expansion by the shell so we
            # must expand any tildes before adding quotes
            if text.startswith('~') and not quote_char:
                text = completion.expand_tilde(text)
            if single_match:
                # Don't append closing quotes to directory names
                if os.path.isdir(os.path.expanduser(text)):
                    completion.suppress_quote = True
                if not completion.suppress_quote:
                    text = text + qc
            text = qc + text
    return text


def backslash_quote_filename(text, single_match, quote_char):
    """Return a backslash-quoted version of text."""
    if text:
        # If the user has typed a quote character, use it.
        if quote_char:
            text = quote_filename(text, single_match, quote_char)
        else:
            text = backslash_quote(text)
    return text


class FilenameCompletion(object):
    """Complete file and directory names.

    Extends readline's default filename quoting by taking
    care of backslash-quoted characters.
    """

    def __init__(self, quote_char='\\'):
        """Configure the readline completer for filename completion."""
        completer.quote_characters = QUOTE_CHARACTERS
        completer.char_is_quoted_function = self.char_is_quoted
        completer.filename_quoting_function = self.quote_filename
        if quote_char == "'":
            completer.quote_characters = BASH_QUOTE_CHARACTERS
        elif quote_char == '\\':
            completer.filename_quoting_function = self.backslash_quote_filename
        elif quote_char != '"':
            raise ValueError('quote_char must be one of " \' \\')

    @print_exc
    def __call__(self, text):
        """Return filenames matching 'text'."""
        matches = []
        # Dequoting early allows us to skip some hooks
        if completion.found_quote:
            text = self.dequote_filename(text, completion.quote_character)
        if text.startswith('~') and (os.sep not in text):
            matches = completion.complete_username(text)
        if not matches:
            matches = completion.complete_filename(text)
            # HFS Plus uses "decomposed" UTF-8
            if sys.platform == 'darwin':
                if not matches:
                    matches = completion.complete_filename(decompose(text))
                matches = [compose(x) for x in matches]
        return matches

    @print_exc
    def char_is_quoted(self, text, index):
        return char_is_quoted(text, index)

    @print_exc
    def dequote_filename(self, text, quote_char):
        return dequote_filename(text, quote_char)

    @print_exc
    def quote_filename(self, text, single_match, quote_char):
        return quote_filename(text, single_match, quote_char)

    @print_exc
    def backslash_quote_filename(self, text, single_match, quote_char):
        return backslash_quote_filename(text, single_match, quote_char)

