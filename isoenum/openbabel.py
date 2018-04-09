#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum.openbabel
~~~~~~~~~~~~~~~~~

This module provides :func:`~isoenum.openbabel.mol_to_inchi` and :func:`~isoenum.openbabel.inchi_to_mol`
to convert between ``InChI`` and ``CTfile`` formatted files. 
"""

import subprocess


try:
    openbabel_version_test = subprocess.run(['obabel', '-V'], stdout=subprocess.PIPE)
    if not openbabel_version_test.returncode == 0:
        raise SystemExit
except FileNotFoundError:
    print('Open Babel software is not installed, exiting.')
    raise SystemExit


def mol_to_inchi(infilename, outfilename):
    """Convert ``Molfile`` to ``InChI`` identifier.
    
    :param str infilename: Input file name.
    :param str outfilename: Output file name.
    :return: None.
    :rtype: :py:obj:`None`
    """
    result = subprocess.run(['obabel', '-imol', '{}'.format(infilename),
                             '-oinchi', '-O{}'.format(outfilename)], stdout=subprocess.PIPE)


def inchi_to_mol(infilename, outfilename):
    """Convert ``InChI`` identifier to ``Molfile``.
    
    :param str infilename: Input file name.
    :param str outfilename: Output file name.
    :return: None.
    :rtype: :py:obj:`None`
    """
    result = subprocess.run(['obabel', '-iinchi', '{}'.format(infilename),
                             '-omol', '-O{}'.format(outfilename), '--gen3D'], stdout=subprocess.PIPE)
