"""DocBlockr for Python.

Author: Adam Bullmer <psycodrumfreak@gmail.com>
Website: https://github.com/adambullmer/sublime-docblockr-python

Credit to `spadgos` and the team at DocBlockr for providing some source code
to support this project
"""
import sublime

from .formatters.registry import populate_registry

plugin_is_loaded = False


def plugin_loaded():
    """The Sublime Text 3 entry point for plugins."""
    populate_registry()

    global plugin_is_loaded
    plugin_is_loaded = True

    sublime.active_window()
