#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum.openbabel
~~~~~~~~~~~~~~~~~

This module provides :func:`~isoenum.openbabel.convert` to convert between ``InChI``, ``SMILES``, 
and ``Molfile`` formatted files. 
"""

import subprocess

try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


def _test_openbabel():
    """Test if Open Babel software is installed.
    
    :return: None.
    :rtype: :py:obj:`None`
    """
    try:
        openbabel_version_test = subprocess.check_output(['obabel', '-V'])
        openbabel_version = openbabel_version_test.decode('utf-8')
        if not openbabel_version.startswith('Open Babel'):
            raise SystemExit('Open Babel version information cannot be found: {}'.format(openbabel_version))
    except OSError:
        raise SystemExit('Open Babel software is not installed, exiting. '
                         'See installation instructions to get Open Babel '
                         'software for your system: http://openbabel.org/wiki/Get_Open_Babel')


def convert(input_file_path, output_file_path, input_format, output_format, **options):
    """Convert between formats using Open Babel.
    
    :param str input_file_path: Path to input file.
    :param str output_file_path: Path to output file.
    :param str input_format: Input file format.
    :param str output_format: Output file format.
    :param options: Additional key-value options to pass to Open Babel.
    :return: None.
    :rtype: :py:obj:`None` 
    """
    _test_openbabel()

    cmd = ['obabel', '-i{}'.format(input_format), '{}'.format(input_file_path),
           '-o{}'.format(output_format), '-O{}'.format(output_file_path)]

    if options:
        cmd.append('{}'.format(' '.join(options.values())))

    subprocess.call(cmd, shell=False, stdout=DEVNULL, stderr=subprocess.STDOUT)
