"""User name completion."""

from rl import completion
from rl import print_exc


class UsernameCompletion(object):
    """Complete user names.

    User names are returned without decoration.
    """

    def __init__(self):
        """Configure the readline completer for user name completion."""

    @print_exc
    def __call__(self, text):
        """__call__(self, text)
        Return user names matching 'text'.
        The search string may start with a '~' character.
        """
        return completion.complete_username(text)
