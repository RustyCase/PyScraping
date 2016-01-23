# PyScraping\os_helpers\__init__.py
"""Helpful utilities for OS related operations"""

import os
import errno

def ensure_directory(dirpath):
    """Checks to see if the directory at dirpath exists. If not, this function will create it.
        
    Args:
        dirpath (str): The path to the directory that will be checked.
    Raises:
        OSError: If there is an issue making the directory.
    """ 
    try:
        os.makedirs(dirpath)
    except OSError as ose:
        if ose.errno != errno.EEXIST:
            raise
    