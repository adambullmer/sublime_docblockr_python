import importlib

import sublime

from docblockr_python.formatters.registry import registry

plugin_is_loaded = False

def get_formatter(formatter):
    try:
        temp = importlib.import_module('docblockr_python.formatters.{}'.format(formatter))
        Formatter = getattr(temp, '{}Formatter'.format(formatter.capitalize()))
        return Formatter
    except ImportError as exception:
        print(exception)
    except AttributeError as exception:
        raise ValueError('Formatter {} doesn\'t exist'.format(formatter)) from exception


def get_setting(key, default=None):
    """Gets the passed setting from the aggregated settings files.

    Merges up settings as specified in Sublime's docs.
    https://www.sublimetext.com/docs/3/settings.html

    Arguments:
        key {str} -- String of the key to get

    Keyword Arguments:
        default {str} -- default value in case the setting is not found (default: None)

    Returns:
        {str} or {None} -- value of the setting
    """
    settings = sublime.load_settings('DocblockrPython.sublime-settings')
    os_specific_settings = {}

    os_name = sublime.platform()
    if os_name == 'osx':
        os_specific_settings = sublime.load_settings('DocblockrPython (OSX).sublime-settings')
    elif os_name == 'windows':
        os_specific_settings = sublime.load_settings('DocblockrPython (Windows).sublime-settings')
    else:
        os_specific_settings = sublime.load_settings('DocblockrPython (Linux).sublime-settings')

    return os_specific_settings.get(key, settings.get(key, default))


def plugin_loaded():
    """The ST3 entry point for plugins."""
    global plugin_is_loaded
    plugin_is_loaded = True

    window = sublime.active_window()
