# -*- coding: utf-8 -*-
"""Generic helper functions for the sacffolding framework"""


def fix_path(path):
    """
    Simple function for appending a '/' character on the end of a path if it is
    missing.

    :param path: url path
    :returns: path appended with '/'
    """
    if not path.endswith('/'):
        path += '/'
    return path
