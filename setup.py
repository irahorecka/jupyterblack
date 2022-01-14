"""Setup for jupyterblack package."""
from setuptools import setup

import jupyterblack


with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="jupyterblack",
    version=jupyterblack.__version__,
    description="Format code cells in Jupyter Notebook and JupyterLab using black.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/irahorecka/jupyterblack",
    author="Ira Horecka",
    author_email="ira89@icloud.com",
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    packages=["jupyterblack", "jupyterblack/util"],
    include_package_data=True,
    install_requires=["attrs", "black", "safer"],
    entry_points={
        "console_scripts": [
            "jblack=jupyterblack.__main__:main",
        ]
    },
)
