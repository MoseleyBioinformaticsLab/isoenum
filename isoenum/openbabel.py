#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum.openbabel
~~~~~~~~~~~~~~~~~

This module provides :func:`~isoenum.openbabel.mol_to_inchi` and :func:`~isoenum.openbabel.inchi_to_mol`
to convert between ``InChI`` and ``CTfile`` formatted files. 
"""

import subprocess


def _test_openbabel():
    """Test if Open Babel software is installed.
    
    :return: None.
    :rtype: :py:obj:`None`
    """
    try:
        openbabel_version_test = subprocess.check_output(['obabel', '-V'])
        openbabel_version = openbabel_version_test.decode('utf-8')
        if not openbabel_version.startswith('Open Babel'):
            raise SystemExit('Open Babel version information cannot be found: {}'.format(openbabel_version))
    except OSError:
        raise SystemExit('Open Babel software is not installed, exiting. '
                         'See installation instructions to get Open Babel '
                         'software for your system: http://openbabel.org/wiki/Get_Open_Babel')


def mol_to_inchi(infilename, outfilename, **options):
    """Convert ``Molfile`` to ``InChI`` identifier.
    
    :param str infilename: Input file name.
    :param str outfilename: Output file name.
    :param options: Key-value options to be passed to Open Babel.
    :return: None.
    :rtype: :py:obj:`None`
    """
    _test_openbabel()

    if options:
        subprocess.check_output(['obabel', '-imol', '{}'.format(infilename),
                                 '-oinchi', '-O{}'.format(outfilename),
                                 '{}'.format(' '.join(options.values()))], shell=False)
    else:
        subprocess.check_output(['obabel', '-imol', '{}'.format(infilename),
                                 '-oinchi', '-O{}'.format(outfilename)], shell=False)


def inchi_to_mol(infilename, outfilename):
    """Convert ``InChI`` identifier to ``Molfile``.
    
    :param str infilename: Input file name.
    :param str outfilename: Output file name.
    :return: None.
    :rtype: :py:obj:`None`
    """
    _test_openbabel()

    subprocess.check_output(['obabel', '-iinchi', '{}'.format(infilename),
                             '-omol', '-O{}'.format(outfilename), '--gen3D'], shell=False)
