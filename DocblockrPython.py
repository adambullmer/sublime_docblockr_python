from .formatters.registry import populate_registry

plugin_is_loaded = False


def plugin_loaded():
    """The Sublime Text 3 entry point for plugins."""
    populate_registry()

    global plugin_is_loaded
    plugin_is_loaded = True
