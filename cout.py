def no_args():
    print(
        """jupyterblack takes at least one argument with a .ipynb extension.\n
Try 'jupyterblack [-h, --help]' for help."""
    )


def invalid_linecount():
    print(
        """Invalid line count value:
[-l, --line_count] must be followed by an integer.\n
Try 'jupyterblack [-h, --help]' for help."""
    )


def invalid_filename(filename):
    print(
        """Error: Path {} does not exist.\n
Try 'jupyterblack [-h, --help]' for help.""".format(
            filename
        )
    )


def invalid_extension(filename):
    print(
        """Error: File {} does not have extension .ipynb.\n
Try 'jupyterblack [-h, --help]' for help.""".format(
            filename
        )
    )
