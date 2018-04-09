#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Isotopic enumerator (isoenum) command-line interface

Usage:
    isoenum -h | --help
    isoenum --version
    isoenum name (--ctfile=<path> | --inchi=<path-or-string>) [--specific=<element-isotope-position>...] 
                 [--all=<element-isotope>...] [--enumerate=<element-isotope-count>...] 
                 [--full | --partial] [--ignore-iso]

Options:
    -h, --help                                 Show this screen.
    --version                                  Show version.
    --verbose                                  Print what files are processing.

    --ctfile=<path>                            Path to CTfile (e.g. Molfile or SDfile).
    --inchi=<path-or-string>                   Path to file containing standard InChI or InChI string.

    -a, --all=<element-isotope>                Specify element and isotope, e.g. -a C-13 or --all=C-13
    -s, --specific=<element-isotope-position>  Specify element, isotope and specific position,
                                               e.g. -s C-13-1 or --specific=C-13-1.
    -e, --enumerate=<element-isotope-min-max>  Enumerate all isotopically-resolved CTfile or InChI.
    -f, --full                                 Use full labeling schema, i.e. every atom must specify
                                               "ISO" property, partial labeling schema will be used otherwise
                                               for specified labeling information only.
    -p, --partial                              Use partial labeling schema, i.e. generate labeling schema
                                               from the provided labeling information.
    -i, --ignore-iso                           Ignore "ISO" specification in the CTfile or InChI.
"""

import tempfile
import itertools
from collections import defaultdict
from collections import Counter
from pprint import pprint

import ctfile
from .enumerator import Enumerator
from .openbabel import mol_to_inchi
from .openbabel import inchi_to_mol
from .conf import isotopes_conf


def cli(cmdargs):
    """Process command-line arguments.
    
    :param dict cmdargs: Command-line arguments.
    :return: None.
    :rtype: :py:obj:`None`
    """
    if cmdargs['name']:
        if cmdargs['--ctfile']:
            ctf = ctfile.read_file(path=cmdargs['--ctfile'])

        elif cmdargs["--inchi"]:
            with tempfile.NamedTemporaryFile() as moltempfh:
                inchi_to_mol(infilename=cmdargs["--inchi"], outfilename=moltempfh.name)
                ctf = ctfile.read_file(path=moltempfh.name)
        else:
            raise ValueError('Incorrect input.')

        enumerate_param_iso = _unpack_isotopes(cmdargs['--enumerate'])
        all_param_iso = _unpack_isotopes(cmdargs['--all'])
        specific_param_iso = _unpack_isotopes(cmdargs['--specific'])
        existing_iso = ['{}-{}-{}'.format(isotope['atom_symbol'], isotope['isotope'], isotope['position'])
                        for isotope in ctf.iso]

        ctfile_atoms = ctf.atoms
        ctfile_positions = ctf.positions


        all_param_iso = _all_param_ok(isotopes=all_param_iso,
                                      isotopes_conf=isotopes_conf,
                                      ctfile_atoms=ctfile_atoms,
                                      ctfile_positions=ctfile_positions)

        specific_param_iso = _specific_param_ok(isotopes=specific_param_iso,
                                                isotopes_conf=isotopes_conf,
                                                ctfile_atoms=ctfile_atoms,
                                                ctfile_positions=ctfile_positions)

        existing_iso = _specific_param_ok(isotopes=existing_iso,
                                          isotopes_conf=isotopes_conf,
                                          ctfile_atoms=ctfile_atoms,
                                          ctfile_positions=ctfile_positions)

        enumerate_param_iso = _enumerate_param_ok(enumerate_param=enumerate_param_iso,
                                                  all_param=all_param_iso,
                                                  isotopes_conf=isotopes_conf,
                                                  ctfile_atoms=ctfile_atoms)

        labeling_schema = _create_labeling_schema(full_labeling_schema=cmdargs['--full'],
                                                  ignore_existing_isotopes=cmdargs['--ignore-iso'],
                                                  enumerate_param_iso=enumerate_param_iso,
                                                  all_param_iso=all_param_iso,
                                                  specific_param_iso=specific_param_iso,
                                                  existing_iso=existing_iso,
                                                  isotopes_conf=isotopes_conf,
                                                  ctfile_atoms=ctfile_atoms,
                                                  ctfile_positions=ctfile_positions)

        for schema in labeling_schema:
            e = Enumerator(ctf)
            iso_property_generator = e.isoenum(labeling_schema=schema)

            for new_iso_property in iso_property_generator:
                ctf['Ctab']['CtabPropertiesBlock']['ISO'] = new_iso_property

            with tempfile.NamedTemporaryFile() as moltempfh, tempfile.NamedTemporaryFile() as inchitempfh:
                moltempfh.write(bytes(ctf.writestr(file_format='ctfile'), encoding='utf-8'))
                moltempfh.flush()
                mol_to_inchi(infilename=moltempfh.name, outfilename=inchitempfh.name)

                inchi_result = inchitempfh.read().decode()
                print("result:", inchi_result)


def _enumerate_param_ok(enumerate_param, all_param, isotopes_conf, ctfile_atoms):
    """Check if `--enumerate` parameter is consistent.

    :param list enumerate_param: Parameter that specifies isotopes.
    :param list all_param: Parameter that specifies isotopes.
    :param dict isotopes_conf: Default isotopes.
    :param list ctfile_atoms: List of atoms.
    :return: :py:obj:`True` if consistent, raises error otherwise.
    :rtype: :py:obj:`True` or :py:class:`ValueError`.
    """
    atom_counter = Counter(ctfile_atoms)
    all_param_atoms = [entry['atom_symbol'] for entry in all_param.values()]
    enumerate_param_iso = []

    for isotopestr in enumerate_param:

        try:
            atom, isotope, min_count, max_count = isotopestr.split('-')

        except ValueError:
            try:
                atom, isotope, max_count = isotopestr.split('-')
                min_count = 0

            except ValueError:
                try:
                    atom, isotope = isotopestr.split('-')
                    max_count = atom_counter[atom]
                    min_count = 0

                except ValueError:
                    raise ValueError('Incorrect isotope specification, use "atom-isotope-min-max",'
                                     '"atom-isotope-max" or "atom-isotope" format.')

        enumerate_param_iso.append({'atom_symbol': atom, 'isotope': isotope,
                                    'min': int(min_count), 'max': int(max_count)})

        if atom in all_param_atoms:
            raise ValueError('"--enumerate" and "--all" parameters are not compatible for atom: "{}"'.format(atom))

        if atom not in ctfile_atoms:
            raise ValueError('Incorrect atom "{}" provided.'.format(atom))

        if isotope not in isotopes_conf[atom]['isotopes']:
            raise ValueError('Incorrect isotope "{}" provided for atom "{}".'.format(isotope, atom))

        if int(max_count) > atom_counter[atom]:
            raise ValueError('Incorrect count "{}" provided for atom "{}".'.format(max_count, atom))

    return enumerate_param_iso


def _all_param_ok(isotopes, isotopes_conf, ctfile_atoms, ctfile_positions):
    """Check if `--all` parameter is consistent.

    :param list isotopes: Parameter that specifies isotope.
    :param dict isotopes_conf: Default isotopes.
    :param list ctfile_atoms: List of atoms.
    :param list ctfile_positions: List of atom positions.
    :return: :py:obj:`True` if consistent, raises error otherwise.
    :rtype: :py:obj:`True` or :py:class:`ValueError`.
    """
    atom_isotope = defaultdict(list)
    ctfile_position_atom = dict(zip(ctfile_positions, ctfile_atoms))
    all_param_iso = {}

    for isotopestr in isotopes:

        try:
            atom, isotope = isotopestr.split('-')
        except ValueError:
            raise ValueError('Incorrect isotope specification, use "atom-isotope" format.')

        if atom not in ctfile_atoms:
            raise ValueError('Incorrect atom "{}" provided.'.format(atom))

        if isotope not in isotopes_conf[atom]["isotopes"]:
            raise ValueError('Incorrect isotope "{}" provided for atom "{}".'.format(isotope, atom))

        atom_isotope[atom].append(isotope)

        for position, ctfile_atom in ctfile_position_atom.items():
            if atom == ctfile_atom:
                all_param_iso[position] = {'atom_symbol': atom, 'isotope': isotope, 'position': position}

    if all(len(isotopes) == 1 for isotopes in atom_isotope.values()):
        return all_param_iso
    else:
        raise ValueError('"--all" parameter can only specify single isotope per atom type.')


def _specific_param_ok(isotopes, isotopes_conf, ctfile_atoms, ctfile_positions):
    """Check if `--specific` parameter is consistent.

    :param list isotopes: Parameter that specifies isotopes.
    :param dict isotopes_conf: Default isotopes.
    :param list ctfile_atoms: List of atoms.
    :param list ctfile_positions: List of atom positions.
    :return: :py:obj:`True` if consistent, raises error otherwise.
    :rtype: :py:obj:`True` or :py:class:`ValueError`.
    """
    position_atom = defaultdict(list)
    ctfile_position_atom = dict(zip(ctfile_positions, ctfile_atoms))
    specific_param_iso = {}

    for isotopestr in isotopes:

        try:
            atom, isotope, position = isotopestr.split('-')
        except ValueError:
            raise ValueError('Incorrect isotope specification, use "atom-isotope-position" format.')

        if atom not in ctfile_atoms:
            raise ValueError('Incorrect atom "{}" provided.'.format(atom))

        if isotope not in isotopes_conf[atom]["isotopes"]:
            raise ValueError('Incorrect isotope "{}" provided for atom "{}".'.format(isotope, atom))

        if ctfile_position_atom[position] != atom:
            raise ValueError('There is no "{}" atom at position "{}"'.format(atom, position))

        position_atom[position].append('{}-{}'.format(atom, isotope))
        specific_param_iso[position] = {'atom_symbol': atom, 'isotope': isotope, 'position': position}

    if all(len(isotopes) == 1 for isotopes in position_atom.values()):
        return specific_param_iso
    else:
        raise ValueError('"--specific" parameter can only specify single isotope per atom position.')


def _create_labeling_schema(full_labeling_schema, ignore_existing_isotopes,
                            enumerate_param_iso, all_param_iso, specific_param_iso, existing_iso,
                            isotopes_conf, ctfile_atoms, ctfile_positions):
    """Create labeling schema.

    :param bool full_labeling_schema: Specifies if default isotopes to be added to isotopic layer.
    :param bool ignore_existing_isotopes: Specifies if will ignore existing isotopic layer.
    :param list enumerate_param_iso: List of isotope strings from `--enumerate` parameter. 
    :param list all_param_iso: List of isotope strings from `--all` parameter.
    :param list specific_param_iso: List of isotope strings from `--specific` parameter.
    :param list existing_iso: List of isotope strings that were defined within `CTfile` or `InChI`.
    :param dict isotopes_conf: Default isotopes.
    :param list ctfile_atoms: List of atoms.
    :param list ctfile_positions: List of atom positions.
    :return: Labeling schema.
    :rtype: :py:class:`list`
    """
    ctfile_position_atom = dict(zip(ctfile_positions, ctfile_atoms))
    starting_iso = {}

    # first, use "--all" specification to create labeling schema
    if all_param_iso:
        starting_iso.update(all_param_iso)

    # second, use "--specific" specification to create labeling schema
    if specific_param_iso:
        starting_iso.update(specific_param_iso)

    # third, keep the isotopic layer from original CTfile
    if not ignore_existing_isotopes:
        if existing_iso:
            starting_iso.update(existing_iso)

    if not enumerate_param_iso:
        # add default isotopes if "--full" parameter is specified
        if full_labeling_schema:
            default_iso = _default_isotopes(ctfile_atoms, ctfile_positions, isotopes_conf, starting_iso)
            starting_iso.update(default_iso)

        labeling_schema = sorted(starting_iso.values(), key=lambda k: int(k['position']))
        yield labeling_schema

    else:
        isotopes_per_atom = defaultdict(set)

        for entry in enumerate_param_iso:
            isotopes_per_atom[entry['atom_symbol']].add(entry['isotope'])
            isotopes_per_atom[entry['atom_symbol']].add(None)  # None designates that isotope is not specified

        list_of_isotopes_per_position = defaultdict(list)
        for position, atom in ctfile_position_atom.items():
            list_of_isotopes_per_position[position].extend(isotopes_per_atom.get(atom, [None]))

        for entry in starting_iso.values():
            list_of_isotopes_per_position[entry['position']] = [entry['isotope']]

        list_of_isotopes_per_position_sorted_by_position = [list_of_isotopes_per_position[iso] for iso in
                                                            sorted(list_of_isotopes_per_position, key=int)]

        labeling_product = itertools.product(*list_of_isotopes_per_position_sorted_by_position)
        for prod in labeling_product:
            labeling_schema = {}

            isotopes_per_atom = ['{}-{}'.format(atom, isotope) for atom, isotope in zip(ctfile_atoms, prod)]
            counter = Counter(isotopes_per_atom)

            valid_labeling = [True
                              if entry['min'] <= counter['{}-{}'.format(entry['atom_symbol'],
                                                                        entry['isotope'])] <= entry['max']
                              else False
                              for entry in enumerate_param_iso]

            if all(valid_labeling):
                for atom, isotope, position in zip(ctfile_atoms, prod, ctfile_positions):
                    if isotope:
                        labeling_schema[position] = {'atom_symbol': atom, 'isotope': isotope, 'position': position}

            if full_labeling_schema:
                default_iso = _default_isotopes(ctfile_atoms, ctfile_positions, isotopes_conf, labeling_schema)
                labeling_schema.update(default_iso)

            labeling_schema = sorted(labeling_schema.values(), key=lambda k: int(k['position']))
            if labeling_schema:
                yield labeling_schema


def _default_isotopes(ctfile_atoms, ctfile_positions, isotopes_conf, starting_iso):
    """Create dictionary with default isotopes.
    
    :param list ctfile_atoms: List of atoms.
    :param list ctfile_positions: List of atom positions.
    :param dict isotopes_conf: Default isotopes.
    :param dict starting_iso: Starting isotopes. 
    :return: Default isotopes.
    :rtype: :py:class:`dict`
    """
    default_iso = {}

    ctfile_position_atom = dict(zip(ctfile_positions, ctfile_atoms))

    for position in ctfile_positions:
        if position not in starting_iso:
            atom = ctfile_position_atom[position]
            isotope = isotopes_conf[atom]['default']
            default_iso[position] = {'atom_symbol': atom, 'isotope': isotope, 'position': position}
    return default_iso


def _unpack_isotopes(param):
    """Unpack isotopes from command-line `--all` and `--specific` parameters.

    :param list param: List of isotopes.
    :return: List of unpacked isotopes.
    :rtype: :py:class:`list`
    """
    isotopes = []
    for isotopestr in param:
        isotopes.extend(isotopestr.split(','))
    return isotopes
