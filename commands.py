"""
DocBlockr Python v1.3.0

Author: Adam Bullmer <adam.bullmer@gmail.com>
Website: https://github.com/adambullmer/sublime-docblockr-python

Credit to `spadgos` and the team at DocBlockr for providing some source code
to support this project
"""
import logging
import sublime
import sublime_plugin
import re

from sublime_docblockr_python.formatters.utils import get_formatter, get_setting
from sublime_docblockr_python.parsers.parser import get_parser

log = logging.getLogger(__name__)


def write(view, string):
    """Writes a string to the view as a snippet.

    Arguments:
        view   {sublime.View} -- view to have content written to
        string {String}       -- String representation of a snippet to be
            written to the view
    """
    view.run_command('insert_snippet', {'contents': string})


def escape(string):
    """Escapes the special characters.

    Escapes characters that are also in snippet tab fields so that inserting into the view
    doesn't accidentally create another tabbable field
    Arguments:
        string {String} -- String to be excaped

    Examples:
        >>> escape('function $test() {}')
        'function \$test() \{\}'

    Returns:
        {String} String with escaped characters
    """
    return string.replace('$', r'\$').replace('{', r'\{').replace('}', r'\}')


class DocblockrPythonCommand(sublime_plugin.TextCommand):
    """Sublime Text Command.

    Command to be run by Sublime Text

    Extends:
        sublime_plugin.TextCommand

    Variables:
        position        {Integer}
        trailing_rgn    {String}
        trailing_string {String}
        settings        {String}
        indent_spaces   {String}
        parser          {Object}
        line            {String}
        contents        {String}
    """
    position = 0
    trailing_rgn = ''
    trailing_string = ''
    settings = ''
    indent_spaces = ''
    parser = object
    line = ''
    contents = ''
    view_settings = None
    project_settings = None

    def run(self, edit):
        """Sublime Command Entrypoint

        Entrypoint for the Sublime Text Command. Outputs the result of the parsing to
        the view.

        Arguments:
            edit {sublime.edit} -- Sublime Edit buffer
        """
        self.initialize(self.view)

        # If this docstring is already closed, then generate a new line
        if self.parser.is_docstring_closed(self.view, self.view.sel()[0].end()) is True:
            write(self.view, '\n')
            return

        self.view.erase(edit, self.trailing_rgn)

        output = self.parser.parse(self.line, self.contents)

        snippet = self.create_snippet(output)
        write(self.view, snippet)

    def initialize(self, view):
        """Setup the command's settings.

        Begins preparsing the file to gather some basic information.
        - Which parser to use
        - Store any trailing characters

        Arguments:
            view {sublime.View} -- The view to be edited
        """
        self.view_settings = view.settings()

        project_data = view.window().project_data() or {}
        self.project_settings = project_data.get('DocblockrPython', {})

        position = view.sel()[0].end()

        # trailing characters are put inside the body of the comment
        self.trailing_rgn = sublime.Region(position, view.line(position).end())
        self.trailing_string = view.substr(self.trailing_rgn).strip()
        # drop trailing '"""'
        self.trailing_string = escape(re.sub(r'\s*"""\s*$', '', self.trailing_string))

        self.parser = parser = get_parser(view)

        # read the previous line
        self.line = parser.get_definition(view, view.line(position).begin() - 1)
        self.contents = parser.get_definition_contents(view, view.line(position).end())
        log.debug('contents -- {}'.format(self.contents))

    def create_snippet(self, parsed_attributes):
        project_formatter = self.project_settings.get('formatter', None)
        formatter = get_formatter(project_formatter or get_setting('formatter'))()

        # Make sure the summary line has the trailing text, or a placeholder
        if not self.trailing_string:
            self.trailing_string = formatter.summary()

        snippet = self.trailing_string + formatter.description()

        for attribute_type, attributes in parsed_attributes:
            if len(attributes) is 0:
                continue

            segment = getattr(formatter, attribute_type)
            snippet += segment(attributes)

        snippet += self.parser.closing_string

        return snippet
