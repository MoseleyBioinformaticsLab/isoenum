#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum.fileio
~~~~~~~~~~~~~~

This module provides routines to generate ``CTfile`` objects and
convert ``CTfile`` objects into ``InChI`` and vice versa.
"""

import os
import tempfile

import requests
import ctfile

from . import openbabel
from . import utils


def create_ctfile(path):
    """Guesses what type of path is provided, i.e. is it existing file in ``Molfile`` format, 
    existing file in ``SDfile`` file format, existing file containing ``InChI`` string, 
    or ``InChI`` string and tries to create ``CTfile`` object.

    :param str path: Path to ``Molfile``, ``SDfile``, ``InChI``, or ``InChI`` string.
    :return: Subclass of :class:`~ctfile.ctfile.CTfile` object.
    :rtype: :class:`~ctfile.ctfile.CTfile`.
    """
    if os.path.isfile(path):
        with open(path, 'r') as infile:
            string = infile.read()

            try:
                return ctfile.loadstr(string)
            except IndexError:
                ctf = create_ctfile_from_inchi_file(path=path)

    elif utils.is_url(path):
        try:
            return ctfile.read_file(path)
        except IndexError:
            inchi_str = requests.get(path).text
            ctf = create_ctfile_from_inchi_str(inchi_str=inchi_str)

    else:
        ctf = create_ctfile_from_inchi_str(inchi_str=path)

    if isinstance(ctf, ctfile.Molfile) or isinstance(ctf, ctfile.SDfile):
        return ctf
    else:
        raise ValueError('Cannot create "CTfile" object.')


def create_ctfile_from_ctfile_str(ctfile_str):
    """Create ``CTfile`` object from ``CTfile`` string.

    :param str ctfile_str: ``CTfile`` string. 
    :return: Subclass of :class:`~ctfile.ctfile.CTfile` object.
    :rtype: :class:`~ctfile.ctfile.CTfile`. 
    """
    return ctfile.loadstr(ctfile_str)


def create_ctfile_from_inchi_str(inchi_str):
    """Create ``CTfile`` object from ``InChI`` string.

    :param str inchi_str: ``InChI`` string. 
    :return: Subclass of :class:`~ctfile.ctfile.CTfile` object.
    :rtype: :class:`~ctfile.ctfile.CTfile`. 
    """
    if not inchi_str.lower().startswith('inchi='):
        inchi_str = 'InChI={}'.format(inchi_str)
    else:
        inchi_str = inchi_str

    with tempfile.NamedTemporaryFile(mode='w') as tempfh:
        tempfh.write(inchi_str)
        tempfh.flush()
        return create_ctfile_from_inchi_file(path=tempfh.name)


def create_ctfile_from_inchi_file(path):
    """Creates ``CTfile`` from ``InChI`` identifier.

    :param str path: Path to file containing ``InChI`` identifier.
    :return: Subclass of :class:`~ctfile.ctfile.CTfile` object.
    :rtype: :class:`~ctfile.ctfile.CTfile`.
    """
    with tempfile.NamedTemporaryFile() as tempfh:
        openbabel.inchi_to_mol(infilename=path, outfilename=tempfh.name)
        with open(tempfh.name, 'r') as infile:
            return ctfile.load(infile)


def create_inchi_from_ctfile_obj(ctf, **options):
    """Create ``InChI`` from ``CTfile`` instance.

    :param ctf: Instance of :class:`~ctfile.ctfile.CTfile`.
    :type ctf: :class:`~ctfile.ctfile.CTfile`
    :return: ``InChI`` string.
    :rtype: :py:class:`str` 
    """
    if 'CHG' in ctf['Ctab']['CtabPropertiesBlock']:
        options.update({'fixedH':'-xF'})

    with tempfile.NamedTemporaryFile(mode='w') as moltempfh, tempfile.NamedTemporaryFile(mode='r') as inchitempfh:
        moltempfh.write(ctf.writestr(file_format='ctfile'))
        moltempfh.flush()
        openbabel.mol_to_inchi(infilename=moltempfh.name, outfilename=inchitempfh.name, **options)
        inchi_result = inchitempfh.read()
        return inchi_result.strip()


def normalize_ctfile_obj(ctf):
    """Normalize ``CTfile`` object . 
    
    :param ctf: ``CTfile`` object.
    :type ctf: :class:`~ctfile.ctfile.CTfile`
    :return: Normalized ``CTfile`` object.
    :rtype: :class:`~ctfile.ctfile.CTfile`
    """
    inchi_str = create_inchi_from_ctfile_obj(ctf)
    return create_ctfile_from_inchi_str(inchi_str=inchi_str)


def create_empty_sdfile_obj():
    """Create empty ``SDfile`` object.
    
    :return: ``SDfile`` object.
    :rtype: :class:`~ctfile.ctfile.SDfile`
    """
    return ctfile.SDfile()


def create_empty_molfile_obj():
    """Create empty ``Molfile`` object.

    :return: ``Molfile`` object.
    :rtype: :class:`~ctfile.ctfile.Molfile`
    """
    return ctfile.Molfile()
