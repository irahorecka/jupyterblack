"""Print error message to console."""
from pathlib import Path
from typing import List, Union


def invalid_paths(files: List[Union[str, Path]]) -> None:
    """Error message for file not found."""
    raise SystemExit(
        """Error: Paths {} do not exist.\n
Try 'jblack [-h, --help]' for help.""".format(
            files
        )
    )


def invalid_extensions(files: List[Union[str, Path]]) -> None:
    """Error message for file without .ipynb extension."""
    raise SystemExit(
        """Error: Files {} do not have extension .ipynb.\n
Try 'jblack [-h, --help]' for help.""".format(
            files
        )
    )


def invalid_content(file: Union[str, Path]) -> None:
    """Error message for file with malformed Jupyter content."""
    raise SystemExit(
        """Error: File {} is malformed.\n
Try 'jblack [-h, --help]' for help.""".format(
            file
        )
    )
