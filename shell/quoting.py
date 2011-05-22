from rl import completer
from rl import completion

BASH_QUOTE_CHARACTERS = "'\""
BASH_COMPLETER_WORD_BREAK_CHARACTERS = " \t\n\"'@><;|&=(:"
BASH_NOHOSTNAME_WORD_BREAK_CHARACTERS = " \t\n\"'><;|&=(:"
BASH_FILENAME_QUOTE_CHARACTERS = "\\ \t\n\"'@><;|&=()#$`?*[!:{~" # Backslash must be first
BASH_COMMAND_SEPARATORS = ";|&{(`"

WHITESPACE_CHARACTERS = " \t\n"
QUOTE_CHARACTERS = "\"'"
WORD_BREAK_CHARACTERS = BASH_NOHOSTNAME_WORD_BREAK_CHARACTERS[:-3]
FILENAME_QUOTE_CHARACTERS = BASH_FILENAME_QUOTE_CHARACTERS[:-1]

QUOTED = dict((x, '\\'+x) for x in BASH_FILENAME_QUOTE_CHARACTERS)


def backslash_dequote(text, chars=''):
    """Backslash-dequote text."""
    for c in (chars or BASH_FILENAME_QUOTE_CHARACTERS):
        text = text.replace(QUOTED[c], c)
    return text


def backslash_quote(text, chars=''):
    """Backslash-quote text."""
    for c in (chars or completer.filename_quote_characters):
        text = text.replace(c, QUOTED[c])
    return text


def is_fully_quoted(text):
    """Return true if all filename_quote_characters in text
    are backslash-quoted."""
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
    """Return true if the character at index is quoted."""
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


def dequote_string(text, quote_char):
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


def quote_string(text, single_match, quote_char):
    """Return a quoted version of text."""
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


def backslash_quote_string(text, single_match, quote_char):
    """Return a backslash-quoted version of text."""
    if text:
        # If the user has typed a quote character, use it.
        if quote_char:
            text = quote_string(text, single_match, quote_char)
        else:
            text = backslash_quote(text)
    return text

