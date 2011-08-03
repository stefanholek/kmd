"""A modern version of cmd.Cmd using rl readline bindings.

Package Contents
================

kmd exports these components:

`kmd.Kmd`
    Implements the mechanics of a command shell. Used as a base class
    for custom command interpreters.

`kmd.completions`
    Implements a set of ready-to-use completions.
"""

from kmd import Kmd
