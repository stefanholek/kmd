=========================================================
kmd |version| -- Interpreter Framework
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
protocol* and, using the protocol, implements a set of ready-to-use
completions for :class:`kmd.Kmd`.

Applications may use the built-in completions and/or add their own,
domain-specific completions based on code in this package.

API Documentation
=================

.. toctree::
   :maxdepth: 3

   kmd
   completions
   examples

Upstream Documentation
======================

The standard library documentation for `cmd.Cmd`_.

.. _`cmd.Cmd`: http://docs.python.org/library/cmd.html

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

