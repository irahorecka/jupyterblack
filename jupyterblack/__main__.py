import os
import sys

# jupyterblack imports
from jupyterblack import cout
from jupyterblack import parser


def main():
    """Read jupyterblack CLI arguments"""

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    # Show help message
    if "-h" in opts or "--help" in opts:
        print(__doc__)
        return
    # Set default and check for input line length
    line_length = 88
    if "-l" in opts or "--line_length" in opts:
        try:
            line_length = int(args[0])
            args = args[1:]
        except ValueError:
            cout.invalid_linecount()
            return

    # Determine if args present
    try:
        jupyter_filename = args[0]
    except IndexError:
        cout.no_args()
        return
    # Check if input filename exists and has .ipynb extension
    for filename in args:
        if not os.path.exists(filename):
            cout.invalid_filename(filename)
            return
        if not parser.check_ipynb_extension(filename):
            cout.invalid_extension(filename)
            return

    # Blackify .ipynb files
    for jupyter_filename in args:
        jupyter_raw = parser.open_jupyter(jupyter_filename)
        jupyter_black = parser.parse_jupyter(jupyter_raw, line_length=line_length)
        parser.write_jupyter(jupyter_black, jupyter_filename)

    print("All done!")


if __name__ == "__main__":
    main()
