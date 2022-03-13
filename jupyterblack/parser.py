"""Open, parse, black format, and write .ipynb file(s)."""

import json
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Generic, List, Set, TypeVar, Union

import safer
from attr import attrs
from black import FileContent, FileMode, InvalidInput, TargetVersion, format_str
from typing_extensions import TypedDict

from jupyterblack.util.error_messages import invalid_content
from jupyterblack.util.files import read_file


class BlackFileModeKwargs(TypedDict, total=False):
    target_versions: Set[TargetVersion]
    line_length: int
    string_normalization: bool
    is_pyi: bool


L = TypeVar("L")  # Lint output type
F = TypeVar("F")  # Format output type
S = TypeVar("S")  # Invalid code reporting type


@attrs(auto_attribs=True)
class LintResult(Generic[L, S]):
    file: str
    is_okay: bool
    output: L
    invalid_report: S


TLintRes = TypeVar("TLintRes", bound=LintResult)


@attrs(auto_attribs=True)
class FormatResult(Generic[L, S]):
    file: str
    output: L
    invalid_report: S


TFormatRes = TypeVar("TFormatRes", bound=FormatResult)


class FileAnalyzer(Generic[TLintRes], ABC):
    def __init__(self, file_path: Union[str, Path]):
        self.file_path = file_path
        self.file_contents = read_file(file_path)

    @abstractmethod
    def run_check(self) -> TLintRes:
        pass


class FileFormatter(FileAnalyzer[TLintRes], Generic[TLintRes, TFormatRes], ABC):
    @abstractmethod
    def apply_format(self) -> TFormatRes:
        pass


@attrs(auto_attribs=True)
class BlackLintRes(LintResult[str, Dict[str, str]]):
    pass


@attrs(auto_attribs=True)
class BlackFormatRes(FormatResult[str, Dict[str, str]]):
    pass


MAGICS_MARKS = ("%", "$")


def _to_code(lines: List[str]) -> str:
    return "".join(lines)


class BlackFormatter(FileFormatter[BlackLintRes, BlackFormatRes]):
    def __init__(self, file_path: Union[str, Path], black_mode_kwargs: BlackFileModeKwargs):
        super().__init__(file_path)
        self.mode = FileMode(**black_mode_kwargs)

    def _format_black(self, lines: List[str]) -> FileContent:
        code = _to_code(lines)
        return format_str(src_contents=code, mode=self.mode)

    @property
    def path(self) -> str:
        return str(self.file_path)

    def run_check(self) -> BlackLintRes:
        content_json = json.loads(self.file_contents)
        is_formatted = True
        invalid_report: Dict[str, str] = {}

        for cell in content_json["cells"]:
            if cell["cell_type"] == "code":
                existing_code = _to_code(cell["source"])
                format_res = self.format_black_cell(cell["source"])
                invalid_report = {**invalid_report, **format_res.invalid_report}

                if format_res.output != existing_code:
                    is_formatted = False
                    break

        return BlackLintRes(self.path, is_okay=is_formatted, output="", invalid_report=invalid_report)

    def apply_format(self) -> BlackFormatRes:
        """Parse and black format .ipynb content."""
        try:
            content_json: Dict = json.loads(self.file_contents)
        except json.decoder.JSONDecodeError:
            invalid_content(self.file_path)
        newline_hash = str(uuid.uuid4())
        invalid_report: Dict[str, str] = {}

        for cell in content_json["cells"]:
            if cell["cell_type"] == "code":
                format_results = self.format_black_cell(cell["source"])
                # Replace '\n' with a unique hash
                blacked_cell = _to_code([newline_hash if char == "\n" else char for char in format_results.output])
                blacked_cell_lines = blacked_cell.split(newline_hash)
                # Black formatter appends "" to end of a code block - mimic this if "" not present
                if blacked_cell_lines[-1] != "":
                    blacked_cell_lines.append("")
                cell["source"] = [line + "\n" for line in blacked_cell_lines[:-1]]

                invalid_report = {**invalid_report, **format_results.invalid_report}

        return BlackFormatRes(self.path, json.dumps(content_json, indent=1), invalid_report)

    def format_black_cell(self, cell_lines: List[str]) -> BlackFormatRes:
        """Black format cell content to defined line length."""
        code = _to_code(cell_lines)
        try:  # Try to format all lines
            return BlackFormatRes(self.path, output=self._format_black(cell_lines), invalid_report={})
        except InvalidInput as exc:
            # The cell may contain lines with magics like "%time"
            if any(magic_mark in str(exc) for magic_mark in MAGICS_MARKS):
                return self._format_black_with_magics(cell_lines)
            return BlackFormatRes(self.path, code, {code: str(exc)})
        except Exception as exc:  # pylint: disable=broad-except
            return BlackFormatRes(self.path, code, {code: str(exc)})

    def _format_black_with_magics(self, cell_lines: List[str]) -> BlackFormatRes:
        """Split a cell that contains magics (i.e. lines that start with % or %%) in segments (before and after magics)
        and try to format each segment with black."""
        code_segments: List[FileContent] = []
        invalid_code: Dict[FileContent, str] = {}

        # Find indexes of magic lines
        magic_line_ix = [i for i, line in enumerate(cell_lines) if line.rstrip(" ").startswith(MAGICS_MARKS)]
        magic_line_ix = [*magic_line_ix, len(cell_lines)]
        prev_magic_ix = 0

        # Black each segment
        for magic_ix in magic_line_ix:
            segment_lines = cell_lines[prev_magic_ix:magic_ix]
            try:
                code_segments.append(self._format_black(segment_lines))
            except Exception as exc:  # pylint: disable=broad-except
                # Mark code as invalid syntax
                code = _to_code(segment_lines)
                code_segments.append(code)
                invalid_code[code] = str(exc)
            finally:
                if magic_ix < len(cell_lines):
                    code_segments.append(cell_lines[magic_ix])
            prev_magic_ix = magic_ix + 1
        return BlackFormatRes(self.path, _to_code(code_segments), invalid_code)


def format_jupyter_file(file: str, kwargs: BlackFileModeKwargs) -> BlackFormatRes:
    print(f"Reformatting {file}")
    formatter = BlackFormatter(file, black_mode_kwargs=kwargs)
    format_res = formatter.apply_format()
    write_jupyter_file(format_res.output, file)
    return format_res


def check_jupyter_file(file: str, kwargs: BlackFileModeKwargs) -> BlackLintRes:
    checker = BlackFormatter(file, black_mode_kwargs=kwargs)
    return checker.run_check()


def write_jupyter_file(content: str, filename: Union[Path, str]) -> None:
    """Safely write to .ipynb file."""
    with safer.open(filename, "w") as ipynb_outfile:
        ipynb_outfile.write(content)
