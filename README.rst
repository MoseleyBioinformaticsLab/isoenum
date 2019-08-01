isoenum
=======


.. image:: https://img.shields.io/pypi/l/isoenum.svg
   :target: https://choosealicense.com/licenses/bsd-3-clause-clear/
   :alt: License information

.. image:: https://img.shields.io/pypi/v/isoenum.svg
   :target: https://pypi.org/project/isoenum
   :alt: Current library version

.. image:: https://img.shields.io/pypi/pyversions/isoenum.svg
   :target: https://pypi.org/project/isoenum
   :alt: Supported Python versions

.. image:: https://readthedocs.org/projects/isoenum/badge/?version=latest
   :target: http://isoenum.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/MoseleyBioinformaticsLab/isoenum.svg?branch=master
   :target: https://travis-ci.org/MoseleyBioinformaticsLab/isoenum
   :alt: Travis CI status

.. image:: https://codecov.io/gh/MoseleyBioinformaticsLab/isoenum/branch/master/graphs/badge.svg?branch=master
   :target: https://codecov.io/gh/MoseleyBioinformaticsLab/isoenum
   :alt: Code coverage information

|

.. image:: https://img.shields.io/docker/automated/moseleybioinformaticslab/isoenum.svg
   :target: https://github.com/MoseleyBioinformaticsLab/isoenum
   :alt: Docker automated build

.. image:: https://img.shields.io/docker/build/moseleybioinformaticslab/isoenum.svg
   :target: https://hub.docker.com/r/moseleybioinformaticslab/isoenum/builds
   :alt: Docker build status

.. image:: https://img.shields.io/docker/pulls/moseleybioinformaticslab/isoenum.svg
   :target: https://hub.docker.com/r/moseleybioinformaticslab/isoenum
   :alt: Docker pulls status


Isotopic (``iso``) enumerator (``enum``) - enumerates isotopically resolved
InChI (`International Chemical Identifier`_) for metabolites.

The ``isoenum`` Python package provides command-line interface that
allows you to enumerate the possible isotopically-resolved ``InChI`` from one of
the `Chemical Table file`_  (``CTfile``) formats (i.e. ``molfile``, ``SDfile``)
used to describe chemical molecules and reactions as well as from ``InChI``
itself.

See Tutorial_ documentation for usage examples of ``isoenum`` Python package
as well as ``isoenum`` docker container.


Links
~~~~~

   * isoenum @ GitHub_
   * isoenum @ PyPI_
   * isoenum @ DockerHub_
   * isoenum @ ReadTheDocs_


Installation
~~~~~~~~~~~~

The ``isoenum`` package runs under Python 2.7 and Python 3.4+. Use pip_ to install.


Install on Linux, Mac OS X
--------------------------

.. code:: bash

   python3 -m pip install isoenum


Install on Windows
------------------

.. code:: bash

   py -3 -m pip install isoenum


Dependencies
------------

The ``isoenum`` Python package requires a **non-pip-installable** dependency:
the `Open Babel`_ chemistry library version 2.3.90 or later, which relies on
``InChI`` library_ version 1.0.4 or later to perform ``InChI`` conversions.

Refer to the official documentation to install `Open Babel`_ on your system:

   * Official Installation Instructions: http://openbabel.org/wiki/Category:Installation


Docker
~~~~~~

In addition to PyPI_ package, ``Dockerfile`` and the automatically built DockerHub_
container, which contains the ``isoenum`` Python package and all its dependencies, are
also provided.

To use the ``isoenum`` Python package, you will need to setup docker for your system
and ``pull`` or ``build`` the docker container.


Install docker
--------------

Install ``docker``:

   * Follow the instructions to install docker on your system: https://docs.docker.com/engine/installation

      * Ubuntu_
      * Debian_
      * CentOS_
      * Fedora_
      * Mac_
      * Windows_

Setup container
---------------

Setup the ``isoenum`` container:

   * ``pull`` the built image from the DockerHub_:

   .. code:: bash

      # docker pull moseleybioinformaticslab/isoenum
      # docker tag moseleybioinformaticslab/isoenum:latest isoenum:latest  # retag docker image
      # docker rmi moseleybioinformaticslab/isoenum  # remove after you have retagged it

   * or ``build`` an image using ``Dockerfile`` at the root of this repo by running
     ``docker build`` from the directory containing ``Dockerfile``:

   .. code:: bash

      # docker build -t isoenum .


Development version installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install development version on Linux, Mac OS X
----------------------------------------------

.. code:: bash

    python3 -m pip install git+git://github.com/MoseleyBioinformaticsLab/isoenum.git


Install development version on Windows
--------------------------------------

.. code:: bash

   py -3 -m pip install git+git://github.com/MoseleyBioinformaticsLab/isoenum.git


License
~~~~~~~

This package is distributed under the BSD_ `license`.


.. _GitHub: https://github.com/MoseleyBioinformaticsLab/isoenum
.. _PyPI: https://pypi.org/project/isoenum
.. _DockerHub: https://hub.docker.com/r/moseleybioinformaticslab/isoenum
.. _ReadTheDocs: http://isoenum.readthedocs.io
.. _Tutorial: http://isoenum.readthedocs.io/en/latest/tutorial.html
.. _library: https://www.inchi-trust.org/downloads

.. _pip: https://pip.pypa.io

.. _Open Babel: http://openbabel.org
.. _Chemical Table file: https://en.wikipedia.org/wiki/Chemical_table_file
.. _International Chemical Identifier: https://www.inchi-trust.org/

.. _BSD: https://choosealicense.com/licenses/bsd-3-clause-clear

.. _Ubuntu: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu
.. _Debian: https://docs.docker.com/engine/installation/linux/docker-ce/debian
.. _CentOS: https://docs.docker.com/engine/installation/linux/docker-ce/centos
.. _Fedora: https://docs.docker.com/engine/installation/linux/docker-ce/fedora
.. _Mac: https://docs.docker.com/docker-for-mac/install
.. _Windows: https://docs.docker.com/docker-for-windows/install
