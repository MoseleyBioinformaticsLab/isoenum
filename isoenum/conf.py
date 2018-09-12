#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
isoenum.conf
~~~~~~~~~~~~

This module provides processing of configuration files necessary for 
isotopic enumerator.
"""

import os
import json


this_directory = os.path.abspath(os.path.dirname(__file__))
isotopes_path = '{}/config_files/isotopes.json'.format(this_directory)
output_formats_path = '{}/config_files/formats.json'.format(this_directory)

with open(isotopes_path, 'r') as infile:
    isotopes_conf = json.load(infile)

with open(output_formats_path, 'r') as infile:
    output_formats_conf = set(json.load(infile))
