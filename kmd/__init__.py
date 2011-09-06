"""A modern version of cmd.Cmd using rl_ readline bindings.

.. _rl: http://pypi.python.org/pypi/rl

Package Contents
================

kmd exports the following components:

`Kmd`
    Implements the mechanics of a command shell.

`completions`
    Implements a set of ready-to-use completions.

Command Interpreters
====================

The `Kmd` class provides a simple framework for writing line-oriented command
interpreters, also known as shells. These are often useful for test harnesses,
prototypes, and administrative tools.
The main UI feature of shell-type applications is TAB completion.

A Kmd instance is a line-oriented interpreter framework.
There is no good reason to instantiate Kmd itself; rather, it is used as
base class for interpreter classes you define.

Completions
===========

The `completions` package implements all OS-related completions known from
Bash. In addition, it establishes the *custom completion protocol* and
provides utility functions for string and filename quoting.

Upstream Documentation
======================

The standard library documentation for `cmd.Cmd`_.

.. _`cmd.Cmd`: http://docs.python.org/library/cmd.html
"""

from kmd import Kmd
