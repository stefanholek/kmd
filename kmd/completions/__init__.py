"""A set of completions for use with kmd.Kmd.

Completion Protocol
===================

A *custom completion* is a class that implements at least two methods:

.. method:: Completion.__init__()

    Initializes the completion and configures the readline completer
    for the type of completion instantiated. May accept additional
    arguments.

.. method:: Completion.__call__(text)

    Returns an iterable of matches for 'text'.
"""
