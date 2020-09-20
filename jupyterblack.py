"""
Blackify your Jupyter file.
Files must have an .ipynb extension.

Usage:
------
Blackify one or more .ipynb file:

    $ jupyterblack notebook.ipynb
    $ jupyterblack notebook_1.ipynb notebook_2.ipynb ...

Show help:

    $ jupyterblack [-h, --help]
"""
import json
import os
import sys
import uuid
import safer
from black import format_str, FileMode, InvalidInput


def open_jupyter(filename):
    with safer.open(filename, "r") as jupyter_infile:
        return jupyter_infile.read()


def parse_jupyter(content):
    content_json = json.loads(content)
    newline_hash = str(uuid.uuid4())
    for cell in content_json["cells"]:
        if cell["cell_type"] == "code":
            blacked_cell_char = [char for char in format_black("".join(cell["source"]))]
            blacked_cell = "".join(
                [newline_hash if char == "\n" else char for char in blacked_cell_char]
            )
            cell_lines = blacked_cell.split(newline_hash)
            cell["source"] = [line + "\n" for line in cell_lines[:-1]]

    return content_json


def export_jupyter(formatted_content, filename):
    with open(filename, "w") as jupyter_outfile:
        jupyter_outfile.write(json.dumps(formatted_content))


def format_black(cell_content, line_length=88):
    mode = FileMode(line_length=line_length)
    try:
        return format_str(src_contents=cell_content, mode=mode)
    except InvalidInput:
        return cell_content


def check_ipynb_extension(filename):
    return bool(filename.endswith(".ipynb"))


def main():
    """Read jupyterblack CLI arguments"""

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    # Show help message
    if "-h" in opts or "--help" in opts:
        print(__doc__)
        return

    # Determine if args present
    try:
        jupyter_filename = args[0]
    except IndexError:
        print(
            """jupyterblack takes at least one argument with a .ipynb extension.\n
Try 'jupyterblack [-h, --help]' for help."""
        )

    # Check if input filename exists and has .ipynb extension
    for filename in args:
        if not os.path.exists(filename):
            print(
                """Error: Path {} does not exist.\n
Try 'jupyterblack [-h, --help]' for help.""".format(
                    filename
                )
            )
            sys.exit(1)
        if not check_ipynb_extension(filename):
            print(
                """Error: File {} does not have extension .ipynb.\n
Try 'jupyterblack [-h, --help]' for help.""".format(
                    filename
                )
            )
            sys.exit(1)

    # Blackify Jupyter files
    for jupyter_filename in args:
        jupyter_raw = open_jupyter(jupyter_filename)
        jupyter_black = parse_jupyter(jupyter_raw)
        export_jupyter(jupyter_black, jupyter_filename)

    print("All done!")


if __name__ == "__main__":
    main()
