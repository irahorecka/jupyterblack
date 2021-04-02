import re
from pathlib import Path
from typing import Iterable, List, Sequence, Union, cast

import safer

from jupyterblack.util.error_messages import invalid_extensions, invalid_paths


def resolve(path: Union[str, Path]) -> Path:
    return path.resolve() if isinstance(path, Path) else Path(path).resolve()


def read_file(path: Union[str, Path], encoding: str = "utf-8") -> str:
    """Safely open .ipynb file."""
    with safer.open(resolve(path), "r", encoding=encoding) as ipynb_infile:
        return cast(str, ipynb_infile.read())


def write_file(
    path: Union[str, Path],
) -> str:
    with open(resolve(path), "r") as file:
        return file.read()


def get_files(path: Union[str, Path]) -> List[str]:
    resolved_path = resolve(path)
    if resolved_path.is_dir():
        return list(map(str, dir_to_files(resolved_path)))
    return [str(resolved_path)]


def dir_to_files(directory: Path, suffix: str = ".ipynb") -> List[Path]:
    return list(directory.glob(f"**/*{suffix}"))


def filter_files(
    files: Iterable[str],
    include_regexes: Sequence[str] = (),
    exclude_regexes: Sequence[str] = (),
) -> List[str]:
    include = [re.compile(regex) for regex in (".*.ipynb", *include_regexes)]
    exclude = [re.compile(regex) for regex in exclude_regexes]
    return [
        file
        for file in files
        if all(regex.match(file) for regex in include) and not any(regex.match(file) for regex in exclude)
    ]


def check_paths_exist(paths: Sequence[Union[str, Path]]) -> None:
    non_existent_paths = [path for path in paths if not resolve(path).exists()]
    if non_existent_paths:
        invalid_paths(non_existent_paths)


def check_ipynb_extensions(files: Sequence[Union[Path, str]]) -> None:
    """Verify .ipynb extension."""
    failing = [file for file in files if not str(file).endswith(".ipynb")]
    if failing:
        invalid_extensions(failing)
