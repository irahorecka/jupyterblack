"""
Blackify one or more Jupyter files.
Files must have an .ipynb extension.

Usage:
------

    $ jupyterblack [options] [filename] [filename...]

Format one Jupyter file:

    $ jupyterblack notebook.ipynb

Format multiple Jupyter files:

    $ jupyterblack notebook_1.ipynb notebook_2.ipynb [...]

Format a Jupyter file with line count of 70:

    $ jupyterblack -l 70 notebook.ipynb


Available options are:

    -h, --help                  Show help
    -l, --line_length <int>      Set max line count of size <int>

"""
import json
import os
import sys
import uuid
import safer
from black import format_str, FileMode, InvalidInput
import cout


def open_jupyter(filename):
    """Safely open .ipynb file"""
    with safer.open(filename, "r") as ipynb_infile:
        return ipynb_infile.read()


def parse_jupyter(content, **kwargs):
    """Parse and blackify .ipynb content"""
    content_json = json.loads(content)
    newline_hash = str(uuid.uuid4())

    for cell in content_json["cells"]:
        if cell["cell_type"] == "code":
            blacked_cell_char = [
                char for char in format_black("".join(cell["source"]), **kwargs)
            ]
            blacked_cell = "".join(
                [newline_hash if char == "\n" else char for char in blacked_cell_char]
            )
            cell_lines = blacked_cell.split(newline_hash)
            cell["source"] = [line + "\n" for line in cell_lines[:-1]]

    return content_json


def write_jupyter(content, filename):
    """Write to .ipynb file"""
    with open(filename, "w") as ipynb_outfile:
        ipynb_outfile.write(json.dumps(content))


def format_black(cell_content, **kwargs):
    """Blackify cell content to appropriate line length."""
    line_length = kwargs["line_length"]
    mode = FileMode(line_length=line_length)
    try:
        return format_str(src_contents=cell_content, mode=mode)
    except InvalidInput:
        return cell_content


def check_ipynb_extension(filename):
    """Check .ipynb extension"""
    return bool(filename.endswith(".ipynb"))


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
        if not check_ipynb_extension(filename):
            cout.invalid_extension(filename)
            return

    # Blackify Jupyter files
    for jupyter_filename in args:
        jupyter_raw = open_jupyter(jupyter_filename)
        jupyter_black = parse_jupyter(jupyter_raw, line_length=line_length)
        write_jupyter(jupyter_black, jupyter_filename)

    print("All done!")


if __name__ == "__main__":
    main()
