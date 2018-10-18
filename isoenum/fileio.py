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

import ctfile
import requests

from . import openbabel
from . import utils


def create_ctfile(path_or_id, xyx_coordinates='--gen2D', explicit_hydrogens='-h'):
    """Guess what type of path is provided, i.e. is it existing file in ``Molfile`` format, 
    existing file in ``SDfile`` file format, existing file containing ``InChI`` string, 
    or ``InChI`` string and tries to create ``CTfile`` object.

    :param str path_or_id: Path to ``Molfile``, ``SDfile``, ``InChI``, or ``InChI`` string.
    :param str xyx_coordinates: Option that generates x, y, z coordinates (e.g., "--gen2D" or "--gen3D").
    :param str explicit_hydrogens: Option that makes hydrogens atoms explicit when generating ``CTfile`` object.
    :return: Subclass of :class:`~ctfile.ctfile.CTfile` object.
    :rtype: :class:`~ctfile.ctfile.CTfile`
    """
    if os.path.isfile(path_or_id):
        with open(path_or_id, 'r') as infile:
            try:
                return ctfile.load(infile)
            except IndexError:
                return create_ctfile_from_identifier_file(path_or_id,
                                                          xyz_coordinates=xyx_coordinates,
                                                          explicit_hydrogens=explicit_hydrogens)

    elif utils.is_url(path_or_id):
        try:
            return ctfile.read_file(path_or_id)
        except IndexError:
            identifier_str = requests.get(path_or_id).text
            ctf = create_ctfile_from_identifier_str(identifier_str=identifier_str,
                                                    xyx_coordinates=xyx_coordinates,
                                                    explicit_hydrogens=explicit_hydrogens)
    else:
        ctf = create_ctfile_from_identifier_str(identifier_str=path_or_id,
                                                xyx_coordinates=xyx_coordinates,
                                                explicit_hydrogens=explicit_hydrogens)
    # if ctf:
    #     return ctf
    # else:
    #     raise ValueError('Cannot create "CTfile" object, empty object.')
    return ctf


def create_ctfile_from_ctfile_str(ctfile_str):
    """Create ``CTfile`` object from ``CTfile`` string.

    :param str ctfile_str: ``CTfile`` string. 
    :return: Subclass of :class:`~ctfile.ctfile.CTfile` object.
    :rtype: :class:`~ctfile.ctfile.CTfile` 
    """
    return ctfile.loadstr(ctfile_str)


def create_ctfile_from_identifier_file(path, output_format='mol', **options):
    """Create ``CTfile`` instance from ``InChI`` or ``SMILES`` identifier file.

    :param str path: Path to file containing ``InChI`` or ``SMILES`` identifier.
    :param str output_format: Output file format used by Open Babel to generate ``CTfile``.
    :param options: Additional options to be passed to Open Babel.
    :return: Subclass of :class:`~ctfile.ctfile.CTfile` object.
    :rtype: :class:`~ctfile.ctfile.CTfile`
    """
    with open(path, 'r') as infile:
        input_format = guess_identifier_format(identifier_str=infile.read())

    with tempfile.NamedTemporaryFile() as tempfh:
        openbabel.convert(input_file_path=path,
                          output_file_path=tempfh.name,
                          input_format=input_format,
                          output_format=output_format,
                          **options)

        with open(tempfh.name, 'r') as infile:
            return ctfile.load(infile)


def create_ctfile_from_identifier_str(identifier_str, output_format='mol', **options):
    """Create ``CTfile`` instance from ``InChI`` or ``SMILES`` identifier string.

    :param str identifier_str: ``InChI`` or ``SMILES`` identifier string.
    :param str output_format: Output file format used by Open Babel to generate ``CTfile``.
    :param options: Additional options to be passed to Open Babel.
    :return: Subclass of :class:`~ctfile.ctfile.CTfile` object.
    :rtype: :class:`~ctfile.ctfile.CTfile`
    """
    with tempfile.NamedTemporaryFile(mode='w') as tempfh:
        tempfh.write(identifier_str)
        tempfh.flush()
        return create_ctfile_from_identifier_file(path=tempfh.name, output_format=output_format, **options)


def guess_identifier_format(identifier_str):
    """Guess identifier format.

    :param str identifier_str: Chemical identifier string.
    :return: 'inchi' or 'smiles' string.
    :rtype: :py:class:`str`
    """
    if identifier_str.startswith('InChI='):
        return 'inchi'
    else:
        return 'smiles'


def create_inchi_from_ctfile_obj(ctf, **options):
    """Create ``InChI`` from ``CTfile`` instance.

    :param ctf: Instance of :class:`~ctfile.ctfile.CTfile`.
    :type ctf: :class:`~ctfile.ctfile.CTfile`
    :return: ``InChI`` string.
    :rtype: :py:class:`str` 
    """
    if 'CHG' in ctf['Ctab']['CtabPropertiesBlock']:
        options.update({'fixedH': '-xF'})

    with tempfile.NamedTemporaryFile(mode='w') as moltempfh, tempfile.NamedTemporaryFile(mode='r') as inchitempfh:
        moltempfh.write(ctf.writestr(file_format='ctfile'))
        moltempfh.flush()
        openbabel.convert(input_file_path=moltempfh.name,
                          output_file_path=inchitempfh.name,
                          input_format='mol',
                          output_format='inchi',
                          **options)
        inchi_result = inchitempfh.read()
        return inchi_result.strip()


def normalize_ctfile_obj(ctf, xyx_coordinates='--gen2D', explicit_hydrogens='-h'):
    """Normalize ``CTfile`` object.

    :param ctf: ``CTfile`` object.
    :type ctf: :class:`~ctfile.ctfile.CTfile`
    :return: Normalized ``CTfile`` object.
    :rtype: :class:`~ctfile.ctfile.CTfile`
    """
    identifier_str = create_inchi_from_ctfile_obj(ctf)
    return create_ctfile_from_identifier_str(identifier_str=identifier_str,
                                             xyx_coordinates=xyx_coordinates,
                                             explicit_hydrogens=explicit_hydrogens)


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
