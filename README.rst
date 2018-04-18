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

.. image:: https://travis-ci.org/MoseleyBioinformaticsLab/isoenum.svg?branch=master
   :target: https://travis-ci.org/MoseleyBioinformaticsLab/isoenum
   :alt: Travis CI status

.. image:: https://codecov.io/gh/MoseleyBioinformaticsLab/isoenum/branch/master/graphs/badge.svg?branch=master
   :target: https://codecov.io/gh/MoseleyBioinformaticsLab/isoenum
   :alt: Code coverage information


Isotopic (``iso``) enumerator (``enum``) - create isotopically resolved
InChI (`International Chemical Identifier`_) for metabolites.

The ``isoenum`` Python package provides command-line interface that
allows you to create isotopically-resolved ``InChI`` from one of
the `Chemical Table file`_  (``CTfile``) formats (i.e. ``molfile``, ``SDfile``)
used to describe chemical molecules and reactions as well as from ``InChI``
itself.


Links
~~~~~

   * isoenum @ GitHub_
   * isoenum @ PyPI_


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

The ``isoenum`` Python package requires **non-pip-installable** dependency:
`Open Babel`_ chemistry library which relies on ``InChI`` library
to perform ``InChI`` conversions.

Refer to the official documentation to install `Open Babel`_ on your system:

   * Official Installation Instructions: http://openbabel.org/wiki/Category:Installation


License
~~~~~~~

This package is distributed under the BSD_ `license`.


.. _GitHub: https://github.com/MoseleyBioinformaticsLab/isoenum
.. _PyPI: https://pypi.org/project/isoenum
.. _pip: https://pip.pypa.io


.. _Open Babel: http://openbabel.org
.. _Chemical Table file: https://en.wikipedia.org/wiki/Chemical_table_file
.. _International Chemical Identifier: https://www.inchi-trust.org/


.. _BSD: https://choosealicense.com/licenses/bsd-3-clause-clear
