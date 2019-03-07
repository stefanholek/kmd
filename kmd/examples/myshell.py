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
        """Execute the system cat command"""
        os.system('cat ' + args)

    def complete_cat(self, text, *ignored):
        return self.completefilename(text)

    def do_echo(self, args):
        """Execute the system echo command"""
        os.system('echo ' + args)

    def complete_echo(self, text, *ignored):
        return self.completeenviron(text)

    def help_help(self):
        self.stdout.write('Interactive help\n')

    def emptyline(self):
        pass


def main():
    MyShell().run()


if __name__ == '__main__':
    main()
