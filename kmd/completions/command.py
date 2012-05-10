"""System command completion."""

import os


class CommandCompletion(object):
    """Complete names of commands on the system PATH."""

    def __init__(self):
        """Configure the readline completer."""

    def __call__(self, text):
        """Return executables matching 'text'.
        Does not include shell built-ins or aliases.
        """
        matches = []
        for dir in os.environ.get('PATH').split(':'):
            dir = os.path.expanduser(dir)
            if os.path.isdir(dir):
                for name in os.listdir(dir):
                    if name.startswith(text):
                        if os.access(os.path.join(dir, name), os.R_OK|os.X_OK):
                            matches.append(name)
        return matches
