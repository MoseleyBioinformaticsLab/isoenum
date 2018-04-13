#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

from ctfile.conf import ctab_properties_conf


def create_iso_property(labeling_schema, ctab_properties_conf=ctab_properties_conf, version='V2000'):
    """Create "ISO" property block.

    :param list labeling_schema: Labeling schema containing info about atom, isotope, and its position.
    :param str version: Version of ``CTfile``.
    """
    iso_property_fmt = ctab_properties_conf[version]['ISO']['fmt']
    atom_iso_property = '{}  1{}{}'
    ctab_properties_block = [atom_iso_property.format(iso_property_fmt,
                                                      str(i['position']).rjust(4),
                                                      str(i['isotope']).rjust(4))
                             for i in labeling_schema]
    return ctab_properties_block
