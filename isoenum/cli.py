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
    isoenum vis (<path-to-ctfile-file-or-inchi-file-or-inchi-string>) 
                (--format=<format>)
                (--output=<path>)

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

import csv
import io
import os
import sys

from . import api
from .conf import output_formats_conf


def cli(cmdargs):
    """Process command-line arguments.

    :param dict cmdargs: Command-line arguments.
    :return: None.
    :rtype: :py:obj:`None`
    """
    path_or_id = cmdargs['<path-to-ctfile-file-or-inchi-file-or-inchi-string>']

    if cmdargs['name']:
        sdfile = api.iso(path_or_id=path_or_id,
                         specific_opt=cmdargs['--specific'],
                         all_opt=cmdargs['--all'],
                         enumerate_opt=cmdargs['--enumerate'],
                         complete_opt=cmdargs['--complete'],
                         ignore_iso_opt=cmdargs['--ignore-iso'])

        create_output(sdfile=sdfile, path=cmdargs['--output'], file_format=cmdargs['--format'])

    elif cmdargs['ionize']:
        atom_states = cmdargs['--state']
        sdfile = api.chg(path_or_id=path_or_id, atom_states=atom_states)
        create_output(sdfile=sdfile, path=cmdargs['--output'], file_format=cmdargs['--format'])

    elif cmdargs['nmr']:
        experiment_type = cmdargs['--type']
        decoupled = [element.upper() for element in cmdargs['--decoupled']]
        couplings = [coupling.upper() for coupling in cmdargs['--jcoupling']]
        subset = cmdargs['--subset']

        sdfile = api.iso_nmr(path_or_id=path_or_id, experiment_type=experiment_type,
                             couplings=couplings, decoupled=decoupled, subset=subset)

        create_output(sdfile=sdfile, path=cmdargs['--output'], file_format=cmdargs['--format'])

    elif cmdargs['vis']:
        api.visualize(path_or_id=path_or_id,
                      output_path=cmdargs['--output'],
                      output_format=cmdargs['--format'])


def _unpack(param):
    """Unpack command-line option.

    :param list param: List of isotopes.
    :return: List of unpacked isotopes.
    :rtype: :py:class:`list`
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
    :rtype: :py:obj:`None`
    """
    if path is not None:
        dirpath, basename = os.path.split(os.path.normpath(path))
        filename, extension = os.path.splitext(basename)

        if not extension or extension.lower() not in output_formats_conf:
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
    :param str file_format: File format: 'inchi', 'mol', 'sdf', 'json', or 'csv'.
    :return: None.
    :rtype: :py:obj:`None`
    """
    file_format = file_format.lower()

    if file_format not in output_formats_conf:
        raise ValueError('Unknown output format: "{}".\n'
                         'Available formats are: {}'.format(file_format, output_formats_conf))

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
