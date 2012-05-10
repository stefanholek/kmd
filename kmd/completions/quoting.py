"""String quoting and dequoting support."""

from rl import completer
from rl import completion

#: Quote characters used by Bash.
BASH_QUOTE_CHARACTERS = "'\""

#: Word break characters used by Bash.
BASH_COMPLETER_WORD_BREAK_CHARACTERS = " \t\n\"'@><;|&=(:"

#: Word break characters used by Bash when hostname completion is disabled.
BASH_NOHOSTNAME_WORD_BREAK_CHARACTERS = " \t\n\"'><;|&=(:"

#: Filename quote characters used by Bash.
BASH_FILENAME_QUOTE_CHARACTERS = "\\ \t\n\"'@><;|&=()#$`?*[!:{~" # Backslash must be first

#: Command separators used by Bash.
BASH_COMMAND_SEPARATORS = ";|&{(`"

#: Whitespace characters used by Bash.
BASH_WHITESPACE_CHARACTERS = " \t\n"

#: Quote characters used by kmd.
QUOTE_CHARACTERS = "\"'"

#: Word break characters used by kmd.
WORD_BREAK_CHARACTERS = BASH_NOHOSTNAME_WORD_BREAK_CHARACTERS[:-3]

#: Filename quote characters used by kmd.
FILENAME_QUOTE_CHARACTERS = BASH_FILENAME_QUOTE_CHARACTERS[:-1]

# BBB
WHITESPACE_CHARACTERS = BASH_WHITESPACE_CHARACTERS

# Dict used for backslash quoting
QUOTED = dict((x, '\\'+x) for x in BASH_FILENAME_QUOTE_CHARACTERS)


def backslash_dequote(text, chars=''):
    """Backslash-dequote 'text'.
    If 'chars' is given, only characters in 'chars' are dequoted.
    """
    for c in (chars or BASH_FILENAME_QUOTE_CHARACTERS):
        text = text.replace(QUOTED[c], c)
    return text


def backslash_quote(text, chars=''):
    """Backslash-quote 'text'.
    If 'chars' is given, only characters in 'chars' are quoted.
    """
    for c in (chars or completer.filename_quote_characters):
        text = text.replace(c, QUOTED[c])
    return text


def is_fully_quoted(text):
    """Return True if all
    :attr:`rl.completer.filename_quote_characters <rl:rl.Completer.filename_quote_characters>`
    in 'text' are backslash-quoted.
    """
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
        elif c in completer.filename_quote_characters:
            return False
    return True


def char_is_quoted(text, index):
    """Return True if the character at 'index' is quoted."""
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


def dequote_string(text, quote_char=''):
    """Return a backslash-dequoted version of 'text'.
    If 'quote_char' is the single-quote, backslash-dequoting is
    limited to single-quotes.
    """
    if len(text) > 1:
        qc = quote_char
        # Don't backslash-dequote characters between single-quotes,
        # except single-quotes.
        if qc == "'":
            text = text.replace("'\\''", "'")
        elif '\\' in text:
            text = backslash_dequote(text)
    return text


def quote_string(text, single_match=True, quote_char=''):
    """Return a quote-char quoted version of 'text'.
    If 'single_match' is False, the quotes are not closed.
    The default 'quote_char' is the first character in
    :attr:`rl.completer.quote_characters <rl:rl.Completer.quote_characters>`.
    """
    if text:
        qc = quote_char or completer.quote_characters[0]
        # Don't backslash-quote backslashes between single quotes
        if qc == "'":
            text = text.replace("'", "'\\''")
        else:
            text = backslash_quote(text, '\\'+qc)
        # Don't add quotes if the string is already fully quoted
        if qc == "'" or quote_char or not is_fully_quoted(text):
            if single_match:
                if not completion.suppress_quote:
                    text = text + qc
            text = qc + text
    return text


def backslash_quote_string(text, single_match=True, quote_char=''):
    """Return a backslash-quoted version of 'text'.
    If a 'quote_char' is given, behave like :func:`~kmd.completions.quoting.quote_string`.
    """
    if text:
        # If the user has typed a quote character, use it.
        if quote_char:
            text = quote_string(text, single_match, quote_char)
        else:
            text = backslash_quote(text)
    return text

