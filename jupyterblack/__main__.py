"""Black format your Jupyter Notebook and JupyterLab. Files must have a .ipynb extension.

Usage:
------

    $ jblack [options] [filename] [filename...]

Format one Jupyter file:

    $ jblack notebook.ipynb

Format multiple Jupyter files:

    $ jblack notebook_1.ipynb notebook_2.ipynb [...]

Format one Jupyter file with a line length of 70:

    $ jblack -l 70 notebook.ipynb


Available options are:

    [-h, --help]                  Show help
    [-l, --line_length] <int>     Set max line length to <int>
"""
import os
import sys
from typing import List

from jupyterblack import cout, parser
from jupyterblack.parser import BlackFileModeKwargs
from jupyterblack.util.targets import targets_to_files


def main():
    """Read jupyterblack CLI arguments."""
    run(sys.argv[1:])


def run(passed_args: List[str]) -> None:
    args = [arg for arg in passed_args[1:] if not arg.startswith("-")]
    opts = [opt for opt in passed_args[1:] if opt.startswith("-")]

    # Sanity check_jupyter_file -- don't allow invalid options
    valid_options = ["-h", "--help", "-l", "--line_length"]
    if any(opt not in valid_options for opt in opts):
        cout.invalid_options()
        return

    # Show help message
    if "-h" in opts or "--help" in opts:
        print(__doc__)
        return
    # Set default line length and check_jupyter_file for input value
    line_length = 88
    if "-l" in opts or "--line_length" in opts:
        try:
            line_length = int(args.pop(0))
            if not args:
                raise IndexError
        except ValueError:
            cout.invalid_linelength()
            return
        except IndexError:
            cout.no_args()
            return

    if not args:
        cout.no_args()
        return
    # Check if input filename exists and has .ipynb extension
    for target in args:
        if not os.path.exists(target):
            cout.invalid_filename(target)
            return

    target_files = targets_to_files(args)
    for file in target_files:
        if not parser.check_ipynb_extension(file):
            cout.invalid_extension(file)
            return

    # Black format .ipynb files
    for ipynb_filename in target_files:
        jupyter_content = parser.read_jupyter_file(ipynb_filename)
        jupyter_black = parser.format_jupyter_file(
            jupyter_content,
            BlackFileModeKwargs(line_length=line_length, string_normalization=True),
        )
        parser.write_jupyter_file(jupyter_black, ipynb_filename)

    print("All done!")


if __name__ == "__main__":
    main()
