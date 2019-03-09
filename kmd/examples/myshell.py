# A simple shell with two commands

import os
import kmd

from kmd.completions import FilenameCompletion
from kmd.completions import EnvironmentCompletion


class MyShell(kmd.Kmd):

    intro = 'myshell example (type Ctrl+C to exit)\n'
    prompt = 'myshell> '

    def preloop(self):
        super(MyShell, self).preloop()
        self.completefilename = FilenameCompletion()
        self.completeenviron = EnvironmentCompletion()

    def do_cat(self, args):
        """Usage: cat <filename>"""
        os.system('cat ' + args)

    def do_echo(self, args):
        """Usage: echo <varname>"""
        os.system('echo ' + args)

    def complete_cat(self, text, *ignored):
        return self.completefilename(text)

    def complete_echo(self, text, *ignored):
        return self.completeenviron(text)

    def help_help(self):
        self.stdout.write('Usage: help <topic>\n')

    def emptyline(self):
        pass


def main():
    MyShell().run()


if __name__ == '__main__':
    main()
