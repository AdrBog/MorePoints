"""
This module contains methods related to the configuration of the points.
"""
from .misc import *

def read_point_config(id):
    """
    This method reads the configuration found in the point configuration file. (<code>config/points/{POINT_ID}.point</code>)

    :return: Point configuration dict
    """
    if (id.endswith('.point')):
        return readJSON(f"{POINTS_CONFIG_DIR}/{id}")
    else:
        return readJSON(f"{POINTS_CONFIG_DIR}/{id}.point")
