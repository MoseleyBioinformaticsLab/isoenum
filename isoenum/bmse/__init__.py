#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This package provides routines to associate spectral transitions lines from
bmse entries with corresponding atoms and generate partial isotopologue ``InChI``
for those transition lines.

This package includes the following modules:

``bmse``
    This module provides routines to extract information from bmse entries 
    and insert assigned .

``ccm``
    This module uses coupling constants matrix to calculate transition lines assignment 
    within bmse entries.
    
``namebmse``
    This module provides routines to execute "namebmse" CLI command.
"""

import logging

__version__ = '0.1.0'


try:  # Python 2/3 compatibility code
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


# Setting default logging handler
logging.getLogger(__name__).addHandler(NullHandler())
