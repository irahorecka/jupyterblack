"""Open, parse, blackify, and write .ipynb file(s)."""

import json
import uuid
import safer
from black import format_str, FileMode, InvalidInput


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
            # replace '\n' with a unique hash
            blacked_cell = "".join(
                [newline_hash if char == "\n" else char for char in blacked_cell_char]
            )
            blacked_cell_lines = blacked_cell.split(newline_hash)
            cell["source"] = [line + "\n" for line in blacked_cell_lines[:-1]]

    return content_json


def write_jupyter(content, filename):
    """Write to .ipynb file"""
    with safer.open(filename, "w") as ipynb_outfile:
        ipynb_outfile.write(json.dumps(content))


def format_black(cell_content, **kwargs):
    """Blackify cell content to appropriate line length"""
    line_length = kwargs["line_length"]
    mode = FileMode(line_length=line_length)
    try:
        return format_str(src_contents=cell_content, mode=mode)
    except InvalidInput:
        return cell_content


def check_ipynb_extension(filename):
    """Check .ipynb extension"""
    return bool(filename.endswith(".ipynb"))
