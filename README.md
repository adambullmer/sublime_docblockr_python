DocBlockr for Python
====================
Based off the [DocBlockr](https://github.com/spadgos/sublime-jsdocs) project, This extension provides the similar funtionality but for python docstrings.
This plugin is designed around [PEP-257](https://www.python.org/dev/peps/pep-0257/) compliance and takes from [Google's styleguide](https://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Comments).
The main goal of this project is to help developer provide better documentation by giving easy and consistent formatting.

Installation
------------
Manually
1. Go to the [Latest Release](https://github.com/adambullmer/sublime-docblockr-python/releases/latest) and download the `DocString.Python.sublime-package` file.
2. Move this file to your `Installed Packages` directory. (`Preferences > Browse Packages...` and go up one directory to see `Installed Packages`)

Usage
-----
There isn't a key command to start this plugin, it is triggerg by hitting **enter** or **tab** after opening a docstring (`"""`) at the `module`, `class`, or `function` level.


Known Issues
------------
- Only detects closed docstring if it is on a line of the same indentation, and has no text in front of it. Single Line docstrings are converted to block

Roadmap
-------
- Process module or class variables
- Process Decorators
- Determine / Guess at variable and return value types
- `Raises` section of documentation
- `Decorators` section of documentation
- Unit Tests!
- More completions!
- Better README
