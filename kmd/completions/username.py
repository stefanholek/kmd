"""User name completion."""

from rl import completion


class UsernameCompletion(object):
    """Complete user names."""

    def __init__(self):
        """Configure the readline completer."""

    def __call__(self, text):
        """Return user names matching 'text'.

        User names are returned without decoration.
        The search string may start with a '~' character, in which case
        the users' home directories are returned instead.
        Home directories start with a '~' and end with a '/' character.
        """
        return completion.complete_username(text)
