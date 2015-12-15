import logging
import sublime
import importlib

from .registry import REGISTRY

log = logging.getLogger(__name__)


def get_formatter(name):
    """Returns the requested formatter by name from the registry.

    Attempts to get the requested formatter from the registry. If it doesn't
    exist, the base formatter BaseFormatter will be used instead.

    Arguments:
        name {str} -- Friendly name of the formatter to search

    Returns:
        formatters.base.Base -- Instance of the Base formatter
    """
    formatter = REGISTRY.get(name, None)

    if formatter is None:
        log.warning('Formatter {} doesn\'t exist. Defaulting to Base formatter.'.format(name))
        temp = importlib.import_module('DocBlockr_Python.formatters.base')
        formatter = getattr(temp, 'BaseFormatter')

    return formatter


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
