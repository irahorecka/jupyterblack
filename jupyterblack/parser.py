"""Open, parse, black format, and write .ipynb file(s)."""

import json
import uuid
from pathlib import Path
from typing import Dict, Set, Tuple, Union

import safer
from black import FileContent, FileMode, InvalidInput, TargetVersion, format_str
from typing_extensions import TypedDict

from jupyterblack.util.files import read_file


class BlackFileModeKwargs(TypedDict, total=False):
    target_versions: Set[TargetVersion]
    line_length: int
    string_normalization: bool
    is_pyi: bool


def format_jupyter_file(file: str, kwargs: BlackFileModeKwargs) -> None:
    try:
        jupyter_content = read_file(file)
        print(f"Reformatting {file}")
        jupyter_black = format_jupyter_cells(jupyter_content, kwargs)
        write_jupyter_file(jupyter_black, file)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt from user")


def check_jupyter_file(file: str, kwargs: BlackFileModeKwargs) -> Tuple[str, bool]:
    try:
        jupyter_content = read_file(file)
        return (
            file,
            check_jupyter_file_is_formatted(jupyter_content, kwargs),
        )
    except KeyboardInterrupt:
        print("Caught keyboard interrupt from user")
        return file, True


def format_jupyter_cells(content: Union[str, bytes], kwargs: BlackFileModeKwargs) -> Dict:
    """Parse and black format .ipynb content."""
    content_json: Dict = json.loads(content)
    newline_hash = str(uuid.uuid4())

    for cell in content_json["cells"]:
        if cell["cell_type"] == "code":
            blacked_cell_char = format_black_cell("".join(cell["source"]), file_mode_kwargs=kwargs)
            # replace '\n' with a unique hash
            blacked_cell = "".join([newline_hash if char == "\n" else char for char in blacked_cell_char])
            blacked_cell_lines = blacked_cell.split(newline_hash)
            cell["source"] = [line + "\n" for line in blacked_cell_lines[:-1]]

    return content_json


def check_jupyter_file_is_formatted(content: Union[str, bytes], kwargs: BlackFileModeKwargs) -> bool:
    content_json = json.loads(content)
    is_formatted = True

    for cell in content_json["cells"]:
        if cell["cell_type"] == "code":
            code = "".join(cell["source"])
            blacked_cell_char = format_black_cell(code, file_mode_kwargs=kwargs)
            if blacked_cell_char != code:
                is_formatted = False
                break

    return is_formatted


def format_black_cell(cell_content: str, *, file_mode_kwargs: BlackFileModeKwargs) -> Union[str, FileContent]:
    """Black format cell content to defined line length."""
    mode = FileMode(**file_mode_kwargs)
    try:
        return format_str(src_contents=cell_content, mode=mode)
    except InvalidInput:
        return cell_content


def write_jupyter_file(content: Dict, filename: Union[Path, str]) -> None:
    """Safely write to .ipynb file."""
    with safer.open(filename, "w") as ipynb_outfile:
        ipynb_outfile.write(json.dumps(content))
