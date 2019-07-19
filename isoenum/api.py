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


def iso(path_or_id, specific_opt=None, all_opt=None, enumerate_opt=None, complete_opt=False, ignore_iso_opt=False):
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

    if specific_opt is None:
        specific_opt = []

    if all_opt is None:
        all_opt = []

    if enumerate_opt is None:
        enumerate_opt = []

    for molfile in ctfile.molfiles:
        existing_opt = ['{}:{}:{}'.format(atom.isotope, atom.atom_symbol, atom.atom_number)
                        for atom in molfile.atoms if atom.isotope]

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
            sdfile_data = OrderedDict()
            new_molfile = fileio.create_ctfile_from_ctfile_str(ctfile_str=molfile.writestr(file_format='ctfile'))

            for isotope_spec in labeling_schema:
                new_molfile.atom_by_number(atom_number=isotope_spec['atom_number']).isotope = isotope_spec['isotope']

            sdfile_data.setdefault('InChI', []).append('{}'.format(fileio.create_inchi_from_ctfile_obj(new_molfile)))
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
            sdfile_data = OrderedDict()

            ctab_iso_layer = []
            for coupling in coupling_combination:
                for atom in more_itertools.flatten(coupling.coupling_path):
                    if atom.atom_symbol in coupling.nmr_active_atoms:
                        ctab_iso_layer.append({'atom_number': str(atom.atom_number),
                                               'isotope': str(atom.isotope)})

                sdfile_data.setdefault('CouplingType', []).append(coupling.name)

            new_molfile = create_new_molfile(molfile=molfile, ctab_iso_layer=ctab_iso_layer)

            sdfile_data.setdefault('InChI', []).append(
                '{}'.format(fileio.create_inchi_from_ctfile_obj(ctf=new_molfile)))
            sdfile.add_molfile(molfile=new_molfile, data=sdfile_data)

    annotate_me_groups(ctfile=sdfile)
    return sdfile


def coupling_descr(coupling_types):
    """Concatenate a list of coupling types into coupling description string.

    :param coupling_types: List of coupling types.
    :return: Coupling description string.
    :rtype: :py:class:`str`
    """
    return " + ".join([coupling_type.split("]")[1] for coupling_type in coupling_types])


def create_new_molfile(molfile, ctab_iso_layer):
    """Create new `Molfile` instance with new isotopic labeling specification.

    :param ctfile: `Molfile` instance.
    :type ctfile: :class:`~ctfile.ctfile.Molfile`
    :param list ctab_iso_layer: Isotopic layer specification.
    :return: New `Molfile` instance.
    :rtype: :class:`~ctfile.ctfile.Molfile`
    """
    new_molfile = fileio.create_ctfile_from_ctfile_str(ctfile_str=molfile.writestr(file_format='ctfile'))
    for isotope_spec in ctab_iso_layer:
        new_molfile.atom_by_number(atom_number=isotope_spec['atom_number']).isotope = isotope_spec['isotope']
    return new_molfile


def create_aggregate_molfile(ctfile, entry_ids):
    """Create aggregate `Molfile` that has isotopic labeling from all associated entry ids.

    :param ctfile: `SDfile` instance.
    :type ctfile: :class:`~ctfile.ctfile.SDfile`
    :param list entry_ids: List of entry ids within `SDfile` instance.
    :return: Tuple of new `Molfile` and data associated with it.
    :rtype: :py:class:`tuple`
    """
    ctab_iso_layer = []
    coupling_types = set()
    sdfile_data = OrderedDict()

    for entry_id in entry_ids:
        molfile = ctfile[entry_id]['molfile']

        for coupling in ctfile[entry_id]['data']['CouplingType']:
            coupling_types.add(coupling)

        for atom in molfile.atoms:
            iso_property = {'atom_number': str(atom.atom_number),
                            'isotope': str(atom.isotope)}
            if iso_property not in ctab_iso_layer:
                ctab_iso_layer.append(iso_property)
            else:
                continue

    new_molfile = create_new_molfile(molfile=molfile, ctab_iso_layer=ctab_iso_layer)
    sdfile_data['CouplingType'] = sorted(coupling_types, key=lambda x: (x.split("]")[1], x))
    sdfile_data['InChI'] = [fileio.create_inchi_from_ctfile_obj(ctf=new_molfile)]

    return new_molfile, sdfile_data


def create_inchi_groups(ctfile):
    """Organize `InChI` into groups based on their identical `InChI` string and similar coupling type.

    :param ctfile: `SDfile` instance.
    :type ctfile: :class:`~ctfile.ctfile.SDfile`
    :return: Dictionary of related `InChI` groups.
    :rtype: :rtype: :py:class:`dict`
    """
    inchi_groups = defaultdict(list)
    for entry_id, entry in ctfile.items():
        inchi_str = entry["data"]["InChI"][0]
        descr = coupling_descr(coupling_types=entry["data"]["CouplingType"])
        inchi_groups[(inchi_str, descr)].append(entry_id)
    return inchi_groups


def annotate_me_groups(ctfile):
    """Annotate magnetically equivalent (have the same `InChI`) coupling type groups.

    :param ctfile: `SDfile` instance.
    :type ctfile: :class:`~ctfile.ctfile.SDfile`
    :return: None.
    :rtype: :py:obj:`None`
    """
    inchi_groups = create_inchi_groups(ctfile)
    me_ids = {inchi_str: group_id for inchi_str, group_id in zip(inchi_groups.keys(), list(range(1, len(inchi_groups) + 1)))}

    for data in ctfile.sdfdata:
        inchi_str = data["InChI"][0]
        descr = coupling_descr(coupling_types=data["CouplingType"])
        me_group_id = "ME{}".format(me_ids[(inchi_str, descr)])
        data["MEGroup"] = [me_group_id]

    for inchi_group, entry_ids in inchi_groups.items():
        if len(entry_ids) > 1:
            new_molfile, sdfile_data = create_aggregate_molfile(ctfile=ctfile, entry_ids=entry_ids)
            me_group_id = "MEA{}".format(me_ids[inchi_group])
            sdfile_data["MEGroup"] = [me_group_id]
            ctfile.add_molfile(molfile=new_molfile, data=sdfile_data)
        else:
            continue


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

    for isotope_str in isotopes:
        try:
            isotope, atom, position = isotope_str.split(':')
        except ValueError:
            raise ValueError('Incorrect isotope specification, use "isotope:element:position" format.')

        if atom not in allowed_atom_symbols:
            raise ValueError('Incorrect atom "{}" provided.'.format(atom))

        if isotope not in isotopes_conf[atom]["isotopes"]:
            raise ValueError('Incorrect isotope "{}" provided for atom "{}".'.format(isotope, atom))

        if ctfile_position_atom[position] != atom:
            raise ValueError('There is no "{}" atom at position "{}"'.format(atom, position))

        position_atom[position].append('{}-{}'.format(atom, isotope))
        specific_iso[position] = {'atom_symbol': atom, 'isotope': isotope, 'atom_number': position}

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

    for isotope_str in isotopes:
        try:
            isotope, atom = isotope_str.split(':')
        except ValueError:
            raise ValueError('Incorrect isotope specification, use "isotope:element" format.')

        if atom not in allowed_atom_symbols:
            raise ValueError('Incorrect atom "{}" provided.'.format(atom))

        if isotope not in isotopes_conf[atom]["isotopes"]:
            raise ValueError('Incorrect isotope "{}" provided for atom "{}".'.format(isotope, atom))

        atom_isotope[atom].append(isotope)

        for position, ctfile_atom in position_atom.items():
            if atom == ctfile_atom:
                all_iso[position] = {'atom_symbol': atom, 'isotope': isotope, 'atom_number': position}

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

    for isotope_str in enumerate_opt:
        try:
            isotope, atom, min_count, max_count = isotope_str.split(':')

        except ValueError:
            try:
                isotope, atom, max_count = isotope_str.split(':')
                min_count = 0

            except ValueError:
                try:
                    isotope, atom = isotope_str.split(':')
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

    if output_format not in {'svg', 'png'}:
        output_format = 'svg'

    with tempfile.NamedTemporaryFile(mode='w') as tempfh:
        tempfh.write(ctfile.writestr(file_format='ctfile'))
        tempfh.flush()

        openbabel.convert(input_file_path=tempfh.name,
                          output_file_path=output_path,
                          input_format='mol',
                          output_format=output_format,
                          **options)
