# isoenum

[![License information](https://img.shields.io/pypi/l/isoenum.svg)](https://choosealicense.com/licenses/bsd-3-clause-clear/)
[![Current library version](https://img.shields.io/pypi/v/isoenum.svg)](https://pypi.org/project/isoenum)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/isoenum.svg)](https://pypi.org/project/isoenum)
[![Travis CI status](https://travis-ci.org/MoseleyBioinformaticsLab/isoenum.svg?branch=master)](https://travis-ci.org/MoseleyBioinformaticsLab/isoenum)
[![Code coverage information](https://codecov.io/gh/MoseleyBioinformaticsLab/isoenum/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/MoseleyBioinformaticsLab/isoenum)

[![Docker Automated build](https://img.shields.io/docker/automated/moseleybioinformaticslab/isoenum.svg)](https://github.com/MoseleyBioinformaticsLab/isoenum)
[![Docker Build Status](https://img.shields.io/docker/build/moseleybioinformaticslab/isoenum.svg)](https://hub.docker.com/r/moseleybioinformaticslab/isoenum)
[![Docker Pulls Status](https://img.shields.io/docker/pulls/moseleybioinformaticslab/isoenum.svg)](https://hub.docker.com/r/moseleybioinformaticslab/isoenum)


Isotopic (``iso``) enumerator (``enum``) - create isotopically resolved
InChI ([International Chemical Identifier](https://www.inchi-trust.org/)) for metabolites.

The ``isoenum`` Python package provides command-line interface that
allows you to create isotopically-resolved ``InChI`` from one of
the [Chemical Table file](https://en.wikipedia.org/wiki/Chemical_table_file) (``CTfile``) formats (i.e. ``molfile``, ``SDfile``)
used to describe chemical molecules and reactions as well as from ``InChI``
itself.


## Links

   * isoenum [@GitHub](https://github.com/MoseleyBioinformaticsLab/isoenum)
   * isoenum [@PyPI](https://pypi.org/project/isoenum)
   * isoenum [@DockerHub](https://hub.docker.com/r/moseleybioinformaticslab/isoenum)


## Installation

The ``isoenum`` package runs under Python 2.7 and Python 3.4+. Use [pip](https://pip.pypa.io) to install.


### Install on Linux, Mac OS X

```
python3 -m pip install isoenum
```


### Install on Windows

```
py -3 -m pip install isoenum
```

### Dependencies

The ``isoenum`` Python package requires **non-pip-installable** dependency:
[Open Babel](http://openbabel.org) chemistry library which relies on ``InChI`` library
to perform ``InChI`` conversions.

Refer to the official documentation to install [Open Babel](http://openbabel.org) on your system:

   * Official Installation Instructions: http://openbabel.org/wiki/Category:Installation


## License

This package is distributed under the [BSD](https://choosealicense.com/licenses/bsd-3-clause-clear) license.
