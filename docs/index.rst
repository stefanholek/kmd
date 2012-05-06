=========================================================
:mod:`kmd` -- Interpreter Framework
=========================================================

.. module:: kmd

.. image:: _static/admin_mourning.png

http://xkcd.com/686/

Command Interpreters
====================

The :class:`kmd.Kmd` class provides a simple framework for creating
line-oriented command interpreters, commonly known as *shells*. These are often
useful for test harnesses, prototypes, and administrative tools.
The main UI feature of shell-type applications is TAB completion.

A :class:`~kmd.Kmd` instance is a line-oriented interpreter framework.
There is no good reason to instantiate :class:`~kmd.Kmd` itself; rather, it is used as
base class for interpreter classes you define.

Custom Completions
==================

The :mod:`kmd.completions` package defines the *custom completion*
protocol and, using the protocol, implements a set of ready-to-use
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

