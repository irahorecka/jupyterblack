import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="jupyterblack",
    version="0.1.0",
    description="Format code cells in Jupyter Notebook and JupyterLab using black.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/irahorecka/jupyterblack",
    author="Ira Horecka",
    author_email="ira89@icloud.com",
    license="MIT",
    python_requires=">=3.5",
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
    packages=["jupyterblack"],
    include_package_data=True,
    install_requires=["black", "safer"],
    entry_points={
        "console_scripts": [
            "jblack=jupyterblack.__main__:main",
        ]
    },
)