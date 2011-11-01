"""Host name completion."""

import os

from rl import completer


class HostnameCompletion(object):
    """Complete host names found in the system's hosts file."""

    def __init__(self, hostsfile='/etc/hosts'):
        """Configure the readline completer.
        """
        self.hostsfile = hostsfile

        if '@' not in completer.word_break_characters:
            completer.word_break_characters += '@'
        if '@' not in completer.special_prefixes:
            completer.special_prefixes += '@'

    def __call__(self, text):
        """Return host names matching 'text'.

        Host names are returned with a leading '@' character.
        The search string may start with an '@' character which is
        stripped before matching.
        """
        if text[0] == '@':
            text = text[1:]
        return ['@'+x for x in self.read_hostnames() if x.startswith(text)]

    def read_hostnames(self):
        """Read host names from the hosts file."""
        if os.path.isfile(self.hostsfile):
            f = open(self.hostsfile, 'rt')
            lines = f.readlines()
            f.close()

            for line in lines:
                line = line.split()
                if line and not line[0].startswith('#'):
                    for hostname in line[1:]:
                        yield hostname
