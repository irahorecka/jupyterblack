from pathlib import Path
from typing import List, Union


def resolve(path: Union[str, Path]) -> str:
    return str(path.resolve()) if isinstance(path, Path) else str(Path(path).resolve())


def read_file(path: Union[str, Path]) -> str:
    with open(resolve(path), "r") as file:
        return file.read()


def write_file(path: Union[str, Path],) -> str:
    with open(resolve(path), "r") as file:
        return file.read()


def get_files(path: Union[str, Path]) -> List[str]:
    actual_path = path.resolve() if isinstance(path, Path) else Path(path).resolve()
    if actual_path.is_dir():
        return list(map(str, dir_to_files(actual_path)))
    return [str(actual_path)]


def dir_to_files(directory: Path, suffix: str = ".ipynb") -> List[Path]:
    return list(directory.glob(f"**/*{suffix}"))
