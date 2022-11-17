"""String and filename quoting support."""

import os
import sys

from rl import completer
from rl import completion

#: Quote characters used by Bash.
BASH_QUOTE_CHARACTERS = "'\""

#: Word break characters used by Bash.
BASH_COMPLETER_WORD_BREAK_CHARACTERS = " \t\n\"'@><;|&=(:"

#: Word break characters used by Bash when hostname completion is off.
BASH_NOHOSTNAME_WORD_BREAK_CHARACTERS = " \t\n\"'><;|&=(:"

#: Filename quote characters used by Bash.
BASH_FILENAME_QUOTE_CHARACTERS = "\\ \t\n\"'@><;|&=()#$`?*[!:{~"

#: Command separators used by Bash.
BASH_COMMAND_SEPARATORS = ";|&{(`"

#: Whitespace characters used by Bash.
BASH_WHITESPACE_CHARACTERS = " \t\n"

#: Slashify characters used by Bash.
BASH_SLASHIFY_IN_QUOTES = "\\\"$`\n"

#: These characters may be used in pairs to quote substrings of the line.
QUOTE_CHARACTERS = "\"'"

#: These characters define word boundaries.
WORD_BREAK_CHARACTERS = BASH_NOHOSTNAME_WORD_BREAK_CHARACTERS

#: These characters are quoted when they occur in filenames.
FILENAME_QUOTE_CHARACTERS = BASH_FILENAME_QUOTE_CHARACTERS[:-1]

# BBB
WHITESPACE_CHARACTERS = BASH_WHITESPACE_CHARACTERS

#: These characters are backslash-quoted even between double quotes.
SLASHIFY_IN_QUOTES = BASH_SLASHIFY_IN_QUOTES


def backslash_dequote(text, chars=''):
    """Backslash-dequote all
    :attr:`rl.completer.filename_quote_characters <rl:rl.Completer.filename_quote_characters>`
    in ``text``.
    If ``chars`` is given, only characters in ``chars`` are dequoted.
    """
    if not chars:
        chars = set(completer.filename_quote_characters).union(BASH_FILENAME_QUOTE_CHARACTERS)
    if '\\' in chars:
        text = text.replace('\\\\', '\\')
    for c in chars:
        if c != '\\':
            text = text.replace('\\'+c, c)
    return text


def backslash_quote(text, chars=''):
    """Backslash-quote all
    :attr:`rl.completer.filename_quote_characters <rl:rl.Completer.filename_quote_characters>`
    in ``text``.
    If ``chars`` is given, only characters in ``chars`` are quoted.
    """
    if not chars:
        chars = completer.filename_quote_characters
    if '\\' in chars:
        text = text.replace('\\', '\\\\')
    for c in chars:
        if c != '\\':
            text = text.replace(c, '\\'+c)
    return text


def is_fully_quoted(text, chars=''):
    """Return True if all
    :attr:`rl.completer.filename_quote_characters <rl:rl.Completer.filename_quote_characters>`
    in ``text`` are backslash-quoted.
    If ``chars`` is given, only characters in ``chars`` are checked.
    """
    if not chars:
        chars = completer.filename_quote_characters
    skip_next = False
    size = len(text)
    for i in range(size):
        c = text[i]
        if skip_next:
            skip_next = False
        elif c == '\\':
            skip_next = True
            if i == size-1:
                return False
        elif c in chars:
            return False
    return True


def char_is_quoted(text, index):
    """Return True if the character at ``index`` is quoted."""
    skip_next = False
    quote_char = ''
    for i in range(index):
        c = text[i]
        if skip_next:
            skip_next = False
        elif quote_char != "'" and c == '\\':
            skip_next = True
            if i == index-1:
                return True
        elif quote_char != '':
            if c == quote_char:
                quote_char = ''
        elif c in completer.quote_characters:
            quote_char = c
    # A closing quote character is never quoted
    if index < len(text) and text[index] == quote_char:
        return False
    return bool(quote_char)


def char_is_backslash_quoted(text, index):
    """Return True if the character at ``index`` is backslash-quoted."""
    skip_next = False
    for i in range(index):
        c = text[i]
        if skip_next:
            skip_next = False
        elif c == '\\':
            skip_next = True
            if i == index-1:
                return True
    return False


def backslash_dequote_string(text, quote_char=''):
    """Return a backslash-dequoted version of ``text``.
    If ``quote_char`` is the single-quote, backslash-dequoting is
    limited to single-quotes.
    """
    if len(text) > 1:
        qc = quote_char
        # Don't backslash-dequote characters between single-quotes,
        # except single-quotes.
        if qc == "'":
            text = text.replace("'\\''", "'")
        elif qc != '':
            text = backslash_dequote(text, SLASHIFY_IN_QUOTES)
        elif '\\' in text:
            text = backslash_dequote(text)
    return text

backslash_dequote_filename = backslash_dequote_string


def quote_string(text, single_match=True, quote_char=''):
    """Return a ``quote_char``-quoted version of ``text``.
    If ``single_match`` is False, the quotes are not closed.
    The default ``quote_char`` is the first character in
    :attr:`rl.completer.quote_characters <rl:rl.Completer.quote_characters>`.
    """
    if text:
        qc = quote_char or completer.quote_characters[:1]
        # Don't backslash-quote single-quotes between single-quotes
        if qc == "'":
            text = text.replace("'", "'\\''")
        else:
            text = backslash_quote(text, SLASHIFY_IN_QUOTES)
        # Don't add quotes if the string is already fully quoted
        if qc == "'" or quote_char or not is_fully_quoted(text):
            if single_match:
                if not completion.suppress_quote:
                    text = text + qc
            text = qc + text
    return text


def backslash_quote_string(text, single_match=True, quote_char=''):
    """Return a backslash-quoted version of ``text``.
    If a ``quote_char`` is given, behave like :func:`~kmd.quoting.quote_string`.
    """
    if text:
        # If the user has typed a quote character, use it.
        if quote_char:
            text = quote_string(text, single_match, quote_char)
        else:
            text = backslash_quote(text)
    return text


def quote_filename(text, single_match=True, quote_char=''):
    """Return a ``quote_char``-quoted version of ``text``.
    If ``single_match`` is False or ``text`` is a directory, the
    quotes are not closed.
    The default ``quote_char`` is the first character in
    :attr:`rl.completer.quote_characters <rl:rl.Completer.quote_characters>`.
    """
    if text:
        qc = quote_char or completer.quote_characters[:1]
        # Don't backslash-quote single-quotes between single-quotes
        if qc == "'":
            text = text.replace("'", "'\\''")
        else:
            text = backslash_quote(text, SLASHIFY_IN_QUOTES)
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


def backslash_quote_filename(text, single_match=True, quote_char=''):
    """Return a backslash-quoted version of ``text``.
    If a ``quote_char`` is given, behave like :func:`~kmd.quoting.quote_filename`.
    """
    if text:
        # If the user has typed a quote character, use it.
        if quote_char:
            text = quote_filename(text, single_match, quote_char)
        else:
            text = backslash_quote(text)
    return text

