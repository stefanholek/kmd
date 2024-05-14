=====
kmd
=====
--------------------------------------------------------
An interpreter framework
--------------------------------------------------------

Overview
============

**kmd** allows to build command line driven shells
with powerful tab-completion capabilities.

The kmd.Kmd class derives from `cmd.Cmd`_ and extends it in the
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
   is invoked, receiving the line as argument.

6. It is now possible to configure the *shell_escape_chars*.
   The default is '!'.

7. If a *history_file* is set, kmd.Kmd loads and saves the history
   in *preloop* and *postloop*.

8. The new *run* method encapsulates the full execution cycle of a Kmd.

.. _`cmd.Cmd`: https://docs.python.org/3/library/cmd.html
.. _readline: https://docs.python.org/3/library/readline.html

Package Contents
================

kmd.Kmd
    Implements the mechanics of a command shell, based on `cmd.Cmd`_.

kmd.completions
    Implements a set of ready-to-use completions.

kmd.quoting
    Defines constants and functions for writing completions.

Documentation
=============

For further details please refer to the `API Documentation`_.

.. _`API Documentation`: https://kmd.readthedocs.io/en/stable/

Development
===========

kmd development is hosted on GitHub_ where it also has an `issue tracker`_.

.. _GitHub: https://github.com/stefanholek/kmd
.. _`issue tracker`: https://github.com/stefanholek/kmd/issues

Installation
============

Installation requires Python 2.7 or higher.

Note: kmd uses the rl_ library which contains a C extension. It is a good idea
to review its `installation instructions`_ and make sure all dependencies are
in place.

To install the ``kmd`` package, type::

    pip install kmd

.. _rl: https://github.com/stefanholek/rl
.. _`installation instructions`: https://github.com/stefanholek/rl#installation

