"""Black format your Jupyter Notebook and JupyterLab.

Usage:
------

Format one Jupyter file:

    $ jblack notebook.ipynb

Format multiple Jupyter files:

    $ jblack notebook_1.ipynb notebook_2.ipynb [...]

Format a directory:

    $ jblack python/

Format one Jupyter file with a line length of 70:

    $ jblack -l 70 notebook.ipynb
"""

import os
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter

from black import TargetVersion


def parse_args(*args: str) -> Namespace:
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument("--check", action="store_true")
    # parser.add_argument("--diff", action="store_true")
    parser.add_argument("--pyi", action="store_true")
    parser.add_argument("-l", "--line-length", type=int, default=88)
    parser.add_argument("-s", "--skip-string-normalization", action="store_true")
    parser.add_argument("-w", "--workers", type=int, default=1, help="number of worker processes")
    parser.add_argument("--show-invalid-code", action="store_true")
    parser.add_argument("targets", nargs="+", default=os.getcwd())
    parser.add_argument(
        "-t",
        "--target-version",
        nargs="+",
        help="Python versions that should be supported by Black's output. [default: per-file auto-detection]",
        choices=[version.name.lower() for version in TargetVersion],
    )

    return parser.parse_args(args)
