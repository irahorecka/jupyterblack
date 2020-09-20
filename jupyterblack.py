import json
import safer
import uuid
from black import format_str, FileMode, InvalidInput


def open_jupyter(filename):
    with safer.open(filename, "r") as file:
        return file.read()


def parse_jupyter(content):
    newline_hash = str(uuid.uuid4())
    content_json = json.loads(content)
    for cell in content_json["cells"]:
        if cell["cell_type"] == "code":
            # print(repr("".join(cell["source"])))
            format_cell_repr = repr(format_black("".join(cell["source"])))
            ####dev#####

            black_cell=[i for i in format_black("".join(cell["source"]))]
            black_cell_newline=''.join([newline_hash if i == "\n" else i for i in black_cell])
            list_format = black_cell_newline.split(newline_hash)
            cell["source"] = [i + "\n" for i in list_format]
            ####dev#####
            # print(format_cell_repr.split('\\n'))
            # print(format_cell_repr.encode().decode('unicode_escape'), '\n')
            # temp_escape_list = format_cell_repr[1:-1].split("\\\\")
            # escape_exceptions = ("n", "t")
            # temp_escape_list = [
            #     "\\" + i if len(i) != 0 and i.startswith(escape_exceptions) else i for i in temp_escape_list
            # ]
            # temp_escape_list=["\\\\" if len(i) == 0 else i for i in temp_escape_list]
            # # print(temp_escape_list)
            # # replace empty cells with \\\\ to ""
            # if len(temp_escape_list) == 1 and temp_escape_list[0] == "\\\\":
            #     temp_escape_list = ['']
            # temp_escape_str = ''.join(temp_escape_list)
            # # print(temp_escape_str)
            # list_format = temp_escape_str.split("\\n")
            # # print(format_cell_repr)
            # # print(temp_escape_str)
            # # print(format_cell_repr)
            # # list_format = format_cell_repr[1:-1].split("\\n")
            # # print(temp_escape_list)
            # # print(list_format)
            # cell["source"] = [i + "\n" for i in list_format]
    return content_json


def format_black(cell_content, line_length=88):
    mode = FileMode(line_length=line_length)
    try:
        return format_str(src_contents=cell_content, mode=mode)
    except InvalidInput:
        return cell_content


def export_jupyter(formatted_content, filename):
    with open(filename, "w") as file:
        file.write(json.dumps(formatted_content))


if __name__ == "__main__":
    jupyter_raw = open_jupyter("test1_lab.ipynb")
    jupyter_format = parse_jupyter(jupyter_raw)
    export_jupyter(jupyter_format, "out_lab.ipynb")
