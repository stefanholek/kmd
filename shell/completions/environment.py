import os

from rl import completer
from rl import print_exc


class EnvironmentCompletion(object):
    """Complete environment variables."""

    def __init__(self):
        """Configure the completer for environment variable completion."""
        if '$' not in completer.word_break_characters:
            completer.word_break_characters += '$'
        if '$' not in completer.special_prefixes:
            completer.special_prefixes += '$'

    @print_exc
    def __call__(self, text):
        """Return environment variables matching 'text'."""
        if text[0] == '$':
            text = text[1:]
        return ['$'+x for x in os.environ if x.startswith(text)]
