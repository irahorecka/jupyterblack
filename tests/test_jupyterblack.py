# pylint: disable=redefined-outer-name
import json
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import List, Union

from pytest import mark, raises

from jupyterblack.__main__ import run
from jupyterblack.util.files import read_file


class Spec:
    def __init__(self, bad_contents: str, fixed_contents: str, options: List[str]):
        self.bad = bad_contents
        self.fixed = fixed_contents
        self.options = options


NOTEBOOKS = Path(__file__).parent / "notebooks"

NO_OPTS_SPEC = Spec(
    bad_contents=read_file(NOTEBOOKS / "no_opts" / "test_bad_format.ipynb"),
    fixed_contents=read_file(NOTEBOOKS / "no_opts" / "test_fixed_format.ipynb"),
    options=[],
)


SKIP_STRING_SPEC_1 = Spec(
    bad_contents=read_file(NOTEBOOKS / "skip_string" / "test_bad_format.ipynb"),
    fixed_contents=read_file(NOTEBOOKS / "skip_string" / "test_fixed_format.ipynb"),
    options=["-s"],
)


SKIP_STRING_SPEC_2 = Spec(
    bad_contents=read_file(NOTEBOOKS / "skip_string" / "test_bad_format.ipynb"),
    fixed_contents=read_file(NOTEBOOKS / "skip_string" / "test_fixed_format.ipynb"),
    options=["--skip-string-normalization"],
)


SKIP_STRING_SPEC_1_MULTI_WORKER = Spec(
    bad_contents=read_file(NOTEBOOKS / "skip_string" / "test_bad_format.ipynb"),
    fixed_contents=read_file(NOTEBOOKS / "skip_string" / "test_fixed_format.ipynb"),
    options=["-s", "-w", "3"],
)


SKIP_STRING_SPEC_2_MULTI_WORKER = Spec(
    bad_contents=read_file(NOTEBOOKS / "skip_string" / "test_bad_format.ipynb"),
    fixed_contents=read_file(NOTEBOOKS / "skip_string" / "test_fixed_format.ipynb"),
    options=["--skip-string-normalization", "--workers", "3"],
)

SKIP_STRING_SPEC_3 = Spec(
    bad_contents=read_file(NOTEBOOKS / "skip_string" / "test_bad_format.ipynb"),
    fixed_contents=read_file(NOTEBOOKS / "skip_string" / "test_fixed_format.ipynb"),
    options=["--skip-string-normalization", "-t", "py37", "py38"],
)


MAGIC_SPEC = Spec(
    bad_contents=read_file(NOTEBOOKS / "magics" / "test_bad_format.ipynb"),
    fixed_contents=read_file(NOTEBOOKS / "magics" / "test_fixed_format.ipynb"),
    options=[],
)


SPECS = [
    MAGIC_SPEC,
    NO_OPTS_SPEC,
    SKIP_STRING_SPEC_1,
    SKIP_STRING_SPEC_2,
    SKIP_STRING_SPEC_3,
    SKIP_STRING_SPEC_2_MULTI_WORKER,
    SKIP_STRING_SPEC_2_MULTI_WORKER,
]


@mark.parametrize("spec", SPECS)
def test_format_file(spec: Spec) -> None:
    try:
        with NamedTemporaryFile(mode="w", delete=False, suffix=".ipynb") as temp:
            temp.write(spec.bad)
            test_file_path = temp.name

        with raises(SystemExit):
            run(["--check", test_file_path, *spec.options])

        run([test_file_path, *spec.options])
        assert read_file(test_file_path) == json.dumps(json.loads(spec.fixed), indent=1)
        run(["--check", test_file_path, *spec.options])
    finally:
        temp.close()


@mark.parametrize("spec", SPECS)
def test_format_dir_default(spec: Spec) -> None:
    files: List[str] = []

    def create_files(directory: Union[str, Path], n_files_per_directory: int = 3) -> None:
        directory_path = Path(directory)
        directory_path.mkdir(exist_ok=True)
        for file_number in range(n_files_per_directory):
            for extension in [".ipynb", ".py"]:
                file_path = str((directory_path / f"{file_number}{extension}").resolve())
                files.append(file_path)
                with open(file_path, mode="w", encoding="utf-8") as temp_file:
                    temp_file.write(spec.bad)

    def check_before_and_after_format(targets: List[str], affected_files: List[str]) -> None:
        file_contents_before = {file: read_file(file) for file in affected_files}
        # Checks before formatting fail
        with raises(SystemExit):
            run(["--check", *targets, *spec.options])
        # A --check run does not change the files
        for file, file_contents in file_contents_before.items():
            assert read_file(file) == file_contents, file

        # Run black
        run([*targets, *spec.options])

        # Checks after formatting succeed
        for file in affected_files:
            if file.endswith(".ipynb"):  # ipynb files changed
                assert read_file(file) != file_contents_before[file], file
                assert read_file(file) == json.dumps(json.loads(spec.fixed), indent=1), file
                assert (
                    json.loads(read_file(file))["cells"] == json.loads(spec.fixed)["cells"]
                ), f"No exact match with file {file}"
            else:  # Other files stayed the same
                assert read_file(file) == file_contents_before[file], file
        run(["--check", *targets, *spec.options])

    # Single target directory, single level directory
    with TemporaryDirectory() as temp_dir:
        create_files(temp_dir)
        check_before_and_after_format([temp_dir], affected_files=files)
        files = []

    # Multiple target files, single level directory
    with TemporaryDirectory() as temp_dir:
        create_files(temp_dir)
        check_before_and_after_format(files, affected_files=files)
        files = []

    # Single target directory, double level directory - outer
    with TemporaryDirectory() as temp_dir:
        create_files(temp_dir)
        inner_dir = (Path(temp_dir) / "inner").resolve()
        create_files(inner_dir)
        check_before_and_after_format([temp_dir], affected_files=files)
        files = []

    # Single target directory, double level directory - inner
    with TemporaryDirectory() as temp_dir:
        create_files(temp_dir)
        inner_dir = (Path(temp_dir) / "inner").resolve()
        create_files(inner_dir)
        # Check inner dir first - target is the dir
        check_before_and_after_format([str(inner_dir)], affected_files=files[-6:])
        # Do the rest of the files - targets are the files
        check_before_and_after_format(files[:-6], affected_files=files[:-6])
        files = []
