The isoenum Tutorial
====================

Command-line interface
~~~~~~~~~~~~~~~~~~~~~~

The ``isoenum`` package provides easy-to-use command-line interface
that allows specification of isotopes necessary to create isotopically-resolved
``InChI``.


To display all available options, run:

.. code-block:: none

   $ python3 -m isoenum --help

Output:

.. code-block:: none

   Isotopic enumerator (isoenum) command-line interface

   Usage:
       isoenum -h | --help
       isoenum --version
       isoenum name (<path-to-ctfile-file-or-inchi-file-or-inchi-string>)
                    [--specific=<element-isotope-position>...]
                    [--all=<element-isotope>...]
                    [--enumerate=<element-isotope-count>...]
                    [--complete | --partial]
                    [--ignore-iso]
                    [--format=<format>]
                    [--output=<path>]
                    [--verbose]

   Options:
       -h, --help                                 Show this screen.
       --verbose                                  Print more information.
       -v, --version                              Show version.
       -a, --all=<element-isotope>                Specify element and isotope, e.g. -a C-13 or --all=C-13
       -s, --specific=<element-isotope-position>  Specify element, isotope and specific position,
                                                  e.g. -s C-13-1 or --specific=C-13-1.
       -e, --enumerate=<element-isotope-min-max>  Enumerate all isotopically-resolved CTfile or InChI.
       -c, --complete                             Use complete labeling schema, i.e. every atom must specify
                                                  "ISO" property, partial labeling schema will be used otherwise
                                                  for specified labeling information only.
       -p, --partial                              Use partial labeling schema, i.e. generate labeling schema
                                                  from the provided labeling information.
       -i, --ignore-iso                           Ignore existing "ISO" specification in the CTfile or InChI.
       -f, --format=<format>                      Format of output: inchi, mol or sdf [default: inchi].
       -o, --output=<path>                        Path to output file.


Usage examples
~~~~~~~~~~~~~~

Input files
-----------

We are going to use several input files to generate isotopically-resolved
``InChI``.

   * ``Molfile`` example:

   .. code-block:: none

      pentane-2_2-diol
      OpenBabel04241814313D

       19 18  0  0  0  0  0  0  0  0999 V2000
          0.9398    0.0281    0.0594   C 0  0  0  0  0  0  0  0  0  0  0  0
          5.1399   -1.8948   -1.9819   C 0  0  0  0  0  0  0  0  0  0  0  0
          2.4621    0.0601    0.0832   C 0  0  0  0  0  0  0  0  0  0  0  0
          3.0524   -0.9348   -0.9251   C 0  0  0  0  0  0  0  0  0  0  0  0
          4.5873   -0.9132   -0.9449   C 0  0  0  0  0  0  0  0  0  0  0  0
          5.0222    0.3995   -1.2439   O 0  0  0  0  0  0  0  0  0  0  0  0
          5.1166   -1.2929    0.3146   O 0  0  0  0  0  0  0  0  0  0  0  0
          0.5343    0.7436    0.7819   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.5639   -0.9667    0.3178   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.5563    0.2945   -0.9319   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.8204   -1.6296   -2.9975   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.8268   -2.9228   -1.7657   H 0  0  0  0  0  0  0  0  0  0  0  0
          6.2362   -1.8812   -1.9694   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.8078   -0.1742    1.0938   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.7926    1.0796   -0.1484   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.6751   -0.6810   -1.9232   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.6972   -1.9418   -0.6781   H 0  0  0  0  0  0  0  0  0  0  0  0
          5.1501    0.4682   -2.2019   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.7281   -2.1498    0.5503   H 0  0  0  0  0  0  0  0  0  0  0  0
        1  3  1  0  0  0  0
        1  8  1  0  0  0  0
        1  9  1  0  0  0  0
        1 10  1  0  0  0  0
        2  5  1  0  0  0  0
        2 11  1  0  0  0  0
        2 12  1  0  0  0  0
        2 13  1  0  0  0  0
        3  4  1  0  0  0  0
        3 14  1  0  0  0  0
        3 15  1  0  0  0  0
        4  5  1  0  0  0  0
        4 16  1  0  0  0  0
        4 17  1  0  0  0  0
        5  6  1  0  0  0  0
        5  7  1  0  0  0  0
        6 18  1  0  0  0  0
        7 19  1  0  0  0  0
      M  ISO  1   1  12
      M  END

   * File contaning ``InChI`` string:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3


Examples
--------

Input file/string specification
'''''''''''''''''''''''''''''''

As shown above, ``isoenum`` command-line interface asks user
to provide one required parameter ``<path-to-ctfile-file-or-inchi-file-or-inchi-string>``
which is file or string with information required to create isotopically-resolved ``InChI``:

   * Path to ``CTfile`` (i.e. ``Molfile`` or ``SDfile``).

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol

   * Path to file containing ``InChI``.

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.inchi

   * ``InChI`` string.

   .. code-block:: none

      $ python3 -m isoenum name InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3

   or

   .. code-block:: none

      $ python3 -m isoenum name 1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3


Isotopic layer specification: specific atoms
''''''''''''''''''''''''''''''''''''''''''''

* To add isotope designation to specific atom within ``Molfile``. For example,
  if we want to add carbon 13 specification to second carbon atom:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -s C-13-2

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --specific=C-13-2

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1

* To add isotope designation to several specific atoms just repeat ``-s`` or ``--specific`` option:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -s C-13-1 -s C-13-2

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --specific=C-13-1 --specific=C-13-2

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1

   .. note::

      Since original file already contained ``ISO`` specification for the first carbon atom,
      it did not change the designation of that atom (i.e. ``i1+0`` was retained).

* To ignore existing ``ISO`` specification provide ``-i`` or ``--ignore-iso`` oprtion:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -s C-13-1 -s C-13-2 -i

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --specific=C-13-1 --specific=C-13-2 --ignore-iso

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1


Isotopic layer specification: all atoms of specific type
''''''''''''''''''''''''''''''''''''''''''''''''''''''''

* To add isotope designation to all atoms of specific type use ``-a`` or ``--all`` option:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -a C-13

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --all=C-13

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1

* To add isotope designation to different types of atoms just repeat ``-a`` or ``--all`` option
  for desired atom type:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -a C-13 -a O-18

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --all=C-13 --all=O-18

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1,6+2,7+2

* To ignore existing ``ISO`` specification combine with ``-i`` or ``--ignore-iso`` option:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -a C-13 -a O-18 -i

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --all=C-13 --all=O-18 --ignore-iso

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,3+1,4+1,5+1,6+2,7+2

* Also ``-a`` or ``--all`` option can be combined with ``-s`` or ``--specific`` option
  which has higher priority:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -a C-13 -s C-12-3 -i

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --all=C-13 --specific=C-12-3 --ignore-iso

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,3+0,4+1,5+1


Isotopic layer specification: enumerate atoms of specific type
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

* To enumerate atoms of specific type use ``-e`` or ``--enumerate`` option:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -e C-13

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --enumerate=C-13

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0

* Minimum and maximum number can be set to limit ``InChI`` generation to desired minimum and maximum
  number of atoms of specific type. For example generate all possible ``InChI`` where the number of
  carbon 13 atoms is in the range from 3 to 4:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -e C-13-3-4

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --enumerate=C-13-3-4

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+1

* To ignore existing ``ISO`` specification combine it with ``-i`` or ``ignore-iso`` option:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -e C-13-3-4 -i

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --enumerate=C-13-3-4 --ignore-iso

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,3+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i2+1,3+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i2+1,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i2+1,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i2+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i3+1,4+1,5+1

   * To enumerate multiple atom types just repeat ``-e`` or ``--enumerate`` option for desired atom type:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -e C-13-3-4 -e O-18-1-2

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --enumerate=C-13-3-4 --enumerate=O-18-1-2

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1,6+2/t5-/m0/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1,6+2/t5-/m1/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,6+2/t5-/m0/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,6+2/t5-/m1/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+1,6+2/t5-/m0/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+1,6+2/t5-/m1/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+1,6+2/t5-/m0/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+1,6+2/t5-/m1/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+1,6+2/t5-/m0/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+1,6+2/t5-/m1/s1

* Also ``-e`` (``--enumerate``) can be combined with ``-a`` (``--all``) and ``-s`` (``--specific``) options
  except ``-e`` (``--enumerate``) option cannot specify the same atom type as ``-a`` (``--all``) option.

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -e C-13-2-4 -a O-18 -s C-12-3

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --enumerate=C-13-2-4 --all=O-18 --specific=C-12-3

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0,4+1,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0,4+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+0,4+1,5+1,6+2,7+2

* It is also possible to combine ``-e`` or ``--enumerate`` option for the same element but different
  isotopes (also note that we are not specifying minimum number in this example, it will be set 0 by default).
  For, example we want to generate ``InChI`` with up to 2 carbon 12 and up to 2 carbon 13:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -e C-13-2 -e C-12-2

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --enumerate=C-13-2 --enumerate=C-12-2

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+0,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+0,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+0


Output format
'''''''''''''

* There are several output formats available:

   * ``inchi`` - which produces ``InChI`` string.
   * ``sdf`` - which produces ``SDfile`` with one or more ``Molfile`` and ``InChI`` associated with it.
   * ``mol`` - same as ``sdf``.

* To specify ``inchi`` output format (which is set to default and does not require format specification)
  use ``-f`` or ``--format`` option:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -s C-13-2 -f inchi

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --specific=C-13-2 --format=inchi

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1

* To specify ``mol`` or ``sdf`` output format:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -s C-13-2 -f sdf

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --specific=C-13-2 --format=sdf

   Output:

   .. code-block:: none

      pentane-2_2-diol
      OpenBabel04241818183D

       19 18  0  0  0  0  0  0  0  0999 V2000
          0.8564    0.0224   -0.0199   C 0  0  0  0  0  0  0  0  0  0  0  0
          5.0590   -2.7653   -0.2642   C 0  0  0  0  0  0  0  0  0  0  0  0
          2.3767    0.0633   -0.0253   C 0  0  0  0  0  0  0  0  0  0  0  0
          2.9725   -1.3472   -0.1203   C 0  0  0  0  0  0  0  0  0  0  0  0
          4.5036   -1.3472   -0.1439   C 0  0  0  0  0  0  0  0  0  0  0  0
          4.9424   -0.5621   -1.2388   O 0  0  0  0  0  0  0  0  0  0  0  0
          5.0329   -0.7920    1.0484   O 0  0  0  0  0  0  0  0  0  0  0  0
          0.4514    1.0368    0.0457   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.4813   -0.5495    0.8345   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.4733   -0.4367   -0.9365   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.7458   -3.2426   -1.1982   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.7417   -3.3903    0.5788   H 0  0  0  0  0  0  0  0  0  0  0  0
          6.1556   -2.7490   -0.2585   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.7259    0.5602    0.8869   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.7092    0.6719   -0.8743   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.5969   -1.8221   -1.0358   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.6148   -1.9367    0.7329   H 0  0  0  0  0  0  0  0  0  0  0  0
          5.0489   -1.1442   -2.0068   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.6612   -1.2841    1.7969   H 0  0  0  0  0  0  0  0  0  0  0  0
        1  3  1  0  0  0  0
        1  8  1  0  0  0  0
        1  9  1  0  0  0  0
        1 10  1  0  0  0  0
        2  5  1  0  0  0  0
        2 11  1  0  0  0  0
        2 12  1  0  0  0  0
        2 13  1  0  0  0  0
        3  4  1  0  0  0  0
        3 14  1  0  0  0  0
        3 15  1  0  0  0  0
        4  5  1  0  0  0  0
        4 16  1  0  0  0  0
        4 17  1  0  0  0  0
        5  6  1  0  0  0  0
        5  7  1  0  0  0  0
        6 18  1  0  0  0  0
        7 19  1  0  0  0  0
      M  ISO  2   1  12   2  13
      M  END
      > <InChI>
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1

      $$$$


Output file
'''''''''''

* To save generated output into a file use ``-o`` or ``--output`` option.
  For example, to save generated output in ``inchi`` format:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -a C-13 -f inchi -o outfile.inchi

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --all=C-13 --format=inchi --output=outfile.inchi

   Generated file will contain the following output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1


* To save generated output in ``mol`` or ``sdf`` format:

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol -a C-13 -f sdf -o outfile.sdf

   or

   .. code-block:: none

      $ python3 -m isoenum name tests/example_data/pentane-2_2-diol.mol --all=C-13 --format=sdf --output=outfile.sdf

   Generated file will contain the following output:

   .. code-block:: none

      pentane-2_2-diol
      OpenBabel04251811053D

       19 18  0  0  0  0  0  0  0  0999 V2000
          0.9237   -0.0881    0.1091   C 0  0  0  0  0  0  0  0  0  0  0  0
          5.1259   -2.4797    1.5667   C 0  0  0  0  0  0  0  0  0  0  0  0
          2.4438   -0.0580    0.0798   C 0  0  0  0  0  0  0  0  0  0  0  0
          3.0394   -1.2473    0.8454   C 0  0  0  0  0  0  0  0  0  0  0  0
          4.5756   -1.2658    0.8182   C 0  0  0  0  0  0  0  0  0  0  0  0
          4.9993   -1.2893   -0.5316   O 0  0  0  0  0  0  0  0  0  0  0  0
          5.1095   -0.1114    1.4395   O 0  0  0  0  0  0  0  0  0  0  0  0
          0.5176    0.7650   -0.4432   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.5500   -0.0378    1.1365   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.5406   -1.0041   -0.3524   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.8066   -3.4184    1.1046   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.8189   -2.4761    2.6168   H 0  0  0  0  0  0  0  0  0  0  0  0
          6.2250   -2.4670    1.5528   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.7928    0.8838    0.5163   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.7749   -0.0753   -0.9642   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.6598   -2.1729    0.3950   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.6864   -1.2108    1.8833   H 0  0  0  0  0  0  0  0  0  0  0  0
          5.1891   -2.2082   -0.7786   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.7262   -0.0485    2.3265   H 0  0  0  0  0  0  0  0  0  0  0  0
        1  3  1  0  0  0  0
        1  8  1  0  0  0  0
        1  9  1  0  0  0  0
        1 10  1  0  0  0  0
        2  5  1  0  0  0  0
        2 11  1  0  0  0  0
        2 12  1  0  0  0  0
        2 13  1  0  0  0  0
        3  4  1  0  0  0  0
        3 14  1  0  0  0  0
        3 15  1  0  0  0  0
        4  5  1  0  0  0  0
        4 16  1  0  0  0  0
        4 17  1  0  0  0  0
        5  6  1  0  0  0  0
        5  7  1  0  0  0  0
        6 18  1  0  0  0  0
        7 19  1  0  0  0  0
      M  ISO  5   1  12   2  13   3  13   4  13   5  13
      M  END
      > <InChI>
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1

      $$$$


Docker usage examples
~~~~~~~~~~~~~~~~~~~~~

This section contains example provided above but with the use of provided docker
container with ``isoenum`` Python package and all its dependencies instead of using
``isoenum`` Python package directly.

After you ``docker pull`` or ``docker build`` ``isoenum`` container you can verify
that it is available.

.. code-block:: none

   # docker images

You should see output similar to the following:

.. code-block:: none

   REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
   isoenum             latest              0e4c431aa519        1 day ago           862MB


* To access ``isoenum`` command-line interface from docker container:

   .. code-block:: none

      # docker run isoenum --help

Output:

   .. code-block:: none

      Isotopic enumerator (isoenum) command-line interface

      Usage:
          isoenum -h | --help
          isoenum --version
          isoenum name (<path-to-ctfile-file-or-inchi-file-or-inchi-string>)
                       [--specific=<element-isotope-position>...]
                       [--all=<element-isotope>...]
                       [--enumerate=<element-isotope-count>...]
                       [--complete | --partial]
                       [--ignore-iso]
                       [--format=<format>]
                       [--output=<path>]
                       [--verbose]

      Options:
          -h, --help                                 Show this screen.
          --verbose                                  Print more information.
          -v, --version                              Show version.
          -a, --all=<element-isotope>                Specify element and isotope, e.g. -a C-13 or --all=C-13
          -s, --specific=<element-isotope-position>  Specify element, isotope and specific position,
                                                     e.g. -s C-13-1 or --specific=C-13-1.
          -e, --enumerate=<element-isotope-min-max>  Enumerate all isotopically-resolved CTfile or InChI.
          -c, --complete                             Use complete labeling schema, i.e. every atom must specify
                                                     "ISO" property, partial labeling schema will be used otherwise
                                                     for specified labeling information only.
          -p, --partial                              Use partial labeling schema, i.e. generate labeling schema
                                                     from the provided labeling information.
          -i, --ignore-iso                           Ignore existing "ISO" specification in the CTfile or InChI.
          -f, --format=<format>                      Format of output: inchi, mol or sdf [default: inchi].
          -o, --output=<path>                        Path to output file.


Input files
-----------

We are going to use the same input files as above to generate isotopically-resolved
``InChI``. Repeated here for convenience.

   * ``Molfile`` example:

   .. code-block:: none

      pentane-2_2-diol
      OpenBabel04241814313D

       19 18  0  0  0  0  0  0  0  0999 V2000
          0.9398    0.0281    0.0594   C 0  0  0  0  0  0  0  0  0  0  0  0
          5.1399   -1.8948   -1.9819   C 0  0  0  0  0  0  0  0  0  0  0  0
          2.4621    0.0601    0.0832   C 0  0  0  0  0  0  0  0  0  0  0  0
          3.0524   -0.9348   -0.9251   C 0  0  0  0  0  0  0  0  0  0  0  0
          4.5873   -0.9132   -0.9449   C 0  0  0  0  0  0  0  0  0  0  0  0
          5.0222    0.3995   -1.2439   O 0  0  0  0  0  0  0  0  0  0  0  0
          5.1166   -1.2929    0.3146   O 0  0  0  0  0  0  0  0  0  0  0  0
          0.5343    0.7436    0.7819   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.5639   -0.9667    0.3178   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.5563    0.2945   -0.9319   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.8204   -1.6296   -2.9975   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.8268   -2.9228   -1.7657   H 0  0  0  0  0  0  0  0  0  0  0  0
          6.2362   -1.8812   -1.9694   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.8078   -0.1742    1.0938   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.7926    1.0796   -0.1484   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.6751   -0.6810   -1.9232   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.6972   -1.9418   -0.6781   H 0  0  0  0  0  0  0  0  0  0  0  0
          5.1501    0.4682   -2.2019   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.7281   -2.1498    0.5503   H 0  0  0  0  0  0  0  0  0  0  0  0
        1  3  1  0  0  0  0
        1  8  1  0  0  0  0
        1  9  1  0  0  0  0
        1 10  1  0  0  0  0
        2  5  1  0  0  0  0
        2 11  1  0  0  0  0
        2 12  1  0  0  0  0
        2 13  1  0  0  0  0
        3  4  1  0  0  0  0
        3 14  1  0  0  0  0
        3 15  1  0  0  0  0
        4  5  1  0  0  0  0
        4 16  1  0  0  0  0
        4 17  1  0  0  0  0
        5  6  1  0  0  0  0
        5  7  1  0  0  0  0
        6 18  1  0  0  0  0
        7 19  1  0  0  0  0
      M  ISO  1   1  12
      M  END

   * File contaning ``InChI`` string:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3


Docker examples
---------------

Docker input file/string specification
''''''''''''''''''''''''''''''''''''''

As shown above, ``isoenum`` command-line interface asks user
to provide one required parameter ``<path-to-ctfile-file-or-inchi-file-or-inchi-string>``
which is file or string with information required to create isotopically-resolved ``InChI``.

In order to provide input file path to ``isoenum`` docker container
you will need to mount it as volume for docker container so it can see it.


.. warning::

   You need to provide absolute path to input file, otherwise docker container
   will not be able to see it.

   For example, ``-v /absolute/path/to/input.txt:/input.txt``, where path on the
   left side of ``:`` is absolute path on host machine and path on the right side of ``:``
   is path within docker container.


To illustrate, let's invoke ``isoenum`` docker container and provide input files:

   * Path to ``CTfile`` (i.e. ``Molfile`` or ``SDfile``).

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol

   * Path to file containing ``InChI``.

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol

   * ``InChI`` string.

   .. code-block:: none

      # docker run isoenum name 'InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3'

   or

   .. code-block:: none

      # docker run isoenum name '1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3'


Docker isotopic layer specification: specific atoms
'''''''''''''''''''''''''''''''''''''''''''''''''''

* To add isotope designation to specific atom within ``Molfile``. For example,
  if we want to add carbon 13 specification to second carbon atom:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -s C-13-2

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --specific=C-13-2

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1

* To add isotope designation to several specific atoms just repeat ``-s`` or ``--specific`` option:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -s C-13-1 -s C-13-2

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --specific=C-13-1 --specific=C-13-2

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1

   .. note::

      Since original file already contained ``ISO`` specification for the first carbon atom,
      it did not change the designation of that atom (i.e. ``i1+0`` was retained).

* To ignore existing ``ISO`` specification provide ``-i`` or ``--ignore-iso`` oprtion:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -s C-13-1 -s C-13-2 -i

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --specific=C-13-1 --specific=C-13-2 --ignore-iso

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1


Docker Isotopic layer specification: all atoms of specific type
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

* To add isotope designation to all atoms of specific type use ``-a`` or ``--all`` option:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -a C-13

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --all=C-13

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1

* To add isotope designation to different types of atoms just repeat ``-a`` or ``--all`` option
  for desired atom type:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -a C-13 -a O-18

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --all=C-13 --all=O-18

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1,6+2,7+2

* To ignore existing ``ISO`` specification combine with ``-i`` or ``--ignore-iso`` option:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -a C-13 -a O-18 -i

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --all=C-13 --all=O-18 --ignore-iso

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,3+1,4+1,5+1,6+2,7+2

* Also ``-a`` or ``--all`` option can be combined with ``-s`` or ``--specific`` option
  which has higher priority:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -a C-13 -s C-12-3 -i

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --all=C-13 --specific=C-12-3 --ignore-iso

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,3+0,4+1,5+1


Docker Isotopic layer specification: enumerate atoms of specific type
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

* To enumerate atoms of specific type use ``-e`` or ``--enumerate`` option:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -e C-13

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --enumerate=C-13

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0

* Minimum and maximum number can be set to limit ``InChI`` generation to desired minimum and maximum
  number of atoms of specific type. For example generate all possible ``InChI`` where the number of
  carbon 13 atoms is in the range from 3 to 4:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -e C-13-3-4

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --enumerate=C-13-3-4

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+1

* To ignore existing ``ISO`` specification combine it with ``-i`` or ``ignore-iso`` option:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -e C-13-3-4 -i

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --enumerate=C-13-3-4 --ignore-iso

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,2+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,3+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i2+1,3+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i2+1,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i2+1,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i2+1,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i3+1,4+1,5+1

   * To enumerate multiple atom types just repeat ``-e`` or ``--enumerate`` option for desired atom type:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -e C-13-3-4 -e O-18-1-2

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --enumerate=C-13-3-4 --enumerate=O-18-1-2

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1,6+2/t5-/m0/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1,6+2/t5-/m1/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,6+2/t5-/m0/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,6+2/t5-/m1/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+1,6+2/t5-/m0/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+1,6+2/t5-/m1/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+1,6+2/t5-/m0/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+1,6+2/t5-/m1/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+1,6+2/t5-/m0/s1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+1,6+2/t5-/m1/s1

* Also ``-e`` (``--enumerate``) can be combined with ``-a`` (``--all``) and ``-s`` (``--specific``) options
  except ``-e`` (``--enumerate``) option cannot specify the same atom type as ``-a`` (``--all``) option.

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -e C-13-2-4 -a O-18 -s C-12-3

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --enumerate=C-13-2-4 --all=O-18 --specific=C-12-3

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0,4+1,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0,4+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0,5+1,6+2,7+2
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+0,4+1,5+1,6+2,7+2

* It is also possible to combine ``-e`` or ``--enumerate`` option for the same element but different
  isotopes (also note that we are not specifying minimum number in this example, it will be set 0 by default).
  For, example we want to generate ``InChI`` with up to 2 carbon 12 and up to 2 carbon 13:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -e C-13-2 -e C-12-2

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --enumerate=C-13-2 --enumerate=C-12-2

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+0,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+0,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,3+1,4+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,4+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,3+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+0,3+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,4+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0,5+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+0,4+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,5+0
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+0


Output format
'''''''''''''

* There are several output formats available:

   * ``inchi`` - which produces ``InChI`` string.
   * ``sdf`` - which produces ``SDfile`` with one or more ``Molfile`` and ``InChI`` associated with it.
   * ``mol`` - same as ``sdf``.

* To specify ``inchi`` output format (which is set to default and does not require format specification)
  use ``-f`` or ``--format`` option:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -s C-13-2 -f inchi

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --specific=C-13-2 --format=inchi

   Output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1

* To specify ``mol`` or ``sdf`` output format:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol -s C-13-2 -f sdf

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol isoenum name /pentane-2_2-diol.mol --specific=C-13-2 --format=sdf

   Output:

   .. code-block:: none

      pentane-2_2-diol
      OpenBabel04241818183D

       19 18  0  0  0  0  0  0  0  0999 V2000
          0.8564    0.0224   -0.0199   C 0  0  0  0  0  0  0  0  0  0  0  0
          5.0590   -2.7653   -0.2642   C 0  0  0  0  0  0  0  0  0  0  0  0
          2.3767    0.0633   -0.0253   C 0  0  0  0  0  0  0  0  0  0  0  0
          2.9725   -1.3472   -0.1203   C 0  0  0  0  0  0  0  0  0  0  0  0
          4.5036   -1.3472   -0.1439   C 0  0  0  0  0  0  0  0  0  0  0  0
          4.9424   -0.5621   -1.2388   O 0  0  0  0  0  0  0  0  0  0  0  0
          5.0329   -0.7920    1.0484   O 0  0  0  0  0  0  0  0  0  0  0  0
          0.4514    1.0368    0.0457   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.4813   -0.5495    0.8345   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.4733   -0.4367   -0.9365   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.7458   -3.2426   -1.1982   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.7417   -3.3903    0.5788   H 0  0  0  0  0  0  0  0  0  0  0  0
          6.1556   -2.7490   -0.2585   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.7259    0.5602    0.8869   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.7092    0.6719   -0.8743   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.5969   -1.8221   -1.0358   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.6148   -1.9367    0.7329   H 0  0  0  0  0  0  0  0  0  0  0  0
          5.0489   -1.1442   -2.0068   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.6612   -1.2841    1.7969   H 0  0  0  0  0  0  0  0  0  0  0  0
        1  3  1  0  0  0  0
        1  8  1  0  0  0  0
        1  9  1  0  0  0  0
        1 10  1  0  0  0  0
        2  5  1  0  0  0  0
        2 11  1  0  0  0  0
        2 12  1  0  0  0  0
        2 13  1  0  0  0  0
        3  4  1  0  0  0  0
        3 14  1  0  0  0  0
        3 15  1  0  0  0  0
        4  5  1  0  0  0  0
        4 16  1  0  0  0  0
        4 17  1  0  0  0  0
        5  6  1  0  0  0  0
        5  7  1  0  0  0  0
        6 18  1  0  0  0  0
        7 19  1  0  0  0  0
      M  ISO  2   1  12   2  13
      M  END
      > <InChI>
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1

      $$$$


Docker output file
''''''''''''''''''

In case of using ``isoenum`` docker container both input file and output file
must be mounted as volumes for docker container.

.. warning::

   You need to provide absolute path to input and output files, otherwise docker container
   will not be able to see them.

   For example, ``-v /absolute/path/to/input.txt:/input.txt``, where path on the
   left side of ``:`` is absolute path on host machine and path on the
   right side of ``:`` is path within docker container.

   The same way, you will need to create an empty text file and mount it as volume,
   so docker container can write to it, ``-v /absolute/path/to/output.txt:/output.txt``,
   where path on the left side of ``:`` is absolute path on host machine and path on the
   right side of ``:`` is path within docker container.


* To save generated output into a file use ``-o`` or ``--output`` option.
  For example, to save generated output in ``inchi`` format:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol \
                   -v /absolute/path/to/outfile.inchi:/outfile.inchi \
                   isoenum name /pentane-2_2-diol.mol -a C-13 -f inchi -o /outfile.inchi

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol \
                   -v /absolute/path/to/outfile.inchi:/outfile.inchi \
                   isoenum name /pentane-2_2-diol.mol --all=C-13 --format=inchi --output=/outfile.inchi

   Generated file will contain the following output:

   .. code-block:: none

      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1


* To save generated output in ``mol`` or ``sdf`` format:

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol \
                   -v /absolute/path/to/outfile.sdf:/outfile.sdf \
                   isoenum name /pentane-2_2-diol.mol -a C-13 -f sdf -o /outfile.sdf

   or

   .. code-block:: none

      # docker run -v /absolute/path/to/pentane-2_2-diol.mol:/pentane-2_2-diol.mol \
                   -v /absolute/path/to/outfile.sdf:/outfile.sdf \
                   isoenum name /pentane-2_2-diol.mol --all=C-13 --format=sdf --output=/outfile.sdf

   Generated file will contain the following output:

   .. code-block:: none

      pentane-2_2-diol
      OpenBabel04251811053D

       19 18  0  0  0  0  0  0  0  0999 V2000
          0.9237   -0.0881    0.1091   C 0  0  0  0  0  0  0  0  0  0  0  0
          5.1259   -2.4797    1.5667   C 0  0  0  0  0  0  0  0  0  0  0  0
          2.4438   -0.0580    0.0798   C 0  0  0  0  0  0  0  0  0  0  0  0
          3.0394   -1.2473    0.8454   C 0  0  0  0  0  0  0  0  0  0  0  0
          4.5756   -1.2658    0.8182   C 0  0  0  0  0  0  0  0  0  0  0  0
          4.9993   -1.2893   -0.5316   O 0  0  0  0  0  0  0  0  0  0  0  0
          5.1095   -0.1114    1.4395   O 0  0  0  0  0  0  0  0  0  0  0  0
          0.5176    0.7650   -0.4432   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.5500   -0.0378    1.1365   H 0  0  0  0  0  0  0  0  0  0  0  0
          0.5406   -1.0041   -0.3524   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.8066   -3.4184    1.1046   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.8189   -2.4761    2.6168   H 0  0  0  0  0  0  0  0  0  0  0  0
          6.2250   -2.4670    1.5528   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.7928    0.8838    0.5163   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.7749   -0.0753   -0.9642   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.6598   -2.1729    0.3950   H 0  0  0  0  0  0  0  0  0  0  0  0
          2.6864   -1.2108    1.8833   H 0  0  0  0  0  0  0  0  0  0  0  0
          5.1891   -2.2082   -0.7786   H 0  0  0  0  0  0  0  0  0  0  0  0
          4.7262   -0.0485    2.3265   H 0  0  0  0  0  0  0  0  0  0  0  0
        1  3  1  0  0  0  0
        1  8  1  0  0  0  0
        1  9  1  0  0  0  0
        1 10  1  0  0  0  0
        2  5  1  0  0  0  0
        2 11  1  0  0  0  0
        2 12  1  0  0  0  0
        2 13  1  0  0  0  0
        3  4  1  0  0  0  0
        3 14  1  0  0  0  0
        3 15  1  0  0  0  0
        4  5  1  0  0  0  0
        4 16  1  0  0  0  0
        4 17  1  0  0  0  0
        5  6  1  0  0  0  0
        5  7  1  0  0  0  0
        6 18  1  0  0  0  0
        7 19  1  0  0  0  0
      M  ISO  5   1  12   2  13   3  13   4  13   5  13
      M  END
      > <InChI>
      InChI=1S/C5H12O2/c1-3-4-5(2,6)7/h6-7H,3-4H2,1-2H3/i1+0,2+1,3+1,4+1,5+1

      $$$$
