=====
kmd
=====
--------------------------------------------------------
An interpreter framework
--------------------------------------------------------

Introduction
============

**kmd** allows to easily build command line driven shells
with powerful tab-completion capabilities.

The kmd.Kmd class derives from `cmd.Cmd`_ and modifies it in the
following ways:

1. Instead of Python's readline_ module, kmd.Kmd uses the alternative
   rl_ readline bindings.

2. Setup and tear-down of the readline completer have been moved to *preloop*
   and *postloop* respectively. Subclasses must make sure to call their
   parents' implementations.

3. Incomplete command names are automatically expanded if they are unique.

4. Command aliases can be defined by extending the *aliases* dictionary.
   Alias names apply to all *do_*, *complete_*, and *help_* attributes.

5. Lines starting with '#' are treated as comments. The new *comment* method
   is invoked, receiving the line as argument. By default this method clears
   the *lastcmd*.

6. It is now possible to configure the *shell_escape_chars*.
   The default is '!'.

7. If a *history_file* is set, kmd.Kmd loads and saves the history
   in *preloop* and *postloop*. The history size is controlled by setting
   *history_max_entries*.

8. The new *run* method encapsulates the full execution cycle of a Kmd.

.. _`cmd.Cmd`: http://docs.python.org/library/cmd.html
.. _readline: http://docs.python.org/library/readline.html

Package Contents
----------------

kmd.Kmd
    Implements the mechanics of a command shell, similar to `cmd.Cmd`_.

kmd.completions
    Implements a set of ready-to-use completions.

Completions
-----------

FilenameCompletion
    Complete names of files and directories on the filesystem. This is
    the real deal, thanks to rl_ providing access to all the necessary readline
    features.  Includes full quoting support as well as support for decomposed
    UTF-8 on HFS Plus!

UsernameCompletion
    Complete names of users known to the system.

HostnameCompletion
    Complete names of hosts in the system's ``/etc/hosts`` file.

EnvironmentCompletion
    Complete names of variables in the process environment.

CommandCompletion
    Complete names of executables on the system PATH.

Example Code
------------
::

    import os
    import kmd

    from kmd.completions.filename import FilenameCompletion
    from kmd.completions.environment import EnvironmentCompletion

    class MyShell(kmd.Kmd):

        def preloop(self):
            super(MyShell, self).preloop()
            self.completefilename = FilenameCompletion()
            self.completeenviron = EnvironmentCompletion()

        def do_cat(self, args):
            os.system('cat ' + args)

        def complete_cat(self, text, *ignored):
            return self.completefilename(text)

        def do_echo(self, args):
            os.system('echo ' + args)

        def complete_echo(self, text, *ignored):
            return self.completeenviron(text)

    def main():
        MyShell().run()

For further details please refer to the `API Documentation`_.
Also see gpgkeys_, a front-end for GnuPG built entirely around tab completion.

.. _`API Documentation`: http://packages.python.org/kmd
.. _gpgkeys: http://pypi.python.org/pypi/gpgkeys

Development
-----------

kmd development is hosted on GitHub_ where it also has an `issue tracker`_.

.. _GitHub: http://github.com/stefanholek/kmd
.. _`issue tracker`: http://github.com/stefanholek/kmd/issues

Installation
============

Installation requires Python 2.5 or higher.

Note: kmd uses the rl_ library. Since rl contains a C extension, it is a good idea
to review its `installation instructions`_ and make sure all dependencies are
in place.

To install the ``kmd`` package, type::

    easy_install kmd

.. _rl: http://pypi.python.org/pypi/rl
.. _`installation instructions`: http://pypi.python.org/pypi/rl#installation
