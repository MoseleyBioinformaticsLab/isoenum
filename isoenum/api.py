#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum.api
~~~~~~~~~~~

This module provides routines to augment ``CTfile`` objects 
with additional information and used by ``isoenum`` package CLI. 
"""

import tempfile
from collections import Counter
from collections import defaultdict
from collections import OrderedDict

import more_itertools

from . import fileio
from . import labeling
from . import nmr
from . import openbabel
from .conf import isotopes_conf


def iso(path_or_id, specific_opt, all_opt, enumerate_opt, complete_opt, ignore_iso_opt):
    """Create isotopically-resolved ``SDfile``.

    :param str path_or_id: Path to ``CTfile`` or file identifier.
    :param list specific_opt: List of isotopes per specific element type and position.
    :param list all_opt: List of isotopes for specific element type. 
    :param list enumerate_opt: List of isotopes to perform enumeration. 
    :param complete_opt: Identify if every element need to have isotope information.
    :type complete_opt: py:obj:`True` or py:obj:`False`  
    :param ignore_iso_opt: Ignore existing isotope information or not.
    :type ignore_iso_opt: py:obj:`True` or py:obj:`False`
    :return: instance of ``SDfile``.
    :rtype: :class:`ctfile.ctfile.SDfile`
    """
    ctfile = fileio.create_ctfile(path_or_id=path_or_id)
    sdfile = fileio.create_empty_sdfile_obj()

    for molfile in ctfile.molfiles:
        existing_opt = ['{}:{}:{}'.format(isotope['isotope'], isotope['atom_symbol'], isotope['atom_number'])
                        for isotope in molfile.iso]

        specific_iso = _check_specific_opt(isotopes=specific_opt, isotopes_conf=isotopes_conf, ctfile=molfile)
        existing_iso = _check_specific_opt(isotopes=existing_opt, isotopes_conf=isotopes_conf, ctfile=molfile)
        all_iso = _check_all_opt(isotopes=all_opt, isotopes_conf=isotopes_conf, ctfile=molfile)
        enumerate_iso = _check_enumerate_opt(enumerate_opt=enumerate_opt, all_iso=all_iso,
                                             isotopes_conf=isotopes_conf, ctfile=molfile)

        labeling_schemas = labeling.create_labeling_schema(complete_labeling_schema=complete_opt,
                                                           ignore_existing_isotopes=ignore_iso_opt,
                                                           all_iso=all_iso, specific_iso=specific_iso,
                                                           existing_iso=existing_iso, enumerate_iso=enumerate_iso,
                                                           isotopes_conf=isotopes_conf, ctfile=molfile)

        for labeling_schema in labeling_schemas:
            ctab_iso_layer_property = []
            sdfile_data = OrderedDict()
            for entry in labeling_schema:
                ctab_iso_layer_property.append((entry['position'], entry['isotope']))

            ctab_iso_layer_property = sorted(ctab_iso_layer_property, key=lambda x: int(x[0]))
            molfile.replace_ctab_property(ctab_property_name='ISO', values=ctab_iso_layer_property)
            new_molfile = fileio.create_ctfile_from_ctfile_str(ctfile_str=molfile.writestr(file_format='ctfile'))

            sdfile_data.setdefault('InChI', []).append('{}'.format(fileio.create_inchi_from_ctfile_obj(molfile)))
            sdfile.add_molfile(molfile=new_molfile, data=sdfile_data)

    return sdfile


def chg(path_or_id, atom_states):
    """Create ``SDfile`` with charge information.

    :param str path_or_id: Path to ``CTfile`` or file identifier. 
    :param list atom_states: List of charges for specific elements. 
    :return: instance of ``SDfile``.
    :rtype: :class:`ctfile.ctfile.SDfile`
    """
    ctfile = fileio.create_ctfile(path_or_id=path_or_id)
    sdfile = fileio.create_empty_sdfile_obj()

    for molfile in ctfile.molfiles:
        sdfile_data = OrderedDict()
        for state in atom_states:
            try:
                atom_symbol, atom_number, charge = state.split(':')
            except ValueError:
                raise ValueError('Incorrect ionization specification, use "element:position:charge" format.')

            molfile.add_charge(atom_symbol=atom_symbol, atom_number=atom_number, charge=charge)

        new_molfile = fileio.create_ctfile_from_ctfile_str(ctfile_str=molfile.writestr(file_format='ctfile'))
        sdfile_data.setdefault('InChI', []).append('{}'.format(fileio.create_inchi_from_ctfile_obj(ctf=molfile)))
        sdfile.add_molfile(molfile=new_molfile, data=sdfile_data)

    return sdfile


def iso_nmr(path_or_id, experiment_type, couplings, decoupled, subset):
    """Create isotopically-resolved ``SDfile`` assuming specific NMR experiment type.

    :param str path_or_id: Path to ``CTfile`` or file identifier.
    :param str experiment_type: NMR experiment type (1D1H of 1DCHSQC). 
    :param list couplings: What couplings to include?
    :param list decoupled: What elements are decoupled?
    :param subset: Create subsets?
    :type subset: py:obj:`True` or py:obj:`False`
    :return: instance of ``SDfile``.
    :rtype: :class:`ctfile.ctfile.SDfile`
    """
    ctfile = fileio.create_ctfile(path_or_id=path_or_id)
    sdfile = fileio.create_empty_sdfile_obj()
    nmr_experiment = nmr.create_nmr_experiment(name=experiment_type, couplings=couplings, decoupled=decoupled)

    for molfile in ctfile.molfiles:
        molfile = fileio.normalize_ctfile_obj(molfile)
        coupling_combinations = nmr_experiment.generate_coupling_combinations(molfile=molfile, subset=subset)

        for coupling_combination in coupling_combinations:
            ctab_iso_layer_property = []
            sdfile_data = OrderedDict()

            for coupling in coupling_combination:
                for atom in more_itertools.flatten(coupling.coupling_path):
                    if atom.atom_symbol in coupling.nmr_active_atoms:
                        ctab_iso_layer_property.append((str(atom.atom_number), str(atom.isotope)))

                sdfile_data.setdefault('CouplingType', []).append(coupling.name)

            ctab_iso_layer_property = sorted(ctab_iso_layer_property, key=lambda x: int(x[0]))
            molfile.replace_ctab_property(ctab_property_name='ISO', values=ctab_iso_layer_property)
            new_molfile = fileio.create_ctfile_from_ctfile_str(ctfile_str=molfile.writestr(file_format='ctfile'))

            sdfile_data.setdefault('InChI', []).append(
                '{}'.format(fileio.create_inchi_from_ctfile_obj(ctf=new_molfile)))
            sdfile.add_molfile(molfile=new_molfile, data=sdfile_data)

    return sdfile


def _check_specific_opt(isotopes, isotopes_conf, ctfile):
    """Check if `specific` option is consistent.

    :param list isotopes: Option that specifies isotopes.
    :param dict isotopes_conf: Default isotopes configuration.
    :param ctfile: Instance of ``Molfile``. 
    :type ctfile: :class:`~ctfile.ctfile.Molfile`
    :return: :py:class:`dict` with position specific labeling if consistent, raises error otherwise.
    :rtype: :py:class:`dict` or :py:class:`ValueError`
    """
    position_atom = defaultdict(list)
    allowed_atom_symbols = [atom.atom_symbol for atom in ctfile.atoms]
    positions = [atom.atom_number for atom in ctfile.atoms]
    ctfile_position_atom = dict(zip(positions, allowed_atom_symbols))
    specific_iso = {}

    for isotopestr in isotopes:

        try:
            isotope, atom, position = isotopestr.split(':')
        except ValueError:
            raise ValueError('Incorrect isotope specification, use "isotope:element:position" format.')

        if atom not in allowed_atom_symbols:
            raise ValueError('Incorrect atom "{}" provided.'.format(atom))

        if isotope not in isotopes_conf[atom]["isotopes"]:
            raise ValueError('Incorrect isotope "{}" provided for atom "{}".'.format(isotope, atom))

        if ctfile_position_atom[position] != atom:
            raise ValueError('There is no "{}" atom at position "{}"'.format(atom, position))

        position_atom[position].append('{}-{}'.format(atom, isotope))
        specific_iso[position] = {'atom_symbol': atom, 'isotope': isotope, 'position': position}

    if all(len(isotopes) == 1 for isotopes in position_atom.values()):
        return specific_iso
    else:
        raise ValueError('"specific" option can only specify single isotope per atom position.')


def _check_all_opt(isotopes, isotopes_conf, ctfile):
    """Check if `all` option is consistent.

    :param list isotopes: Option that specifies isotopes.
    :param dict isotopes_conf: Default isotopes configuration.
    :param ctfile: Instance of ``Molfile``. 
    :type ctfile: :class:`~ctfile.ctfile.Molfile`
    :return: :py:class:`dict` with position specific labeling if consistent, raises error otherwise.
    :rtype: :py:class:`dict` or :py:class:`ValueError`
    """
    allowed_atom_symbols = [atom.atom_symbol for atom in ctfile.atoms]
    positions = [atom.atom_number for atom in ctfile.atoms]
    position_atom = dict(zip(positions, allowed_atom_symbols))
    atom_isotope = defaultdict(list)
    all_iso = {}

    for isotopestr in isotopes:

        try:
            isotope, atom = isotopestr.split(':')
        except ValueError:
            raise ValueError('Incorrect isotope specification, use "isotope:element" format.')

        if atom not in allowed_atom_symbols:
            raise ValueError('Incorrect atom "{}" provided.'.format(atom))

        if isotope not in isotopes_conf[atom]["isotopes"]:
            raise ValueError('Incorrect isotope "{}" provided for atom "{}".'.format(isotope, atom))

        atom_isotope[atom].append(isotope)

        for position, ctfile_atom in position_atom.items():
            if atom == ctfile_atom:
                all_iso[position] = {'atom_symbol': atom, 'isotope': isotope, 'position': position}

    if all(len(isotopes) == 1 for isotopes in atom_isotope.values()):
        return all_iso
    else:
        raise ValueError('"all" option can only specify single isotope per atom type.')


def _check_enumerate_opt(enumerate_opt, all_iso, isotopes_conf, ctfile):
    """Check if `enumerate` option is consistent.

    :param list enumerate_param: Option that specifies isotopes.
    :param dict all_param: Check for consistency, `enumerate` are not compatible with `all` for the same atom.
    :param dict isotopes_conf: Default isotopes configuration. 
    :param ctfile: Instance of ``Molfile``. 
    :type ctfile: :class:`~ctfile.ctfile.Molfile`
    :return: :py:class:`list` with position specific labeling if consistent, raises error otherwise.
    :rtype: :py:class:`list` or :py:class:`ValueError`
    """
    atom_counter = Counter([atom.atom_symbol for atom in ctfile.atoms])
    allowed_atom_symbols = [atom.atom_symbol for atom in ctfile.atoms]
    all_param_atoms = [entry['atom_symbol'] for entry in all_iso.values()]
    enumerate_iso = []

    for isotopestr in enumerate_opt:

        try:
            isotope, atom, min_count, max_count = isotopestr.split(':')

        except ValueError:
            try:
                isotope, atom, max_count = isotopestr.split(':')
                min_count = 0

            except ValueError:
                try:
                    isotope, atom = isotopestr.split(':')
                    max_count = atom_counter[atom]
                    min_count = 0

                except ValueError:
                    raise ValueError('Incorrect isotope specification, use "isotope:element:min:max",'
                                     '"isotope:element:max" or "isotope:element" format.')

        enumerate_iso.append({'atom_symbol': atom, 'isotope': isotope,
                              'min': int(min_count), 'max': int(max_count)})

        if atom in all_param_atoms:
            raise ValueError('"enumerate" and "all" options are not compatible for atom: "{}"'.format(atom))

        if atom not in allowed_atom_symbols:
            raise ValueError('Incorrect atom "{}" provided.'.format(atom))

        if isotope not in isotopes_conf[atom]['isotopes']:
            raise ValueError('Incorrect isotope "{}" provided for atom "{}".'.format(isotope, atom))

        if int(max_count) > atom_counter[atom]:
            raise ValueError('Incorrect count "{}" provided for atom "{}".'.format(max_count, atom))

    return enumerate_iso


def visualize(path_or_id, output_path, output_format='svg', **options):
    """Visualize ``CTfile`` object.

    :param str path_or_id: Path to ``CTfile`` or file identifier.
    :type ctfile: :class:`~ctfile.ctfile.Molfile` or :class:`~ctfile.ctfile.SDfile`
    :param str output_format: Image output format. 
    :param str output_path: Image output path.
    """
    ctfile = fileio.create_ctfile(path_or_id=path_or_id)

    with tempfile.NamedTemporaryFile(mode='w') as tempfh:
        tempfh.write(ctfile.writestr(file_format='ctfile'))
        tempfh.flush()

        openbabel.convert(input_file_path=tempfh.name,
                          output_file_path=output_path,
                          input_format='mol',
                          output_format=output_format,
                          **options)
