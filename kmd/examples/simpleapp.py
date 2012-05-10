"""Complete system commands and filenames on the same line."""

import os
import kmd

from kmd.completions.command import CommandCompletion
from kmd.completions.filename import FilenameCompletion


class SimpleApp(kmd.Kmd):

    intro = 'Completion example (type Ctrl+D to exit)\n'
    prompt = 'simpleapp> '

    def preloop(self):
        """Set up completions."""
        super(SimpleApp, self).preloop()
        self.completecommand = CommandCompletion()
        self.completefilename = FilenameCompletion()

    def emptyline(self):
        """Do nothing."""

    def do_EOF(self, args):
        """Usage: Ctrl+D"""
        self.stdout.write('\n')
        return True

    def do_shell(self, args):
        """Usage: !<command> [<filename> ...]"""
        os.system(args)

    def complete_shell(self, text, line, begidx, endidx):
        """Complete shell commands.

        This function is called when the command line starts with
        an exclamation mark. It further dispatches to command or
        filename completion, depending on position and format of
        the completion word.
        """
        if line[0:begidx].strip() in ('!', 'shell'):
            if not text.startswith('~') and os.sep not in text:
                return self.completecommand(text)
        return self.completefilename(text)


def main():
    SimpleApp().run()


if __name__ == '__main__':
    main()
