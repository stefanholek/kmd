=====
shell
=====
------------------------------------------------------
A modern version of cmd.Cmd using rl readline bindings
------------------------------------------------------

Introduction
============

**shell** allows to easily build command line driven shells
with powerful TAB-completion capabilities.

The shell.Shell class derives from `cmd.Cmd`_ and modifies it in the
following ways:

1. Instead of Python's readline_ module, shell.Shell uses the alternative
   rl_ readline bindings.

2. Setup and tear-down of the readline completer have been moved to *preloop*
   and *postloop* respectively. Subclasses must now make sure to call their
   parent's implementations.

3. Lines starting with '#' are treated as comments. The new *comment* method
   is invoked, passing the line as argument. By default this method clears the
   *lastcmd*.

4. Incomplete command names are automatically expanded given they are unique.

5. It is now possible to configure the *shell_escape_characters*.
   The default set is '!'.

6. If a *history_file* is configured, shell.Shell loads and saves the history
   during *preloop* and *postloop*.

7. The new *run* method encapsulates execution of a shell.Shell.

.. _`cmd.Cmd`: http://docs.python.org/library/cmd.html
.. _readline: http://docs.python.org/library/readline.html

Package Contents
----------------

shell.Shell
    Implements the mechanics of a command shell, similar to cmd.Cmd.

shell.completions
    Implements a set of ready-to-use completions.

Completions
-----------

FilenameCompletion
    Complete file and directory names.

UsernameCompletion
    Complete user names.

EnvironmentCompletion
    Complete environment variables.

CommandCompletion
    Complete system commands.

Example Code
------------
::

    import os
    import shell

    from shell.completions.filename import FilenameCompletion
    from shell.completions.environment import EnvironmentCompletion

    class MyShell(shell.Shell):

        def preloop(self):
            super(MyShell, self).preloop()
            self.completefilename = FilenameCompletion()
            self.completeenviron = EnvironmentCompletion()

        def do_echo(self, args):
            os.system('echo ' + args)

        def complete_echo(self, text, line, begidx, endidx):
            return self.completeenviron(text)

        def do_cat(self, args):
            os.system('cat ' + args)

        def complete_cat(self, text, line, begidx, endidx):
            return self.completefilename(text)

    def main():
        MyShell().run()

Also see gpgkeys_, a front-end for GnuPG built entirely around tab completion.

.. _gpgkeys: http://pypi.python.org/pypi/gpgkeys

Repository Access
-----------------

shell development is hosted on github_.

.. _github: http://github.com/stefanholek/shell

Installation
============

shell uses the rl_ library. Since rl_ contains a C extension, it is
a good idea to review its `installation instructions`_ and make sure
all dependencies are in place.

To install the ``shell`` package, type::

    easy_install shell

.. _rl: http://pypi.python.org/pypi/rl
.. _`installation instructions`: http://pypi.python.org/pypi/rl#installation
