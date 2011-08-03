"""User name completion."""

from rl import completion
from rl import print_exc


class UsernameCompletion(object):
    """Complete user names."""

    def __init__(self):
        """Configure the readline completer for user name completion."""

    @print_exc
    def __call__(self, text):
        """__call__(self, text)
        Return user names matching 'text'.
        """
        return completion.complete_username(text)
