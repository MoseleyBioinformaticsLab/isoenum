.. :changelog:

Release History
===============

0.1.5 (2018-04-26)
~~~~~~~~~~~~~~~~~~

**Bugfixes**

- Fixed incorrect rendering on PyPI project page.


0.1.4 (2018-04-25)
~~~~~~~~~~~~~~~~~~

**Improvements**

- Added ReadTheDocs documentation: http://isoenum.readthedocs.io


0.1.3 (2018-04-20)
~~~~~~~~~~~~~~~~~~

**Improvements**

- Added "Dockerfile" to create docker container with ``isoenum`` software and all
  required dependencies ready-to-use.
- Changes to cli options: replaced "-f" and "--full" with "-c" and "--complete"
  to specify labeling schema. Used "-f" for "--format" option.


0.1.2 (2018-04-19)
~~~~~~~~~~~~~~~~~~

**Improvements**

- Added ability to save conversion results into file via "--output" cli option
  and in different formats ("inchi", "mol", and "sdf") via "--format" cli option.


0.1.1 (2018-04-17)
~~~~~~~~~~~~~~~~~~

**Improvements**

- Added ability to process ``SDfiles`` in addition to ``Molfiles`` and ``InChI``.
- Added basic unit tests for command-line interface.

**Bugfixes**

- Fixed bug of not including package data configuration files into source distribution.


0.1.0 (2018-04-16)
~~~~~~~~~~~~~~~~~~

- Initial public release.
