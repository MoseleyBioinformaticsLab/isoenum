#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools
from collections import defaultdict
from collections import Counter


def create_labeling_schema(full_labeling_schema, ignore_existing_isotopes,
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


def _default_isotopes(ctfile_atoms, ctfile_positions, isotopes_conf, current_iso):
    """Create dictionary with default isotopes.

    :param list ctfile_atoms: List of atoms.
    :param list ctfile_positions: List of atom positions.
    :param dict isotopes_conf: Default isotopes.
    :param dict current_iso: Current isotopes to which default isotopes will be added. 
    :return: Default isotopes.
    :rtype: :py:class:`dict`
    """
    default_iso = {}

    ctfile_position_atom = dict(zip(ctfile_positions, ctfile_atoms))

    for position in ctfile_positions:
        if position not in current_iso:
            atom = ctfile_position_atom[position]
            isotope = isotopes_conf[atom]['default']
            default_iso[position] = {'atom_symbol': atom, 'isotope': isotope, 'position': position}
    return default_iso
