"""A cmd.Cmd replacement using rl_ readline bindings.

.. _rl: http://pypi.python.org/pypi/rl

Package Contents
================

kmd exports the following components:

`Kmd`
    Implements the mechanics of a command shell. Used as a base class
    for custom command interpreters.

`completions`
    Implements a set of ready-to-use completions.

Command Interpreters
====================

The `Kmd` class provides a simple framework for writing line-oriented command
interpreters. These are often useful for test harnesses, administrative
tools, and prototypes that will later be wrapped in a more sophisticated
interface.

A Kmd instance is a line-oriented interpreter framework.
There is no good reason to instantiate Kmd itself; rather, it is useful as a
base class for an interpreter class you define in order to inherit
Kmd's methods and encapsulate your own action methods.

Completions
===========

The `completions` package implements all OS-related completions present in
Bash. In addition, it establishes the *custom completion protocol* and
provides utility functions for string and filename quoting.

Upstream Documentation
======================

The standard library documentation for `cmd.Cmd`_.

.. _`cmd.Cmd`: http://docs.python.org/library/cmd.html
"""

from kmd import Kmd
