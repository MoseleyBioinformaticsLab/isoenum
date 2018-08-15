#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum.utils
~~~~~~~~~~~~~

This module provides reusable utility functions.
"""

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def is_url(path):
    """Test if path represents a valid URL.
    :param str path: Path to file.
    :return: True if path is valid url string, False otherwise.
    :rtype: :py:obj:`True` or :py:obj:`False`
    """
    try:
        parse_result = urlparse(path)
        return all((parse_result.scheme, parse_result.netloc, parse_result.path))
    except ValueError:
        return False
