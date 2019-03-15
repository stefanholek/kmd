=========================================================
Overview
=========================================================

.. automodule:: kmd

Interpreters
====================

The :class:`kmd.Kmd` class provides a simple framework for writing
line-oriented command interpreters, also known as *shells*. These are often
useful for test harnesses, prototypes, and administrative tools.

A :class:`kmd.Kmd` instance is a line-oriented command interpreter.
There is no good reason to instantiate :class:`kmd.Kmd` itself; rather, it is used as
base class for interpreter classes you define.

Completions
==================

The :mod:`kmd.completions` package defines the *custom completion
protocol* and implements a set of ready-to-use
completions for :class:`kmd.Kmd`.
Applications may use the provided completions and/or add their own,
domain-specific completions based on code in this package.

Quoting
==================

The :mod:`kmd.quoting` module defines constants and functions for writing
custom completions.

Upstream Documentation
======================

The standard library documentation for `cmd.Cmd`_.

.. _`cmd.Cmd`: https://docs.python.org/3/library/cmd.html

The rl_ GNU Readline Bindings.

.. _rl: https://rl.readthedocs.io/en/stable/
