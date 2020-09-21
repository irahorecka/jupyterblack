# jupyterblack

[![Licence](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/csurfer/blackcellmagic/master/LICENSE)

Format code cells in Jupyter Notebook and JupyterLab using [black](https://github.com/ambv/black).

## It's as simple as calling jblack

```bash
$ jblack my_notebook.ipynb
```

## Install jupyterblack from the command line with pip

```bash
$ pip install jupyterblack
```

## Usage

```bash
# Format to black's default line length of 88.
$ jblack notebook.ipynb

# Customize your own line lenth to 70.
$ jblack -l 70 notebook.ipynb

# Format three .ipynb files to default line length.
$ jblack notebook_1.ipynb notebook_2.ipynb notebook_3.ipynb

# Show help.
$ jblack -h
```

## Contributing

### Bug Reports and Feature Requests

Please use the [issues tracker](https://github.com/irahorecka/jupyterblack/issues) to report bugs or submit feature requests.

### Development

Pull requests are very welcome.
