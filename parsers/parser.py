import logging
import re

from DocBlockr import jsdocs

log = logging.getLogger(__name__)

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
        next_line = current_line.begin() if reverse else current_line.end()
        next_line += modifier

        # Ensure within bounds of the view
        if not (next_line < view.size() and next_line > 0):
            break

        current_line = view.line(next_line)

        yield current_line


class PythonParser:
    """Parser class Specific to Python.

    Contains the relevant parsing configuration to be able to handle Python style
    source files.

    Variables:
        closing_string {String}
    """
    closing_string = '"""'

    def __init__(self, view_settings=None):
        self.view_settings = view_settings

    @classmethod
    def get_definition(self, view, position):
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
        indentation_level = view.indentation_level(position)
        definition = ''
        docstring_type = None

        # Read above the docstring for function/class definition and decorators
        for current_line in read_next_line(view, position, True):
            # Not an empty line
            current_line_string = view.substr(current_line).strip()
            if len(current_line_string) is 0:
                continue

            # Ignore comments
            if re.match(r'^\s*(\#)', current_line_string):
                continue

            # When we move up in scope, stop reading
            current_indentation = view.indentation_level(current_line.end())
            if not current_indentation == indentation_level - 1:
                break

            # Set to module, class, or function
            if docstring_type is None:
                if re.match(r'^\s*(class )', current_line_string):
                    docstring_type = 'class'
                elif re.match(r'^\s*(def )', current_line_string):
                    docstring_type = 'function'
                else:
                    docstring_type = 'module'

            definition = current_line_string + '\n' + definition

        # Read the class/function contents
        for current_line in read_next_line(view, position):
            # Not an empty line
            current_line_string = view.substr(current_line).rstrip()
            if len(current_line_string) is 0:
                continue

            # Remove comments
            if re.match(r'^\s*(\#)', current_line_string):
                continue

            # If this is a module or a class, we only care about the lines on
            # the same indentation level for contextual reasons
            current_indentation = view.indentation_level(current_line.end())
            if not docstring_type == 'function' and not current_indentation == indentation_level:
                continue

            # Still within the same indentation level
            if current_indentation < indentation_level:
                break

            definition += current_line_string + '\n'

        return definition

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
        log.debug('definition_line -- {}'.format(line))
        output = self.process_module(line, contents)
        if output is not None:
            return output

        output = self.process_class(line, contents)
        if output is not None:
            return output

        output = self.process_function(line, contents)
        if output is not None:
            return output

        return {}

    def process_variable(self, variable):
        params = {
            'name': None,
            'type': None,
            'default': None,
        }

        if '=' in variable:
            pieces = variable.split('=')
            variable = pieces[0].strip()
            params['default'] = pieces[1].strip()

        params['name'] = variable
        params['type'] = self.guess_type_from_value(params['default']) or self.guess_type_from_name(variable)

        return params

    def parse_variables(self, contents):
        variables = []
        contents + '\n'
        regex = re.compile(r'^\s*((?:(?!from |import |def |class |@).)+$)', re.MULTILINE)
        matches = re.findall(regex, contents)

        if len(matches) == 0:
            return None

        for match in matches:
            variable = self.process_variable(match)
            variables.append(variable)

        return variables

    def process_module(self, line, contents):
        """Parses the whole module file to find module level variables.

        Reads the lines in the module contents to get the names of the module level variables.
        Arguments:
            contents {String} -- Module Body

        Decorators:
            classmethod

        Returns:
            {Dictionary} Dictionary of attributes to create snippets from
        """

        if line is not None:
            return None;

        parsed_module = []
        variables = self.parse_variables(contents)

        if variables is not None:
            parsed_module.append(('variables', variables))

        return parsed_module

    def parse_extends(self, line):
        extends = re.search(r'^\s*class \w*\((.*)\):\s*$', line)

        if not extends:
            return None

        extends = jsdocs.splitByCommas(extends.group(1))
        parsed_extends = []
        for extend in extends:
            if extend == 'object':
                continue

            parsed_extends.append(extend)

        return parsed_extends

    def process_class(self, line, contents):
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
        if not re.match(r'^\s*(class )', line):
            return None

        parsed_class = []

        extends = self.parse_extends(line)
        if extends is not None:
            parsed_class.append(('extends', extends))

        variables = self.parse_variables(contents)
        if variables is not None:
            parsed_class.append(('variables', variables))

        return parsed_class

    def parse_decorators(self, definition, content):
        """Parses the lines above the definition for decorators.

        Finds and returns all the decorators over a function that aren't
        in the excluded list.

        Arguments:
            definition {str} -- definition line.
            content {str} -- Content definition

        Returns:
            {list} -- list of decorators
        """
        lines = content.split('\n')
        excluded_decorators = ['classmethod', 'staticmethod', 'property']
        decorators = []

        for line in lines:
            if line == definition:
                break

            match = re.findall(r'^\s*@([a-zA-Z0-9_\.]*)(\(.*\)|$)', line)

            if len(match) == 0:
                continue

            decorator = match[0][0]
            if decorator in excluded_decorators:
                continue

            decorators.append(decorator)

        return decorators

    def parse_arguments(self, line):
        """Finds and parses each argument and keyword argument.

        Arguments:
            line {str} -- definition line to be parsed

        Returns:
            {dict} -- Contains a list of arguments and a list of
                      keyword arguments in their respective keys.
        """
        parsed_arguments = {
            'arguments': [],
            'keyword_arguments': [],
        }

        arguments = re.search(r'^\s*def \w*\((.*)\):\s*$', line)

        if not arguments:
            return None

        excluded_parameters = ['self', 'cls']
        arguments = jsdocs.splitByCommas(arguments.group(1))

        for argument in arguments:
            if argument in excluded_parameters:
                continue

            argument_type = 'keyword_arguments' if '=' in argument else 'arguments'
            params = self.process_variable(argument)
            parsed_arguments[argument_type].append(params)

        return parsed_arguments

    def parse_returns(self, contents):
        """Finds the first instances of returning in the definition.

        Parses through the whole definition for occurrances of the keyword `return`,
        or `yield` and returns the first. Tries guess the type of the value.

        Arguments:
            contents {str} -- contents of the definition

        Returns:
            {tuple} -- type of return and a dict for the return value type
        """
        regex = re.compile(r'^\s*(return|yield) (\w+)', re.MULTILINE)
        match = re.findall(regex, contents)

        if len(match) == 0:
            return None

        match = match[0]
        return_type = match[0] + 's'
        return_value_type = self.guess_type_from_value(match[1])

        return (return_type, {'type': return_value_type})

    def parse_raises(self, contents):
        """Finds instances of raised exceptions in the definition.

        Parses through the whole definition for occurrances of the keyword `raise`,
        and appends the following value to the list of exceptions to be returned.

        Arguments:
            contents {str} -- contents of the definition

        Returns:
            {list} -- list of exception types
        """
        regex = re.compile(r'^\s*(raise) (\w+)', re.MULTILINE)
        match = re.findall(regex, contents)

        if len(match) == 0:
            return None

        raises = []
        for exception in match:
            raises.append(exception[1])

        return raises

    def process_function(self, line, contents):
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
        if not re.match(r'^\s*(def )', line):
            return None

        parsed_function = []

        decorators = self.parse_decorators(line, contents)
        if len(decorators) > 0:
            parsed_function.append(('decorators', decorators))

        arguments = self.parse_arguments(line)
        if arguments is not None:
            parsed_function.append(('arguments', arguments))

        returns = self.parse_returns(contents)
        if returns is not None:
            parsed_function.append(returns)

        raises = self.parse_raises(contents)
        if raises is not None:
            parsed_function.append(('raises', raises))

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

    def guess_type_from_value(self, value):
        """Make educated assertion about the type of the value.

        Arguments:
            value {str} -- string representation of a value

        Returns:
            {str} -- string of the builtin type or None if one cannot be found
        """
        if value is None:
            return None

        first_char = value[0]

        if jsdocs.is_numeric(value):
            return "number"

        if first_char in ['\"', '\'']:
            return "str"

        if first_char == '[':
            return "list"

        if first_char == '{':
            return "dict"

        if first_char == '(':
            return "tuple"

        if value in ['True', 'False']:
            return 'bool'

        if value[:2] in ["r'", 'r"', "R'", 'R"']:
            return 'regexp'

        if value[:2] in ["u'", 'u"', "U'", 'U"']:
            return 'unicode'

        if value[:7] == 'lambda ':
            return 'function'

        return None

    def guess_type_from_name(self, name):
        """Make an educated guess about the type of a variable based on common naming conventions.

        Arguments:
            name {str} -- variable name

        Returns:
            {str} -- string of the builtin type or None ifone cannot be found
        """
        if re.match("(?:is|has)[A-Z_]", name):
            return 'bool'

        if re.match("^(?:cb|callback|done|next|fn)$", name):
            return 'function'

        return None
