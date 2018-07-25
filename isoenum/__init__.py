#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This package provides routines to generate isotopically-resolved ``InChI`` 
(International Chemical Identifier) from non-isotopically labeled ``CTfile``
formatted files (e.g. ``Molfiles``, ``SDfiles``) or non-isotopically labeled 
InChI identifiers.

This package includes the following modules:

``cli``
    This module provides the command-line interface for the ``isoenum`` package.

``conf``
    This module provides the processing of configuration files necessary for 
    isotopic enumerator.

``iso_property``
    This module provides the :func:`~isoenum.iso_property.create_iso_property` 
    function that is responsible for generating the ``Ctab`` properties block (part of 
    ``CTfile`` formatted files specifying "ISO" property for atoms) based on 
    provided labeling schema.

``labeling_schema``
    This module provides functions for generating a labeling schema.

``openbabel``
    This module provides functions to call the Open Babel software to convert 
    between ``InChI`` and ``CTfile`` formatted files. 

``fileio``
    This module provides functions for generating ``CTfile`` objects and
    convert ``CTfile`` objects into ``InChI``.

``utils``
    This module provides reusable utility functions.
"""

import logging

__version__ = '0.1.6dev'


try:  # Python 2/3 compatibility code
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


# Setting default logging handler
logging.getLogger(__name__).addHandler(NullHandler())
