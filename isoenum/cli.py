#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum.cli
~~~~~~~~~~~

Isotopic enumerator (isoenum) command-line interface

Usage:
    isoenum -h | --help
    isoenum --version
    isoenum name (<path-to-ctfile-file-or-inchi-file-or-inchi-string>) 
                 [--specific=<isotope:element:position>...] 
                 [--all=<isotope:element>...] 
                 [--enumerate=<isotope:element:min:max>...] 
                 [--complete | --partial] 
                 [--ignore-iso]
                 [--format=<format>]
                 [--output=<path>]
                 [--verbose]
    isoenum ionize (<path-to-ctfile-file-or-inchi-file-or-inchi-string>)
                   (--state=<element:position:charge>...)
                   [--format=<format>]
                   [--output=<path>]
    isoenum nmr (<path-to-ctfile-file-or-inchi-file-or-inchi-string>)
                [--type=<experiment-type>]
                [--jcoupling=<name>...]
                [--decoupled=<element>...]
                [--format=<format>]
                [--output=<path>]
                [--subset]
                [--verbose]

Options:
    -h, --help                                 Show this screen.
    --verbose                                  Print more information.
    -v, --version                              Show version.
    -a, --all=<isotope:element>                Specify element and isotope, e.g. -a 13:C or --all=13:C
    -s, --specific=<isotope:element:position>  Specify element, isotope and specific position,
                                               e.g. -s 13:C:1 or --specific=13:C:1.
    -e, --enumerate=<isotope:element:min:max>  Enumerate all isotopically-resolved CTfile or InChI,
                                               e.g. -e 13:C:2:4 or --enumerate=13:C:2:4
    -c, --complete                             Use complete labeling schema, i.e. every atom must specify
                                               "ISO" property, partial labeling schema will be used otherwise
                                               for specified labeling information only.
    -p, --partial                              Use partial labeling schema, i.e. generate labeling schema
                                               from the provided labeling information.
    -i, --ignore-iso                           Ignore existing "ISO" specification in the CTfile or InChI.
    -f, --format=<format>                      Format of output: inchi, mol, sdf, csv, json [default: inchi].
    -o, --output=<path>                        Path to output file.
    -t, --type=<experiment-type>               Type of NMR experiment [default: 1D1H].
    -j, --jcoupling=<type>                     Allowed J couplings.
    -d, --decoupled=<element>                  Turn off J coupling for a given element.
    -z, --state=<element:position:charge>      Create ionized form of InChI from neutral molecule, 
                                               e.g. N:6:+1, O:8:-1.
    --subset                                   Create atom subsets for each resonance.
"""

from __future__ import print_function, division, unicode_literals

import os
import sys
import csv
import io
from collections import defaultdict
from collections import Counter
from collections import OrderedDict

import more_itertools

from . import fileio
from . import nmr
from .conf import isotopes_conf
from .labeling_schema import create_labeling_schema


def cli(cmdargs):
    """Process command-line arguments.
    
    :param dict cmdargs: Command-line arguments.
    :return: None.
    :rtype: :py:obj:`None`.
    """
    if cmdargs['name']:
        path = cmdargs['<path-to-ctfile-file-or-inchi-file-or-inchi-string>']
        ctf = fileio.create_ctfile(path)

        sdfile = fileio.create_empty_sdfile_obj()

        for molfile in ctf.molfiles:
            enumerate_param_iso = _unpack(cmdargs['--enumerate'])
            all_param_iso = _unpack(cmdargs['--all'])
            specific_param_iso = _unpack(cmdargs['--specific'])
            existing_iso = ['{}:{}:{}'.format(isotope['isotope'], isotope['atom_symbol'], isotope['atom_number'])
                            for isotope in molfile.iso]

            all_param_iso = _all_param_ok(isotopes=all_param_iso,
                                          isotopes_conf=isotopes_conf,
                                          ctfile=molfile)

            specific_param_iso = _specific_param_ok(isotopes=specific_param_iso,
                                                    isotopes_conf=isotopes_conf,
                                                    ctfile=molfile)

            existing_iso = _specific_param_ok(isotopes=existing_iso,
                                              isotopes_conf=isotopes_conf,
                                              ctfile=molfile)

            enumerate_param_iso = _enumerate_param_ok(enumerate_param=enumerate_param_iso,
                                                      all_param=all_param_iso,
                                                      isotopes_conf=isotopes_conf,
                                                      ctfile=molfile)

            labeling_schemas = create_labeling_schema(full_labeling_schema=cmdargs['--complete'],
                                                      ignore_existing_isotopes=cmdargs['--ignore-iso'],
                                                      enumerate_param_iso=enumerate_param_iso,
                                                      all_param_iso=all_param_iso,
                                                      specific_param_iso=specific_param_iso,
                                                      existing_iso=existing_iso,
                                                      isotopes_conf=isotopes_conf,
                                                      ctfile=molfile)

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

        create_output(sdfile=sdfile, path=cmdargs['--output'], file_format=cmdargs['--format'])

    elif cmdargs['ionize']:
        path = cmdargs['<path-to-ctfile-file-or-inchi-file-or-inchi-string>']
        atom_states = cmdargs['--state']
        ctf = fileio.create_ctfile(path)

        sdfile = fileio.create_empty_sdfile_obj()
        for molfile in ctf.molfiles:
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

        create_output(sdfile=sdfile, path=cmdargs['--output'], file_format=cmdargs['--format'])

    elif cmdargs['nmr']:
        path = cmdargs['<path-to-ctfile-file-or-inchi-file-or-inchi-string>']
        experiment_type = cmdargs['--type']
        decoupled = [element.upper() for element in cmdargs['--decoupled']]
        jcoupling = [coupling.upper() for coupling in cmdargs['--jcoupling']]
        subset = cmdargs['--subset']

        ctf = fileio.create_ctfile(path)
        nmr_experiment = nmr.create_nmr_experiment(name=experiment_type, couplings=jcoupling, decoupled=decoupled)

        sdfile = fileio.create_empty_sdfile_obj()
        for molfile in ctf.molfiles:
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

                sdfile_data.setdefault('InChI', []).append('{}'.format(fileio.create_inchi_from_ctfile_obj(ctf=new_molfile)))
                sdfile.add_molfile(molfile=new_molfile, data=sdfile_data)

        create_output(sdfile=sdfile, path=cmdargs['--output'], file_format=cmdargs['--format'])


def _enumerate_param_ok(enumerate_param, all_param, isotopes_conf, ctfile):
    """Check if `--enumerate` option is consistent.
    
    :param list enumerate_param: Option that specifies isotopes.
    :param dict all_param: Check for consistency, `--enumerate` are not compatible with `--all` for the same atom.
    :param dict isotopes_conf: Default isotopes configuration. 
    :param ctfile: Instance of ``Molfile``. 
    :type ctfile: :class:`~ctfile.ctfile.Molfile`.
    :return: :py:class:`dict` with position specific labeling if consistent, raises error otherwise.
    :rtype: :py:class:`dict` or :py:class:`ValueError`. 
    """
    atom_counter = Counter([atom.atom_symbol for atom in ctfile.atoms])
    allowed_atom_symbols = [atom.atom_symbol for atom in ctfile.atoms]
    all_param_atoms = [entry['atom_symbol'] for entry in all_param.values()]
    enumerate_param_iso = []

    for isotopestr in enumerate_param:

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

        enumerate_param_iso.append({'atom_symbol': atom, 'isotope': isotope,
                                    'min': int(min_count), 'max': int(max_count)})

        if atom in all_param_atoms:
            raise ValueError('"--enumerate" and "--all" options are not compatible for atom: "{}"'.format(atom))

        if atom not in allowed_atom_symbols:
            raise ValueError('Incorrect atom "{}" provided.'.format(atom))

        if isotope not in isotopes_conf[atom]['isotopes']:
            raise ValueError('Incorrect isotope "{}" provided for atom "{}".'.format(isotope, atom))

        if int(max_count) > atom_counter[atom]:
            raise ValueError('Incorrect count "{}" provided for atom "{}".'.format(max_count, atom))

    return enumerate_param_iso


def _all_param_ok(isotopes, isotopes_conf, ctfile):
    """Check if `--all` option is consistent.

    :param list isotopes: Option that specifies isotopes.
    :param dict isotopes_conf: Default isotopes configuration.
    :param ctfile: Instance of ``Molfile``. 
    :type ctfile: :class:`~ctfile.ctfile.Molfile`.
    :return: :py:class:`dict` with position specific labeling if consistent, raises error otherwise.
    :rtype: :py:class:`dict` or :py:class:`ValueError`.
    """
    allowed_atom_symbols = [atom.atom_symbol for atom in ctfile.atoms]
    positions = [atom.atom_number for atom in ctfile.atoms]
    position_atom = dict(zip(positions, allowed_atom_symbols))
    atom_isotope = defaultdict(list)
    all_param_iso = {}

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
                all_param_iso[position] = {'atom_symbol': atom, 'isotope': isotope, 'position': position}

    if all(len(isotopes) == 1 for isotopes in atom_isotope.values()):
        return all_param_iso
    else:
        raise ValueError('"--all" option can only specify single isotope per atom type.')


def _specific_param_ok(isotopes, isotopes_conf, ctfile):
    """Check if `--specific` option is consistent.

    :param list isotopes: Option that specifies isotopes.
    :param dict isotopes_conf: Default isotopes configuration.
    :param ctfile: Instance of ``Molfile``. 
    :type ctfile: :class:`~ctfile.ctfile.Molfile`.
    :return: :py:class:`dict` with position specific labeling if consistent, raises error otherwise.
    :rtype: :py:class:`dict` or :py:class:`ValueError`.
    """
    position_atom = defaultdict(list)
    allowed_atom_symbols = [atom.atom_symbol for atom in ctfile.atoms]
    positions = [atom.atom_number for atom in ctfile.atoms]
    ctfile_position_atom = dict(zip(positions, allowed_atom_symbols))
    specific_param_iso = {}

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
        specific_param_iso[position] = {'atom_symbol': atom, 'isotope': isotope, 'position': position}

    if all(len(isotopes) == 1 for isotopes in position_atom.values()):
        return specific_param_iso
    else:
        raise ValueError('"--specific" option can only specify single isotope per atom position.')


def _unpack(param):
    """Unpack command-line option.

    :param list param: List of isotopes.
    :return: List of unpacked isotopes.
    :rtype: :py:class:`list`.
    """
    options = []
    for option_str in param:
        options.extend(option_str.split(','))
    return options


def save_output(outputstr, path, file_format):
    """Save output results into file or print to stdout.
    
    :param str outputstr: Output string. 
    :param str path: Where to save results.
    :param str file_format: File format to create file extension.
    :return: None.
    :rtype: :py:obj:`None`.
    """
    if path is not None:
        dirpath, basename = os.path.split(os.path.normpath(path))
        filename, extension = os.path.splitext(basename)

        if not extension:
            extension = '.{}'.format(file_format)

        filename = '{}{}'.format(filename, extension)
        filepath = os.path.join(dirpath, filename)

        if dirpath and not os.path.exists(dirpath):
            raise IOError('Directory does not exist: "{}"'.format(dirpath))

        with open(filepath, 'w') as outfile:
            print(outputstr, file=outfile)
    else:
        print(outputstr, file=sys.stdout)


def create_output(sdfile, path=None, file_format='inchi'):
    """Create output containing conversion results.

    :param sdfile: ``SDfile`` instance.
    :type sdfile: :class:`~ctfile.ctfile.SDfile`.
    :param str path: Path to where file will be saved. 
    :param str format: File format: 'inchi', 'mol', 'sdf', 'json', or 'csv'. 
    :return: None.
    :rtype: :py:obj:`None`.
    """
    default_output_formats = {'inchi', 'mol', 'sdf', 'csv', 'json'}
    file_format = file_format.lower()

    if file_format not in default_output_formats:
        raise ValueError('Unknown output format: "{}"'.format(file_format))

    if file_format in {'sdf', 'mol'}:
        save_output(outputstr=sdfile.writestr(file_format='ctfile'),
                    path=path,
                    file_format=file_format)

    elif file_format in {'json'}:
        save_output(outputstr=sdfile.writestr(file_format='json'),
                    path=path,
                    file_format=file_format)

    elif file_format in {'inchi'}:
        output = []
        for entry_id in sdfile:
            output.extend([inchi.strip() for inchi in sdfile[entry_id]['data']['InChI']])

        save_output(outputstr='\n'.join(output),
                    path=path,
                    file_format=file_format)

    elif file_format in {'csv'}:
        outputstr = io.StringIO()
        csvwriter = csv.writer(outputstr, delimiter='\t')

        for entry_id in sdfile:
            csv_data = []
            for data_id in sdfile[entry_id]['data']:
                value = ' + '.join([item.strip() for item in sdfile[entry_id]['data'][data_id]])
                csv_data.append(value)
            csvwriter.writerow(csv_data)

        save_output(outputstr=outputstr.getvalue(),
                    path=path,
                    file_format=file_format)
