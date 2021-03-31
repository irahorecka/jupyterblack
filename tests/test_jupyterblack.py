# pylint: disable=redefined-outer-name
import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from pytest import fixture

from jupyterblack.__main__ import run


@fixture
def bad_format() -> str:
    path = (Path(__file__).parent / "test_bad_format.ipynb").resolve()
    with open(str(path), "r") as file:
        return file.read()


@fixture
def fixed_default() -> str:
    path = (Path(__file__).parent / "test_fixed_format_default.ipynb").resolve()
    with open(str(path), "r") as file:
        return file.read()


def test_format(bad_format: str, fixed_default: str) -> None:
    try:
        with NamedTemporaryFile(mode="w", delete=False, suffix=".ipynb") as temp:
            temp.write(bad_format)
            test_file_path = temp.name

        run(["jblack", test_file_path])
        with open(test_file_path, "r") as file:
            assert file.read() == json.dumps(json.loads(fixed_default))
    finally:
        temp.close()
