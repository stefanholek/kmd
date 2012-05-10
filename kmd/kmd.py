"""A base class for custom command interpreters."""

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
from completions.quoting import is_fully_quoted
from completions.quoting import backslash_quote


class Kmd(cmd.Cmd, object):
    """Interpreter base class.

    This is a subclass of the standard library's :class:`cmd.Cmd <py:cmd.Cmd>` class,
    using the new :mod:`rl <rl:rl>` bindings for GNU Readline. The standard
    library documentation applies unless noted otherwise.
    Changes include:

    #. :class:`~kmd.Kmd` is a new-style class.
    #. The :class:`~kmd.Kmd` constructor accepts an additional 'stderr' argument; all error
       messages are printed to 'stderr'.
    #. :meth:`~kmd.Kmd.preloop` and :meth:`~kmd.Kmd.postloop` are no longer stubs but contain important
       code bits. Subclasses must make sure to call their parents' implementations.
    #. New methods: :meth:`~kmd.Kmd.input`, :meth:`~kmd.Kmd.comment`, :meth:`~kmd.Kmd.help`,
       :meth:`~kmd.Kmd.run`, and :meth:`~kmd.Kmd.word_break_hook`.
    #. Incomplete command names are automatically expanded if they are unique.
    #. Command aliases can be defined by overriding :meth:`~kmd.Kmd.__init__` and extending
       the 'aliases' dictionary.
    #. :meth:`help_*` methods optionally receive the help topic as argument.
    #. :meth:`complete_*` methods may return any kind of iterable, not just lists.

    Example::

        import kmd

        class MyShell(kmd.Kmd):
            ...
    """

    prompt = '(Kmd) '
    alias_header = 'Command aliases (type help <topic>):'
    shell_escape_chars = '!'
    history_file = ''
    history_max_entries = -1

    def __init__(self, completekey='TAB', stdin=None, stdout=None, stderr=None):
        """Instantiate a line-oriented interpreter framework.

        The optional argument 'completekey' is the readline name of a
        completion key; it defaults to the TAB key.
        The optional arguments stdin, stdout, and stderr
        specify alternate input and output file objects; if not specified,
        sys.stdin, sys.stdout, and sys.stderr are used.
        """
        super(Kmd, self).__init__(completekey, stdin, stdout)

        if stderr is not None:
            self.stderr = stderr
        else:
            self.stderr = sys.stderr

        self.aliases = {'?': 'help'}
        for char in self.shell_escape_chars:
            self.aliases[char] = 'shell'

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
                            line = self.input(self.prompt)
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
        """Called when the :meth:`~kmd.Kmd.cmdloop` method is entered. Configures the
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
        """Called when the :meth:`~kmd.Kmd.cmdloop` method is exited. Resets the readline
        completer and saves the history file.
        Note that :meth:`~kmd.Kmd.postloop` is called even if :meth:`~kmd.Kmd.cmdloop`
        exits with an exception!
        """
        if self.use_rawinput:
            if self.history_file:
                history.write_file(self.history_file)

            if self.completekey:
                completer.reset()

    def input(self, prompt):
        """Read a line from the keyboard using :func:`raw_input() <py:raw_input>`
        (:func:`input() <py3k:input>` in Python 3).
        When the user presses the TAB key, invoke the readline completer.
        """
        return raw_input(prompt)

    @print_exc
    def complete(self, text, state):
        """complete(text, state)
        Return the next possible completion for 'text'.

        If a command has not been entered, complete against the command list.
        Otherwise try to call complete_<command> to get a list of completions.
        Installed as :attr:`rl.completer.completer <rl:rl.Completer.completer>`.
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
        """word_break_hook(begidx, endidx)
        When completing '?<topic>' make sure '?' is a word break character.
        Ditto for '!<command>'.
        Installed as :attr:`rl.completer.word_break_hook <rl:rl.Completer.word_break_hook>`.
        """
        # This has a flaw as we cannot complete names that contain
        # the new word break character.
        origline = completion.line_buffer
        line = origline.lstrip()
        stripped = len(origline) - len(line)
        if begidx - stripped == 0:
            if line[0] == '?' or line[0] in self.shell_escape_chars:
                if line[0] not in completer.word_break_characters:
                    return line[0] + completer.word_break_characters

    def onecmd(self, line):
        """Interpret a command line.

        This may be overridden, but should not normally need to be;
        see the :meth:`precmd() <py:cmd.Cmd.precmd>` and :meth:`postcmd() <py:cmd.Cmd.postcmd>`
        methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        If there is a do_<command> method for the command prefix, that
        method is called, with the remainder of the line as argument,
        and its return value is returned.
        Otherwise the return value of the :meth:`~kmd.Kmd.default` method
        is returned.
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
                dofunc = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return dofunc(arg)

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments. Returns a tuple containing (command, args, line).
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

    def comment(self, line):
        """Called when the input line starts with a '#'.
        By default clears the lastcmd.
        """
        self.lastcmd = ''

    def default(self, line):
        """Called when the command prefix is not recognized.
        By default prints an error message.
        """
        self.stderr.write('*** Unknown syntax: %s\n' % (line,))

    def do_help(self, topic=''):
        # Print the help screen for 'topic' or the default help.
        if topic:
            try:
                helpfunc = getattr(self, 'help_' + topic)
            except AttributeError:
                try:
                    dofunc = getattr(self, 'do_' + topic)
                except AttributeError:
                    pass
                else:
                    doc = dofunc.__doc__
                    if doc:
                        self.stdout.write("%s\n" % doc)
                        return
                self.stderr.write('%s\n' % (self.nohelp % (topic,)))
            else:
                try:
                    helpfunc(topic)
                except TypeError:
                    helpfunc()
        else:
            self.help()

    def help(self):
        """Called when no help topic is specified.
        Prints the default help screen; empty sections and sections with
        empty headers are omitted.
        """
        names = self.get_names()
        cmds_doc = []
        cmds_undoc = []
        help = {}
        for name in names:
            if name[:5] == 'help_':
                help[name[5:]] = 1
        names.sort()
        prevname = ''
        for name in names:
            if name[:3] == 'do_':
                if name == prevname:
                    continue
                prevname = name
                cmd = name[3:]
                if cmd in help:
                    cmds_doc.append(cmd)
                    del help[cmd]
                elif getattr(self, name).__doc__:
                    cmds_doc.append(cmd)
                else:
                    cmds_undoc.append(cmd)
        self.stdout.write("%s\n" % self.doc_leader)
        if self.doc_header:
            self.print_topics(self.doc_header, cmds_doc, 15, 80)
        if self.alias_header:
            self.print_topics(self.alias_header, sorted(self.aliases), 15, 80)
        if self.misc_header:
            self.print_topics(self.misc_header, sorted(help), 15, 80)
        if self.undoc_header:
            self.print_topics(self.undoc_header, cmds_undoc, 15, 80)

    def run(self, args=None):
        """Run the Kmd.

        If 'args' is None, it defaults to sys.argv[1:].
        """
        if args is None:
            args = sys.argv[1:]

        if args:
            line = self.rejoin(args)
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

    def rejoin(self, args):
        """Rejoin command line arguments."""
        completer.filename_quote_characters = FILENAME_QUOTE_CHARACTERS
        line = []
        for arg in args:
            if not is_fully_quoted(arg):
                arg = backslash_quote(arg)
            line.append(arg)
        return ' '.join(line)

    def __getattr__(self, name):
        """Expand aliases and incomplete command names."""
        if name[:3] == 'do_':
            prefix, cmd = name[:3], name[3:]
        elif name[:9] == 'complete_':
            prefix, cmd = name[:9], name[9:]
        elif name[:5] == 'help_':
            prefix, cmd = name[:5], name[5:]
        else:
            raise AttributeError(name)
        names = self.get_names()
        expanded = prefix + self.aliases.get(cmd, cmd)
        if expanded in names:
            return getattr(self, expanded)
        expanded = set(x for x in names if x.startswith(name))
        if len(expanded) == 1:
            return getattr(self, expanded.pop())
        raise AttributeError(name)


def main(args=None):
    shell = Kmd()
    return shell.run(args)


if __name__ == '__main__':
    sys.exit(main())

