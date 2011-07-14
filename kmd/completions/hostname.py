import os

from rl import completer
from rl import print_exc


class HostnameCompletion(object):
    """Complete host names found in /etc/hosts."""

    def __init__(self, hostsfile):
        """Configure the completer for host name completion."""
        self.hostsfile = hostsfile

        if '@' not in completer.word_break_characters:
            completer.word_break_characters += '@'
        if '@' not in completer.special_prefixes:
            completer.special_prefixes += '@'

    @print_exc
    def __call__(self, text):
        """Return host names matching 'text'."""
        if text[0] == '@':
            text = text[1:]
        return ['@'+x for x in self.get_hostnames() if x.startswith(text)]

    def get_hostnames(self):
        """Read host names from the hosts file."""
        f = open(self.hostsfile, 'rt')
        lines = f.readlines()
        f.close()

        for line in lines:
            line = line.split()
            if line and not line[0].startswith('#'):
                for hostname in line[1:]:
                    yield hostname
