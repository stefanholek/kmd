"""Environment variable completion."""

import os

from rl import completer


class EnvironmentCompletion(object):
    """Complete names of variables in the process environment."""

    def __init__(self):
        """Configure the readline completer.
        """
        if '$' not in completer.word_break_characters:
            completer.word_break_characters += '$'
        if '$' not in completer.special_prefixes:
            completer.special_prefixes += '$'

    def __call__(self, text):
        """Return environment variables matching 'text'.

        Variable names are returned with a leading '$' character.
        The search string may start with a '$' character which is
        stripped before matching.
        """
        if text[0] == '$':
            text = text[1:]
        return ['$'+x for x in os.environ if x.startswith(text)]
