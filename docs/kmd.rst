=========================
Interpreters
=========================

.. automodule:: kmd.kmd

Kmd Class
=========

.. autoclass:: kmd.Kmd

.. attribute:: Kmd.aliases

    Dictionary mapping command short-cuts to their respective long forms.
    Instance variable.

.. autoattribute:: kmd.Kmd.alias_header

    Header for the aliases section of the default help screen.
    If set to the empty string, the aliases section is omitted.

.. autoattribute:: kmd.Kmd.help_escape_chars

    Special, single-character aliases for :meth:`do_help`.

.. autoattribute:: kmd.Kmd.shell_escape_chars

    Special, single-character aliases for :meth:`do_shell`.

.. autoattribute:: kmd.Kmd.history_file

    If a history filename is set, Kmd loads and saves the history in
    :meth:`~kmd.Kmd.preloop` and :meth:`~kmd.Kmd.postloop`.

.. autoattribute:: kmd.Kmd.history_max_entries

    A positive integer value limits the history size.

.. automethod:: kmd.Kmd.cmdloop
.. automethod:: kmd.Kmd.preloop
.. automethod:: kmd.Kmd.postloop
.. automethod:: kmd.Kmd.input
.. automethod:: kmd.Kmd.word_break_hook
.. automethod:: kmd.Kmd.complete
.. automethod:: kmd.Kmd.onecmd
.. automethod:: kmd.Kmd.parseline
.. automethod:: kmd.Kmd.emptyline
.. automethod:: kmd.Kmd.comment
.. automethod:: kmd.Kmd.default

.. automethod:: kmd.Kmd.do_help

    Print the help screen for 'topic'.

    If there is a help_<topic> method for the help topic, that method is called
    with the (unexpanded) topic as argument. Otherwise, and if 'topic' is a command,
    the docstring of the corresponding do_<command> method is used.
    If 'topic' is empty, the :meth:`~kmd.Kmd.help` method is invoked.

.. automethod:: kmd.Kmd.help
.. automethod:: kmd.Kmd.run
