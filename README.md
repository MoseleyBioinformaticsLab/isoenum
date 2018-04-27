# isoenum

[![License information](https://img.shields.io/pypi/l/isoenum.svg)](https://choosealicense.com/licenses/bsd-3-clause-clear/)
[![Current library version](https://img.shields.io/pypi/v/isoenum.svg)](https://pypi.org/project/isoenum)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/isoenum.svg)](https://pypi.org/project/isoenum)
[![Documentation Status](https://readthedocs.org/projects/isoenum/badge/?version=latest)](http://isoenum.readthedocs.io/en/latest/?badge=latest)
[![Travis CI status](https://travis-ci.org/MoseleyBioinformaticsLab/isoenum.svg?branch=master)](https://travis-ci.org/MoseleyBioinformaticsLab/isoenum)
[![Code coverage information](https://codecov.io/gh/MoseleyBioinformaticsLab/isoenum/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/gh/MoseleyBioinformaticsLab/isoenum)

[![Docker Automated build](https://img.shields.io/docker/automated/moseleybioinformaticslab/isoenum.svg)](https://github.com/MoseleyBioinformaticsLab/isoenum)
[![Docker Build Status](https://img.shields.io/docker/build/moseleybioinformaticslab/isoenum.svg)](https://hub.docker.com/r/moseleybioinformaticslab/isoenum)
[![Docker Pulls Status](https://img.shields.io/docker/pulls/moseleybioinformaticslab/isoenum.svg)](https://hub.docker.com/r/moseleybioinformaticslab/isoenum)


Isotopic (``iso``) enumerator (``enum``) - create isotopically resolved
InChI ([International Chemical Identifier](https://www.inchi-trust.org/)) for metabolites.

The ``isoenum`` Python package provides command-line interface that
allows you to create isotopically-resolved ``InChI`` from one of
the [Chemical Table file](https://en.wikipedia.org/wiki/Chemical_table_file) (``CTfile``) formats
(i.e. ``molfile``, ``SDfile``) used to describe chemical molecules and reactions as well as from ``InChI``
itself.

See [Tutorial](http://isoenum.readthedocs.io/en/latest/tutorial.html) documentation for
usage examples of ``isoenum`` Python package as well as ``isoenum`` docker container.


## Links

   * isoenum @ [GitHub](https://github.com/MoseleyBioinformaticsLab/isoenum)
   * isoenum @ [PyPI](https://pypi.org/project/isoenum)
   * isoenum @ [DockerHub](https://hub.docker.com/r/moseleybioinformaticslab/isoenum)
   * isoenum @ [ReadTheDocs](http://isoenum.readthedocs.io)


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
[Open Babel](http://openbabel.org) chemistry library version 2.3.90 or later
which relies on ``InChI`` library version 1.0.4 or later to perform ``InChI``
conversions.

Refer to the official documentation to install [Open Babel](http://openbabel.org) on your system:

   * Official Installation Instructions: http://openbabel.org/wiki/Category:Installation


## Docker

In addition to [PyPI](https://pypi.org/project/isoenum) package, ``Dockerfile`` and
automatically build [DockerHub](https://hub.docker.com/r/moseleybioinformaticslab/isoenum)
container which contains ``isoenum`` Python package and all its dependencies are also provided.

To use ``isoenum`` Python package, you will need to setup docker for your system
and ``pull`` or ``build`` docker container.

### Install docker

Install ``docker``:
   * Follow instructions to install docker for your system: https://docs.docker.com/engine/installation
      * [Ubuntu](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu)
      * [Debian](https://docs.docker.com/engine/installation/linux/docker-ce/debian)
      * [CentOS](https://docs.docker.com/engine/installation/linux/docker-ce/centos)
      * [Fedora](https://docs.docker.com/engine/installation/linux/docker-ce/fedora)
      * [Mac](https://docs.docker.com/docker-for-mac/install)
      * [Windows](https://docs.docker.com/docker-for-windows/install)

### Setup container

Setup ``isoenum`` container:
   * ``pull`` built image from the [DockerHub](https://hub.docker.com/r/moseleybioinformaticslab/isoenum):
   ```
   # docker pull moseleybioinformaticslab/isoenum
   # docker tag moseleybioinformaticslab/isoenum:latest isoenum:latest  # retag docker image
   # docker rmi moseleybioinformaticslab/isoenum  # remove after you have retagged it
   ```
   * or ``build`` an image using ``Dockerfile`` at the root of this repo by running
     ``docker build`` from directory containing ``Dockerfile``:
   ```
   # docker build -t isoenum .
   ```


## License

This package is distributed under the [BSD](https://choosealicense.com/licenses/bsd-3-clause-clear) license.
