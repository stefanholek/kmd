from rl import completion
from rl import print_exc


class UsernameCompletion(object):
    """Complete user names."""

    @print_exc
    def __call__(self, text):
        """Return users matching 'text'."""
        return completion.complete_username(text)
