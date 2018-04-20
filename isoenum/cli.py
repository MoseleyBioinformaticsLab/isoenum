#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Isotopic enumerator (isoenum) command-line interface

Usage:
    isoenum -h | --help
    isoenum --version
    isoenum name (<path-to-ctfile-file-or-inchi-file-or-inchi-string>) 
                 [--specific=<element-isotope-position>...] 
                 [--all=<element-isotope>...] 
                 [--enumerate=<element-isotope-count>...] 
                 [--full | --partial] 
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
    -f, --full                                 Use full labeling schema, i.e. every atom must specify
                                               "ISO" property, partial labeling schema will be used otherwise
                                               for specified labeling information only.
    -p, --partial                              Use partial labeling schema, i.e. generate labeling schema
                                               from the provided labeling information.
    -i, --ignore-iso                           Ignore "ISO" specification in the CTfile or InChI.
    -r, --format=<format>                      Format of output: inchi, mol or sdf [default: inchi].
    -o, --output=<path>                        Path to output file.
"""

from __future__ import print_function, division, unicode_literals

import tempfile
import os
import sys
import io
from collections import defaultdict
from collections import Counter

import ctfile
from .iso_property import create_iso_property
from .openbabel import mol_to_inchi
from .openbabel import inchi_to_mol
from .conf import isotopes_conf
from .labeling_schema import create_labeling_schema


def cli(cmdargs):
    """Process command-line arguments.
    
    :param dict cmdargs: Command-line arguments.
    :return: None.
    :rtype: :py:obj:`None`
    """
    if cmdargs['name']:

        path = cmdargs['<path-to-ctfile-file-or-inchi-file-or-inchi-string>']

        try:
            ctf = _create_ctfile(path)
        except:
            raise

        if isinstance(ctf, ctfile.ctfile.Molfile) or isinstance(ctf, ctfile.ctfile.SDfile):
            molfiles = ctf.molfiles
        else:
            raise ValueError('Unknow "CTfile" type.')

        if cmdargs['--format'] not in ('inchi', 'mol', 'sdf'):
            raise ValueError('Unknown output format provided: "{}"'.format(cmdargs['--format']))

        results = []

        for molfile in molfiles:

            enumerate_param_iso = _unpack_isotopes(cmdargs['--enumerate'])
            all_param_iso = _unpack_isotopes(cmdargs['--all'])
            specific_param_iso = _unpack_isotopes(cmdargs['--specific'])
            existing_iso = ['{}-{}-{}'.format(isotope['atom_symbol'], isotope['isotope'], isotope['position'])
                            for isotope in molfile.iso]

            ctfile_atoms = molfile.atoms
            ctfile_positions = molfile.positions

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

            labeling_schema = create_labeling_schema(full_labeling_schema=cmdargs['--full'],
                                                     ignore_existing_isotopes=cmdargs['--ignore-iso'],
                                                     enumerate_param_iso=enumerate_param_iso,
                                                     all_param_iso=all_param_iso,
                                                     specific_param_iso=specific_param_iso,
                                                     existing_iso=existing_iso,
                                                     isotopes_conf=isotopes_conf,
                                                     ctfile_atoms=ctfile_atoms,
                                                     ctfile_positions=ctfile_positions)

            for schema in labeling_schema:
                new_iso_property = create_iso_property(labeling_schema=schema)
                molfile['Ctab']['CtabPropertiesBlock']['ISO'] = new_iso_property

                inchi_str = '{}'.format(_create_inchi_from_ctfile_obj(molfile))

                # need to create new ctfile from inchi string in order to normalize it
                # in case original file had wrong atom numbering
                new_molfile = _create_ctfile_from_inchi_str(inchi_str=inchi_str)

                new_molfile_str = '{}'.format(new_molfile.writestr(file_format='ctfile'))
                results.append({'inchi': inchi_str, 'molfile': new_molfile_str})

        _create_output(results, path=cmdargs['--output'], format=cmdargs['--format'])


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


def _create_ctfile(path):
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
                return _create_ctfile_from_inchi_file(path=path)
    else:
        return _create_ctfile_from_inchi_str(inchi_str=path)


def _create_ctfile_from_inchi_str(inchi_str):
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
        return _create_ctfile_from_inchi_file(path=tempfh.name)


def _create_ctfile_from_inchi_file(path):
    """Creates ``CTfile`` from ``InChI`` identifier.
    
    :param str path: Path to file containing ``InChI`` identifier.
    :return: Subclass of :class:`~ctfile.ctfile.CTfile` object.
    :rtype: :class:`~ctfile.ctfile.CTfile`.
    """
    with tempfile.NamedTemporaryFile() as tempfh:
        inchi_to_mol(infilename=path, outfilename=tempfh.name)
        with open(tempfh.name, 'r') as infile:
            return ctfile.load(infile)


def _create_inchi_from_ctfile_obj(ctf):
    """Create ``InChI`` from ``CTfile`` instance.
    
    :param ctf: Instance of :class:`~ctfile.ctfile.CTfile`.
    :type ctf: :class:`~ctfile.ctfile.CTfile`
    :return: ``InChI`` string.
    :rtype: :py:class:`str` 
    """
    with tempfile.NamedTemporaryFile(mode='w') as moltempfh, tempfile.NamedTemporaryFile(mode='r') as inchitempfh:
        moltempfh.write(ctf.writestr(file_format='ctfile'))
        moltempfh.flush()
        mol_to_inchi(infilename=moltempfh.name, outfilename=inchitempfh.name)
        inchi_result = inchitempfh.read()
        return inchi_result


def _create_output(results, path=None, format='inchi'):
    """Create output containing conversion results.
    
    :param list results: List of dictionaries, each containing ``InChI`` string and corresponding ``Molfile`` string.
    :param str path: Path to where file will be saved. 
    :param str format: File format: 'inchi', 'mol', or 'sdf'. 
    :return: None.
    :rtype: :py:obj:`None`
    """
    output_format = format.lower()

    if output_format == 'inchi':
        output = io.StringIO()

        for result in results:
            inchi_string = result['inchi']
            output.write(inchi_string)

    elif output_format in ('mol', 'sdf'):
        output = io.StringIO()

        for result in results:
            molfile_string = result['molfile']
            inchi_string = result['inchi']

            output.write(molfile_string)
            output.write('> <InChI>\n')
            output.write(inchi_string)
            output.write('\n')
            output.write('$$$$\n')

    else:
        raise ValueError('Unknown output format provided: "{}"'.format(format))

    if path:
        dirpath, basename = os.path.split(os.path.normpath(path))
        filename, extension = os.path.splitext(basename)

        if not extension:
            extension = '.{}'.format(output_format)

        filename = '{}{}'.format(filename, extension)
        filepath = os.path.join(dirpath, filename)

        if dirpath and not os.path.exists(dirpath):
            raise IOError('Directory does not exist: "{}"'.format(dirpath))

        with open(filepath, 'w') as outfile:
            print(output.getvalue(), file=outfile)

    else:
        print(output.getvalue(), file=sys.stdout)
