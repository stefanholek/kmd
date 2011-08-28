"""A set of completions for use with kmd.Kmd.

Package Contents
================

`CommandCompletion`
    Complete names of commands on the system PATH.

`EnvironmentCompletion`
    Complete names of variables in the process environment.

`FilenameCompletion`
    Complete file and directory names.

`HostnameCompletion`
    Complete host names found in ``/etc/hosts``.

`UsernameCompletion`
    Complete user names.

`quoting`
    String quoting and dequoting support.

`filename`
    Filename quoting and dequoting support.

Custom Completions
==================

A *custom completion* is a class that implements at least two methods:

``__init__(self)``
    Initializes the completion and configures the readline completer
    for the type of completion instantiated. May accept additional arguments
    if the completion is configurable.

``__call__(self, text)``
    Returns an iterable of matches for ``text``.
"""
