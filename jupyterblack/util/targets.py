from typing import List

from jupyterblack.util.files import get_files


def targets_to_files(targets: List[str]) -> List[str]:
    res: List[str] = []
    for target in targets:
        res.extend(get_files(target))
    return sorted(set(res))
