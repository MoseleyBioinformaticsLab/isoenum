#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
isoenum.labeling
~~~~~~~~~~~~~~~~

This module contains a function to generate a labeling schema 
based on provided cli parameters.
"""

import itertools
from collections import defaultdict
from collections import Counter


def create_labeling_schema(complete_labeling_schema, ignore_existing_isotopes,
                           all_iso, specific_iso, existing_iso, enumerate_iso,
                           isotopes_conf, ctfile):
    """Create labeling schema.

    :param bool complete_labeling_schema: Specifies if default isotopes to be added to isotopic layer.
    :param bool ignore_existing_isotopes: Specifies if will ignore existing isotopic layer.
    :param dict all_iso: Atom specific isotopes `--all` option.
    :param dict specific_iso: Atom number specific isotopes from `--specific` option.
    :param dict existing_iso: Atom number specific isotopes from ``Molfile``.
    :param list enumerate_iso: List of isotopes from `--enumerate` option. 
    :param dict isotopes_conf: Default isotopes.
    :param ctfile: Instance of ``Molfile``. 
    :type ctfile: :class:`~ctfile.ctfile.Molfile`
    :return: Labeling schema.
    :rtype: :py:class:`list`
    """
    allowed_atom_symbols = [atom.atom_symbol for atom in ctfile.atoms]
    positions = [atom.atom_number for atom in ctfile.atoms]
    ctfile_position_atom = dict(zip(positions, allowed_atom_symbols))
    starting_iso = {}

    # first, use all atom specification to create labeling schema
    if all_iso:
        starting_iso.update(all_iso)

    # second, use specific atom bspecification to create labeling schema
    if specific_iso:
        starting_iso.update(specific_iso)

    # third, keep the isotopic layer from original CTfile
    if not ignore_existing_isotopes:
        if existing_iso:
            starting_iso.update(existing_iso)

    if not enumerate_iso:
        # add default isotopes if need to create full labeling schema
        if complete_labeling_schema:
            default_iso = _default_isotopes(ctfile=ctfile, isotopes_conf=isotopes_conf, current_iso=starting_iso)
            starting_iso.update(default_iso)

        labeling_schema = sorted(starting_iso.values(), key=lambda k: int(k['atom_number']))
        yield labeling_schema

    else:
        isotopes_per_atom = defaultdict(set)

        for entry in enumerate_iso:
            isotopes_per_atom[entry['atom_symbol']].add(entry['isotope'])
            isotopes_per_atom[entry['atom_symbol']].add(None)  # None designates that isotope is not specified

        list_of_isotopes_per_position = defaultdict(list)
        for position, atom in ctfile_position_atom.items():
            list_of_isotopes_per_position[position].extend(isotopes_per_atom.get(atom, [None]))

        for entry in starting_iso.values():
            list_of_isotopes_per_position[entry['atom_number']] = [entry['isotope']]

        list_of_isotopes_per_position_sorted_by_position = [list_of_isotopes_per_position[iso] for iso in
                                                            sorted(list_of_isotopes_per_position, key=int)]

        labeling_product = itertools.product(*list_of_isotopes_per_position_sorted_by_position)
        for prod in labeling_product:
            labeling_schema = {}

            isotopes_per_atom = ['{}-{}'.format(atom, isotope) for atom, isotope in zip(allowed_atom_symbols, prod)]
            counter = Counter(isotopes_per_atom)

            valid_labeling = [
                True
                if entry['min'] <= counter['{}-{}'.format(entry['atom_symbol'], entry['isotope'])] <= entry['max']
                else False
                for entry in enumerate_iso
            ]

            if all(valid_labeling):
                for atom, isotope, position in zip(allowed_atom_symbols, prod, positions):
                    if isotope:
                        labeling_schema[position] = {'atom_symbol': atom, 'isotope': isotope, 'atom_number': position}

            if complete_labeling_schema:
                default_iso = _default_isotopes(ctfile=ctfile, isotopes_conf=isotopes_conf, current_iso=labeling_schema)
                labeling_schema.update(default_iso)

            labeling_schema = sorted(labeling_schema.values(), key=lambda k: int(k['atom_number']))
            if labeling_schema:
                yield labeling_schema


def _default_isotopes(ctfile, isotopes_conf, current_iso):
    """Create dictionary with default isotopes.

    :param ctfile: Instance of ``Molfile``. 
    :type ctfile: :class:`~ctfile.ctfile.Molfile`.
    :param dict isotopes_conf: Default isotopes.
    :param dict current_iso: Current isotopes to which default isotopes will be added. 
    :return: Default isotopes.
    :rtype: :py:class:`dict`
    """
    default_iso = {}
    allowed_atom_symbols = [atom.atom_symbol for atom in ctfile.atoms]
    positions = [atom.atom_number for atom in ctfile.atoms]
    ctfile_position_atom = dict(zip(positions, allowed_atom_symbols))

    for atom_number in positions:
        if atom_number not in current_iso:
            atom = ctfile_position_atom[atom_number]
            isotope = isotopes_conf[atom]['default']
            default_iso[atom_number] = {'atom_symbol': atom, 'isotope': isotope, 'atom_number': atom_number}
    return default_iso
