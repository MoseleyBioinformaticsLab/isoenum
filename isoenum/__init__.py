#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This package provides routines to generate isotopically-resolved ``InChI`` 
(International Chemical Identifier) from non-isotopically labeled ``CTfile``
formatted files (e.g. ``Molfiles``, ``SDfiles``) or non-isotopically labeled 
InChI identifiers.

This package includes the following modules:

``cli``
    This module provides the command-line interface for the ``isoenum`` package.

``labeling``
    This module provides functions for generating a labeling schema.

``nmr``
    This module provides descriptions of coupling combinations that
    could be observed within NMR experiments.

``openbabel``
    This module provides functions to call the Open Babel software to convert 
    between ``InChI`` and ``CTfile`` formatted files. 

``conf``
    This module provides the processing of configuration files necessary for 
    isotopic enumerator.

``fileio``
    This module provides functions for generating ``CTfile`` objects and
    convert ``CTfile`` objects into ``InChI``.

``utils``
    This module provides reusable utility functions.
"""

import logging

from . import fileio
from . import api
from . import openbabel


__version__ = '0.4.0'


try:  # Python 2/3 compatibility code
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


# Setting default logging handler
logging.getLogger(__name__).addHandler(NullHandler())
