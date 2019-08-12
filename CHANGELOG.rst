.. :changelog:

Release History
===============

0.4.1 (2019-08-12)
~~~~~~~~~~~~~~~~~~

**Improvements**

- Added custom exceptions module.


0.4.0 (2019-07-30)
~~~~~~~~~~~~~~~~~~

**Improvements**

- Added documentation on how to install development version from GitHub.
- Simplified set of functions that interfaces with Open Babel.
- Added default output formats configuration file.
- Generalized functions that create ``CTfile`` objects to accept
  both ``InChI`` and ``SMILES``.
- Added API functions module.
- Added functionality to annotate `Molfiles` that have the same `InChI` and
  coupling type but different labeling schema as magnetically equivalent.

**Bugfixes**

- Fixed bug that used arbitrary output file format extension to save the results.
- Fixed bug not being able to pass two-word options to Open Babel.


0.3.1 (2018-08-27)
~~~~~~~~~~~~~~~~~~

**Improvements**

- Updated "The isoenum Tutorial" documentation.
- Restructured tutorial into two sections: "The isoenum Tutorial" and "The isoenum Docker Tutorial".
- Added logic to use "FixedH" option to create ``InChI`` for charged molecules.

**Bugfixes**

- Fixed bug that gave an error if existing "ISO" property was present.
- Fixed bug generating incorrect coupling for "C" atoms that did not
  have any "H" attached to it (e.g. "C=O").
- Fixed bug that did not create multiple subsets for "J3HH" couplings.


0.3.0 (2018-08-22)
~~~~~~~~~~~~~~~~~~

**Improvements**

- Added ``ionize`` command and functionality in order to create charged versions
  of neutral molecules, e.g. zwitterion forms of amino acids (https://en.wikipedia.org/wiki/Zwitterion)
- Removed Open Babel system call stdout messages.


0.2.1 (2018-08-20)
~~~~~~~~~~~~~~~~~~

**Improvements**

- Updated CLI isotope specification: ``--specific=<isotope:element:position>``,
  ``--all=<isotope:element>``, ``--enumerate=<isotope:element:min:max>``.
- Updated all documentation examples according to new CLI.
- Removed trailing "\n" from ``InChI`` strings.


0.2.0 (2018-08-15)
~~~~~~~~~~~~~~~~~~

**Improvements**

- Added new command-line interface command ``nmr`` and module in order
  to generate ``InChI`` associated with observed coupling combination
  for a given NMR experiment type.
- Added "1D 1H" and "1D 13C HSQC" NMR experiments.
- Added new output formats "json" and "csv".
- Updated API documentation.


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
