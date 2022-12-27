"""Print error message to console."""
from pathlib import Path
from typing import List, Union


def invalid_paths(files: List[Union[str, Path]]) -> None:
    """Error message for file not found."""
    raise SystemExit(
        f"""Error: Paths {files} do not exist.\n
Try 'jblack [-h, --help]' for help."""
    )


def invalid_extensions(files: List[Union[str, Path]]) -> None:
    """Error message for file without .ipynb extension."""
    raise SystemExit(
        f"""Error: Files {files} do not have extension .ipynb.\n
Try 'jblack [-h, --help]' for help."""
    )


def invalid_content(file: Union[str, Path]) -> None:
    """Error message for file with malformed Jupyter content."""
    raise SystemExit(
        f"""Error: File {file} is malformed.\n
Try 'jblack [-h, --help]' for help."""
    )
