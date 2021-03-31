from typing import List

from jupyterblack.util.files import filter_files, get_files


def targets_to_files(targets: List[str]) -> List[str]:
    files: List[str] = []
    for target in targets:
        files.extend(get_files(target))

    return sorted(filter_files(set(files)))
