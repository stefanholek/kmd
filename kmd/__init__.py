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

The :mod:`kmd.completions` package implements all OS-related completions known
from Bash. In addition, it establishes the *custom completion protocol* and
provides utility functions for string and filename quoting.

Applications are encouraged to add their own, domain-specific
completions based on code in this package.
"""

from kmd import Kmd
