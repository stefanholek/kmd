"""A version of cmd.Cmd using rl readline bindings."""

import sys
import cmd

from rl import completer
from rl import completion
from rl import history
from rl import print_exc

from completions.quoting import QUOTE_CHARACTERS
from completions.quoting import WORD_BREAK_CHARACTERS
from completions.quoting import FILENAME_QUOTE_CHARACTERS
from completions.quoting import char_is_quoted


class Kmd(cmd.Cmd, object):
    """A cmd.Cmd subclass using rl readline bindings.

    This is a subclass of the standard library's `cmd.Cmd`_
    class using the rl bindings for GNU readline. The standard
    library documentation applies. Applications must use
    this base class instead of `cmd.Cmd`_ to use rl features.

    Example::

        from shell import shell

        class MyShell(kmd.Kmd):
            ...

    .. _`cmd.Cmd`: http://docs.python.org/library/cmd.html
    """

    prompt = '(Kmd) '
    shell_escape_chars = '!'
    history_file = ''
    history_max_entries = -1

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        """Instantiate a line-oriented interpreter framework.

        The optional argument 'completekey' is the readline name of a
        completion key; it defaults to the Tab key. If completekey is
        not None and the rl module is available, command completion
        is done automatically. The optional arguments stdin and stdout
        specify alternate input and output file objects; if not specified,
        sys.stdin and sys.stdout are used.
        """
        super(Kmd, self).__init__(completekey, stdin, stdout)

    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.
        """
        self.preloop()
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro)+"\n")
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            line = raw_input(self.prompt)
                        except EOFError:
                            line = 'EOF'
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        line = self.stdin.readline()
                        if not len(line):
                            line = 'EOF'
                        else:
                            line = line.rstrip('\r\n')
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
        finally:
            self.postloop()

    def preloop(self):
        """Called when the cmdloop() method is entered. Configures the
        readline completer and loads the history file.
        """
        if self.use_rawinput:
            history.max_entries = self.history_max_entries

            if self.history_file:
                history.read_file(self.history_file)

            if self.completekey:
                completer.reset()
                completer.quote_characters = QUOTE_CHARACTERS
                completer.word_break_characters = WORD_BREAK_CHARACTERS
                completer.filename_quote_characters = FILENAME_QUOTE_CHARACTERS
                completer.char_is_quoted_function = char_is_quoted
                completer.word_break_hook = self.word_break_hook
                completer.completer = self.complete
                completer.parse_and_bind(self.completekey+': complete')

    def postloop(self):
        """Called when the cmdloop() method is exited. Disables the readline
        completer and saves the history file.
        """
        if self.use_rawinput:
            if self.history_file:
                history.write_file(self.history_file)

            if self.completekey:
                completer.reset()

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.
        """
        line = line.strip()
        if not line:
            return None, None, line
        elif line[0] == '#':
            return None, None, line
        elif line[0] == '?':
            line = 'help ' + line[1:]
        elif line[0] in self.shell_escape_chars:
            if hasattr(self, 'do_shell'):
                line = 'shell ' + line[1:]
            else:
                return None, None, line
        i, n = 0, len(line)
        while i < n and line[i] in self.identchars:
            i = i+1
        cmd, arg = line[:i], line[i:].strip()
        return cmd, arg, line

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.
        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if line[0] == '#':
            return self.comment(line)
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg)

    def comment(self, line):
        """Called when the input line starts with a '#'."""
        self.lastcmd = ''

    @print_exc
    def complete(self, text, state):
        """Return the next possible completion for 'text'.

        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """
        if state == 0:
            origline = completion.line_buffer
            line = origline.lstrip()
            stripped = len(origline) - len(line)
            begidx = completion.begidx - stripped
            endidx = completion.endidx - stripped
            if begidx == 0:
                compfunc = self.completenames
            else:
                cmd, arg, foo = self.parseline(line)
                if cmd == '':
                    compfunc = self.completedefault
                else:
                    try:
                        compfunc = getattr(self, 'complete_' + cmd)
                    except AttributeError:
                        compfunc = self.completedefault
            self.completion_matches = iter(compfunc(text, line, begidx, endidx))
        try:
            return self.completion_matches.next()
        except StopIteration:
            return None

    @print_exc
    def word_break_hook(self, begidx, endidx):
        """When completing '?<topic>' make '?' a word break character.

        Ditto for '!<command>'. This has a flaw as we cannot complete names
        that contain the new word break character.
        """
        origline = completion.line_buffer
        line = origline.lstrip()
        stripped = len(origline) - len(line)
        if begidx - stripped == 0:
            if line[0] == '?' or line[0] in self.shell_escape_chars:
                if line[0] not in completer.word_break_characters:
                    return line[0] + completer.word_break_characters

    def __getattr__(self, name):
        """Expand unique command prefixes."""
        if name.startswith(('do_', 'complete_', 'help_')):
            matches = set(x for x in self.get_names() if x.startswith(name))
            if len(matches) == 1:
                return getattr(self, matches.pop())
        raise AttributeError(name)

    def run(self, args=None):
        """Run the Kmd."""
        if args is None:
            args = sys.argv[1:]

        if args:
            line = ' '.join(args)
            line = self.precmd(line)
            stop = self.onecmd(line)
            self.postcmd(stop, line)
        else:
            try:
                self.cmdloop()
            except KeyboardInterrupt:
                self.stdout.write('\n')
                return 1
        return 0


def main(args=None):
    shell = Kmd()
    return shell.run(args)

