"""Environment variable completion."""

import os

from rl import completer
from rl import print_exc


class EnvironmentCompletion(object):
    """Complete names of variables in the process environment.

    Variable names are returned with a leading '$' character.
    """

    def __init__(self):
        """Configure the readline completer for environment variable completion."""
        if '$' not in completer.word_break_characters:
            completer.word_break_characters += '$'
        if '$' not in completer.special_prefixes:
            completer.special_prefixes += '$'

    @print_exc
    def __call__(self, text):
        """__call__(self, text)
        Return environment variables matching 'text'.
        The search string may start with a '$' character.
        """
        if text[0] == '$':
            text = text[1:]
        return ['$'+x for x in os.environ if x.startswith(text)]
