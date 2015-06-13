"""
|||
"""
import sublime, sublime_plugin
import re

def write(view, string):
    """
    |||
    """
    view.run_command('insert_snippet', {'contents': string})

def get_parser(view):
    """Returns the class of the parser to use.

    Args:
        view - The sublime text view in which this is executing in
    Returns:
        class PythonParser if the current file type isn't a python file
    """
    scope = view.scope_name(view.sel()[0].end())
    res = re.search(r'\bsource\.([a-z+\-]+)', scope)
    source_lang = res.group(1) if res else 'js'
    view_settings = view.settings()

    if source_lang == "python":
        return PythonParser(view_settings)

    return None

def split_by_commas(string):
    """
    Split a string by unenclosed commas: that is, commas which are not inside of quotes or
    brackets.

    >>> split_by_commas('foo, bar(baz, quux), fwip = "hey, hi"')
    ['foo', 'bar(baz, quux)', 'fwip = "hey, hi"']
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
    """
    |||
    """
    return string.replace('$', r'\$').replace('{', r'\{').replace('}', r'\}')

def counter():
    """
    |||
    """
    count = 0
    while True:
        count += 1
        yield count

class DocblockrPythonCommand(sublime_plugin.TextCommand):
    """
    |||
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
        """
        |||
        """
        self.initialize(self.view)
        self.view.erase(edit, self.trailing_rgn)

        output = self.parser.parse(self.line, self.contents)

        snippet = self.create_snippet(output)
        write(self.view, snippet)

    def initialize(self, view):
        """
        |||
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
        """
        |||
        """

        tab_index = counter()

        # Make sure the summary line has the trailing text, or a placeholder
        if not self.trailing_string:
            self.trailing_string = '${' + str(next(tab_index)) + ':[summary]}'

        snippet = self.trailing_string + '\n\n${' + str(next(tab_index)) + ':[description]}\n'

        for attribute_type, attributes in parsed_attributes.items():
            if len(attributes) is 0:
                continue

            if attribute_type is 'arguments':
                snippet += 'Arguments:\n'
                for attribute in attributes:
                    snippet += '\t@arg ' + attribute
                    snippet += ' ${' + str(next(tab_index)) + ':[description]}\n'
            elif attribute_type is 'keyword_arguments':
                snippet += 'Keyword Arguments:\n'
                for attribute in attributes:
                    snippet += '\t@kwarg ' + attribute
                    snippet += '${' + str(next(tab_index)) + ':[description]}'
                    snippet += ' (default ${' + str(next(tab_index)) + '})\n'
            elif attribute_type is 'returns':
                returns_snippet = ''
                if isinstance(attribute, {}):
                    returns_snippet += '${' + str(next(tab_index)) + ':[type]}'
                else:
                    returns_snippet += attribute

                returns_snippet += ' ${' + str(next(tab_index)) + ':[description]}'

                snippet += 'Returns:\n\t' + returns_snippet + '\n'
            elif attribute_type is 'extends':
                for attribute in attributes:
                    snippet += '@extends ' + attribute + '\n'
            elif attribute_type is 'variables':
                snippet += 'Variables:\n'
                for attribute in attributes:
                    snippet += '\t@var ' + attribute
                    snippet += ' ${' + str(next(tab_index)) + ':[type]}'
                    snippet += ' ${' + str(next(tab_index)) + ':[description]}\n'

        snippet += self.parser.closing_string

        return snippet


class PythonParser(object):
    """
    |||
    """
    closing_string = '"""'

    def __init__(self, view_settings):
        pass

    @classmethod
    def get_definition(cls, view, position):
        """
        |||
        """
        # At beginning of the module
        if position is 0:
            return None

        return view.substr(view.line(view.line(position - 1)))

    @classmethod
    def get_definition_contents(cls, view, position):
        """
        |||
        """
        pass

    @classmethod
    def get_next_line(cls, view, position):
        """
        |||
        """
        return view.line(view.line(position).end() + 1)

    def parse(self, line, contents):
        """
        |||
        """
        # At beginning of the module
        if not line:
            return ''

        output = self.parse_class(line, contents)
        if output is not None:
            return output

        output = self.parse_function(line, contents)
        if output is not None:
            return output

        return {}

    def parse_module(self, line, contents):
        """
        |||
        """
        pass

    @classmethod
    def parse_class(cls, line, contents):
        """
        |||
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
        """
        |||
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

            if argument_type not in parsed_function:
                parsed_function[argument_type] = []

            parsed_function[argument_type].append(argument)

        # todo: Attempt to parse return/yield and data type
        parsed_function['returns'] = {}

        return parsed_function
