"""Print error message to console."""


def no_args():
    """Error message for no args"""
    print(
        """jupyterblack takes at least one argument with .ipynb extension.\n
Try 'jblack [-h, --help]' for help."""
    )


def invalid_options():
    """Error message for invalid options"""
    print(
        """Invalid option(s):
Use only [-h, --help] or [-l, --line_length].\n
Try 'jblack [-h, --help]' for help."""
    )


def invalid_linelength():
    """Error message for invalid line length (not of type int)"""
    print(
        """Invalid line length value:
[-l, --line_length] must be the first argument followed by an int.\n
Try 'jblack [-h, --help]' for help."""
    )


def invalid_filename(filename):
    """Error message for file not found"""
    print(
        """Error: Path {} does not exist.\n
Try 'jblack [-h, --help]' for help.""".format(
            filename
        )
    )


def invalid_extension(filename):
    """Error message for file without .ipynb extension"""
    print(
        """Error: File {} does not have extension .ipynb.\n
Try 'jblack [-h, --help]' for help.""".format(
            filename
        )
    )
