"""
DocBlockr Python v1.0.0

Author: Adam Bullmer <adam.bullmer@gmail.com>
Website: https://github.com/adambullmer/sublime-docblockr-python

Credit to `spadgos` and the team at DocBlockr for providing some source code
to support this project
"""
import sublime
import sublime_plugin
import re

def write(view, string):
    """Writes a string to the view as a snippet.

    Arguments:
        view   {sublime.View} -- view to have content written to
        string {String}       -- String representation of a snippet to be
            written to the view
    """
    view.run_command('insert_snippet', {'contents': string})

def get_parser(view):
    """Returns the class of the parser to use.

    Arguments:
        view {sublime.View} -- The sublime text view in which this is executing in

    Returns:
        {PythonParser} or None if the current file type isn't a python file
    """
    scope = view.scope_name(view.sel()[0].end())
    res = re.search(r'\bsource\.([a-z+\-]+)', scope)
    source_lang = res.group(1) if res else 'js'
    view_settings = view.settings()

    if source_lang == "python":
        return PythonParser(view_settings)

    return None

def split_by_commas(string):
    """Splits a string by unenclosed commas.

    Splits a string by commas that are not inside of:
    - quotes
    - brackets
    Arguments:
        string {String} -- String to be split. Usuall a function parameter
            string

    Examples:
        >>> split_by_commas('foo, bar(baz, quux), fwip = "hey, hi"')
        ['foo', 'bar(baz, quux)', 'fwip = "hey, hi"']

    Returns:
        {list} List of elements in the string that were delimited by commas
    """
    out = []

    if not string:
        return out

    # the current token
    current = ''

    # characters which open a section inside which commas are not separators between different
    # arguments
    open_quotes = '"\'<({'
    # characters which close the section. The position of the character here should match the
    # opening indicator in `open_quotes`
    close_quotes = '"\'>)}'

    matching_quote = ''
    inside_quotes = False
    is_next_literal = False

    for char in string:
        if is_next_literal:  # previous char was a \
            current += char
            is_next_literal = False
        elif inside_quotes:
            if char == '\\':
                is_next_literal = True
            else:
                current += char
                if char == matching_quote:
                    inside_quotes = False
        else:
            if char == ',':
                out.append(current.strip())
                current = ''
            else:
                current += char
                quote_index = open_quotes.find(char)
                if quote_index > -1:
                    matching_quote = close_quotes[quote_index]
                    inside_quotes = True

    out.append(current.strip())
    return out

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

def counter():
    """Simple Iteratable Counter.

    Starting from 0, will continue to give a new counter number every time
    this function is iterated over, or with the use of `next()`
    Yields:
        {Integer} Current Counter Number
    """
    count = 0
    while True:
        count += 1
        yield count

def read_next_line(view, position, reverse=False):
    """Gets the next line of the view.

    From the given position, will expand the region to the current line in the file,
    grab the ending (beginning if reverse) position, and add (subtract if reverse) 1
    to get the next line in the file. Will return False if the next line is either the
    beginning or the end of the file. This function is iteratable to continuously
    provide file lines
    Arguments:
        view     {sublime.View} -- View to be read
        position {Integer}      -- Position in the view

    Keyword Arguments:
        reverse {Bool} -- If false, will read to the end of the file (default False)

    Yields:
        {sublime.Region} Region of the next line.

    Returns:
        {Bool} False when at the beginning or end of the file
    """
    current_line = view.line(position)
    modifier = 1
    if reverse is True:
        modifier = -1

    while True:
        next_line = current_line.end() + modifier

        # Ensure within bounds of the view
        if not (next_line < view.size() and next_line > 0):
            return False

        current_line = view.line(next_line)

        yield current_line

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
        self.settings = view.settings()
        position = view.sel()[0].end()

        # trailing characters are put inside the body of the comment
        self.trailing_rgn = sublime.Region(position, view.line(position).end())
        self.trailing_string = view.substr(self.trailing_rgn).strip()
        # drop trailing '"""'
        self.trailing_string = escape(re.sub(r'\s*"""\s*$', '', self.trailing_string))

        self.parser = parser = get_parser(view)

        # read the previous line
        self.line = parser.get_definition(view, view.line(position).begin() - 1)
        self.contents = parser.get_definition_contents(view, view.line(position).end() + 1)

    def create_snippet(self, parsed_attributes):
        """Converts dictionary of attributes into a snippet string.

        Reads the dictionary of attributes and substitutes their relevant values into
        the snippet templates, returning the resulting concatenated string.
        Arguments:
            parsed_attributes {Dictionary} -- attribute -> value store

        Returns:
            {String} snippet string
        """
        tab_index = counter()

        # Make sure the summary line has the trailing text, or a placeholder
        if not self.trailing_string:
            self.trailing_string = '${' + str(next(tab_index)) + ':[summary]}'

        snippet = self.trailing_string + '\n\n${' + str(next(tab_index)) + ':[description]}\n'

        for attribute_type, attributes in parsed_attributes.items():

            if attribute_type is 'arguments':
                snippet += '\nArguments:\n'
                for attribute in attributes:
                    snippet += '\t' + attribute
                    snippet += ' {${' + str(next(tab_index)) + ':[type]}} --'
                    snippet += ' ${' + str(next(tab_index)) + ':[description]}\n'
            elif attribute_type is 'keyword_arguments':
                snippet += '\nKeyword Arguments:\n'
                for attribute in attributes:
                    snippet += '\t' + attribute
                    snippet += ' {${' + str(next(tab_index)) + ':[type]}} --'
                    snippet += ' ${' + str(next(tab_index)) + ':[description]}'
                    snippet += ' (default ${' + str(next(tab_index)) + '})\n'
            elif attribute_type is 'returns':
                snippet += 'Returns:\n\t'
                try:
                    if attribute and isinstance(attribute, {}):
                        snippet += '${' + str(next(tab_index)) + ':[type]}'
                    else:
                        snippet += attribute
                except:
                    pass
                snippet += ' ${' + str(next(tab_index)) + ':[description]}\n'
            elif attribute_type is 'extends':
                snippet += '\nExtends:\n\t'
                for attribute in attributes:
                    snippet += attribute + '\n'
            elif attribute_type is 'variables':
                snippet += '\nVariables:\n'
                for attribute in attributes:
                    snippet += '\t@var ' + attribute
                    snippet += ' ${' + str(next(tab_index)) + ':[type]}'
                    snippet += ' ${' + str(next(tab_index)) + ':[description]}\n'

        snippet += self.parser.closing_string

        return snippet


class PythonParser(object):
    """Parser class Specific to Python.

    Contains the relevant parsing configuration to be able to handle Python style
    source files.
    Variables:
        closing_string {String}
    """
    closing_string = '"""'

    def __init__(self, view_settings):
        pass

    @classmethod
    def get_definition(cls, view, position):
        """Gets the definition line.

        String representation fo the line above the docstring

        Arguments:
            view {sublime.View} -- The sublime view in which this is executing
            position {Integer} -- Position of the docstring

        Decorators:
            classmethod

        Returns:
            {String} Representation of the definition line
        """
        # At beginning of the module
        if position is 0:
            return None

        return view.substr(view.line(view.line(position - 1)))

    @classmethod
    def get_definition_contents(cls, view, position):
        """Gets the relevant contents of the module/class/function.

        For Modules and Classes, will only provide the lines on the same
        indentation level as the docstring, so that the interpreter is only looking
        at what is possibly relevant. For functions, the whole content of the function
        if returned, since we will be looking for return/yield values, we cannot be
        certain won which indentation that will be made, if at all.

        Arguments:
            view {sublime.View} -- The sublime view in which this is executing
            position {Integer} -- Position the docstring was created on

        Decorators:
            classmethod

        Returns:
            {String} Contents that matter
        """
        pass

    def parse(self, line, contents):
        """Central command to parse the areas above and below the docstring.

        Tries to determine which type of docstring should be created based upon
        whether the parser returns any output

        Arguments:
            line {String} -- Definition Line
            contents {String} -- Contents of the module/class/function

        Returns:
            {Dictionary} Store of attributes and their values
        """
        # At beginning of the module
        if not line:
            return self.parse_module(contents)

        output = self.parse_class(line, contents)
        if output is not None:
            return output

        output = self.parse_function(line, contents)
        if output is not None:
            return output

        return {}

    @classmethod
    def parse_module(self, contents):
        """Parses the whole module file to find module level variables.

        Reads the lines in the module contents to get the names of the module level variables.
        Arguments:
            contents {String} -- Module Body

        Decorators:
            classmethod

        Returns:
            {Dictionary} Dictionary of attributes to create snippets from
        """
        return {}

    @classmethod
    def parse_class(cls, line, contents):
        """Parses a class line to determine its attributes.

        Reads the class line to determine what other classes it extends
        Arguments:
            line     {String} -- Line containing the class definition
            contents {String} -- Class Body

        Decorators:
            classmethod

        Returns:
            {Dictionary} Dictionary of attributes to create snippets from
        """
        parsed_class = {}

        extends = re.search(r'^\s*class \w*\((.*)\):\s*$', line)
        if not extends:
            return None

        extends = split_by_commas(extends.group(1))

        for extend in extends:
            if extend == 'object':
                continue

            if 'extends' not in parsed_class:
                parsed_class['extends'] = []

            parsed_class['extends'].append(extend)

        # todo: Parse Class Variables

        return parsed_class

    @classmethod
    def parse_function(cls, line, contents):
        """Parses a function for its arguments

        Reads the function line to parse out the args and kwargs.
        Arguments:
            line     {String} -- Line containing the function definition
            contents {String} -- Function body

        Decorators:
            classmethod

        Returns:
            {Dictionary} Parsed valued group by type
        """
        parsed_function = {}

        arguments = re.search(r'^\s*def \w*\((.*)\):\s*$', line)
        if not arguments:
            return None

        arguments = split_by_commas(arguments.group(1))

        for argument in arguments:
            argument_type = 'arguments'
            if argument == 'self' or argument == 'cls':
                continue

            if '=' in argument:
                argument_type = 'keyword_arguments'
                argument = argument.split('=')[0].rstrip()

            if argument_type not in parsed_function:
                parsed_function[argument_type] = []

            parsed_function[argument_type].append(argument)

        # todo: Attempt to parse return/yield and data type
        parsed_function['returns'] = {}

        return parsed_function

    def is_docstring_closed(self, view, position):
        """Checks if the current docstring is supposed to be closed.

        Keep reading lines until we reach the end of the file, class, or function
        We will assume that if the indentation level is ever lower than present, and no
        closing docstring has been found yet, the component has ended and needs to be closed

        Arguments:
            view     {sublime.View} -- Current Sublime Text View
            position {Integer}      -- Position in the view where the docstring is

        Returns:
            {Bool} True if the docstring is confirmed closed
        """
        indentation_level = view.indentation_level(position)

        # Check the current line first, and ignore if docstring is closed on this line
        line = view.substr(view.line(position))
        match = re.search(r'^\s*""".*"""\s*$', line)

        if match is not None:
            return False

        for current_line in read_next_line(view, position):
            # Not an empty line
            current_line_string = view.substr(current_line).rstrip()
            if len(current_line_string) is 0:
                continue

            # Not on a more indented line
            current_indentation = view.indentation_level(current_line.end())
            if current_indentation > indentation_level:
                continue

            # Still within the same indentation level
            if current_indentation < indentation_level:
                break

            # Line only contains whitespace and """
            if re.search(r'^\s*"""', current_line_string) is not None:
                return True

        return False
