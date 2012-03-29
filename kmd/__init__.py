"""A modern version of cmd.Cmd using rl_ readline bindings.

.. _rl: http://pypi.python.org/pypi/rl

Command Interpreters
====================

The :class:`kmd.Kmd` class provides a simple framework for writing
line-oriented command interpreters, also known as *shells*. These are often
useful for test harnesses, prototypes, and administrative tools.
The main UI feature of shell-type applications is TAB completion.

A Kmd instance is a line-oriented interpreter framework.
There is no good reason to instantiate Kmd itself; rather, it is used as
base class for interpreter classes you define.

Custom Completions
==================

The :mod:`kmd.completions` package defines the *custom completion
protocol* and, using the protocol, implements a set of ready-to-use
completions for :class:`kmd.Kmd`.

Applications may use the built-in completions and/or add their own,
domain-specific completions based on code in this package.
"""

from kmd import Kmd
