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


def invalid_extension(filename: Union[str, Path]) -> None:
    """Error message for file without .ipynb extension."""
    raise SystemExit(
        """Error: File {} does not have extension .ipynb.\n
Try 'jblack [-h, --help]' for help.""".format(
            filename
        )
    )
