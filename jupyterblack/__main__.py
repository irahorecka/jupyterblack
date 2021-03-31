import sys
from typing import List

from black import WriteBack

from jupyterblack import parser
from jupyterblack.arguments import parse_args
from jupyterblack.parser import BlackFileModeKwargs
from jupyterblack.util import error_messages
from jupyterblack.util.files import check_paths_exist
from jupyterblack.util.targets import targets_to_files


def main():
    """Read jupyterblack CLI arguments."""
    try:
        run(sys.argv[1:])
    except KeyboardInterrupt:
        print("Caught keyboard interrupt from user")


def run(args: List[str]) -> None:
    # pylint: disable=too-many-locals
    namespace = parse_args(*args)

    targets: List[str] = namespace.targets
    skip_string_normalization: bool = namespace.skip_string_normalization
    is_check: bool = namespace.check
    is_diff: bool = namespace.diff
    line_length: int = namespace.line_length
    is_pyi: bool = namespace.pyi

    check_paths_exist(targets)

    write_back = WriteBack.from_configuration(check=is_check, diff=is_diff)
    black_file_mode_kwargs = BlackFileModeKwargs(
        line_length=line_length, string_normalization=not skip_string_normalization
    )
    if is_pyi:  # Not sure if older versions of black have "is_pyi"
        black_file_mode_kwargs = BlackFileModeKwargs(
            line_length=line_length,
            string_normalization=not skip_string_normalization,
            is_pyi=is_pyi,
        )

    # Transform supplied targets (directories or files) to files
    target_files = targets_to_files(targets)
    # Check if input filename exists and has .ipynb extension
    for file in target_files:
        if not parser.check_ipynb_extension(file):
            error_messages.invalid_extension(file)

    if write_back is WriteBack.YES:
        for ipynb_filename in target_files:
            jupyter_content = parser.read_jupyter_file(ipynb_filename)
            print(f"Reformatting {ipynb_filename}")
            jupyter_black = parser.format_jupyter_file(
                jupyter_content, black_file_mode_kwargs
            )
            parser.write_jupyter_file(jupyter_black, ipynb_filename)
        print("All done!")
    elif write_back is WriteBack.CHECK:
        files_not_formatted: List[str] = []
        for ipynb_filename in target_files:
            jupyter_content = parser.read_jupyter_file(ipynb_filename)
            if not parser.check_jupyter_file_is_formatted(
                jupyter_content, black_file_mode_kwargs
            ):
                files_not_formatted.append(ipynb_filename)
        if not files_not_formatted:
            print("All good! Supplied targets are already formatted with black.")
        else:
            raise SystemExit(
                "Files that need formatting:\n  - " + "\n  - ".join(files_not_formatted)
            )
    else:
        raise SystemExit(f"WriteBack option: {write_back} not yet supported")


if __name__ == "__main__":
    main()
