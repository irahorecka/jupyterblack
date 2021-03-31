# pylint: disable=redefined-outer-name
import json
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import List

from pytest import fixture, mark

from jupyterblack.__main__ import run
from jupyterblack.util.files import read_file


@fixture
def bad_format() -> str:
    return read_file(Path(__file__).parent / "test_bad_format.ipynb")


@fixture
def fixed_default() -> str:
    return read_file(Path(__file__).parent / "test_fixed_format_default.ipynb")


def test_format_file_default(bad_format: str, fixed_default: str) -> None:
    try:
        with NamedTemporaryFile(mode="w", delete=False, suffix=".ipynb") as temp:
            temp.write(bad_format)
            test_file_path = temp.name

        run(["jblack", test_file_path])
        assert read_file(test_file_path) == json.dumps(json.loads(fixed_default))
    finally:
        temp.close()


@mark.parametrize("is_inner", [True, False])
def test_format_dir_default(
    bad_format: str, fixed_default: str, is_inner: bool
) -> None:
    n_files_per_directory = 3
    files: List[str] = []

    def create_files(directory: str) -> None:
        for file_number in range(n_files_per_directory):
            file_path = f"{directory}/{file_number}.ipynb"
            files.append(file_path)
            with open(file_path, mode="w") as temp_file:
                temp_file.write(bad_format)

    with TemporaryDirectory() as temp_dir:
        create_files(temp_dir)
        inner_dir = (Path(temp_dir) / "inner").resolve()
        inner_dir.mkdir(exist_ok=True)
        create_files(str(inner_dir))

        if not is_inner:
            run(["jblack", temp_dir])
            for file in files:
                assert read_file(file) == json.dumps(json.loads(fixed_default))
        else:
            run(["jblack", str(inner_dir)])
            for file in files[-3:]:
                assert read_file(file) == json.dumps(json.loads(fixed_default))
