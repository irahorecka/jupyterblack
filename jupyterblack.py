import json
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
            cell["source"] = [line + "\n" for line in cell_lines]

    return content_json


def format_black(cell_content, line_length=88):
    mode = FileMode(line_length=line_length)
    try:
        return format_str(src_contents=cell_content, mode=mode)
    except InvalidInput:
        return cell_content


def export_jupyter(formatted_content, filename):
    with open(filename, "w") as jupyter_outfile:
        jupyter_outfile.write(json.dumps(formatted_content))


if __name__ == "__main__":
    jupyter_raw = open_jupyter("test1_lab.ipynb")
    jupyter_format = parse_jupyter(jupyter_raw)
    export_jupyter(jupyter_format, "out_lab.ipynb")
