"""Black format your Jupyter Notebook and JupyterLab. Files must have a .ipynb extension.

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
from argparse import ArgumentParser, Namespace


def parse_args(*args: str) -> Namespace:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("targets", nargs="+", default=os.getcwd())
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("-s", "--skip-string-normalization", action="store_true")
    parser.add_argument("--pyi", action="store_true")

    parser.add_argument("-l", "--line-length", type=int, default=88)

    return parser.parse_intermixed_args(args)
