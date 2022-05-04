import pkg_resources    # Functionalities to check project requirements.
from pkg_resources import DistributionNotFound
from definitions import CARPETA_RAIZ
from os import path

"""
This script checks if the user has all dependencies installed. 
    If not, it just stop the execution.
"""

REQUIREMENTS_FILE_PATH = path.join(CARPETA_RAIZ, "requirements.txt")
dependencies = []

with open (REQUIREMENTS_FILE_PATH, "r") as modules_depedencies:
    for modules in modules_depedencies:
        dependencies.append(modules.rstrip())
try:
    pkg_resources.require(dependencies)
except DistributionNotFound:
    print("\nMissing libreries, if you use pip, try running in this location:\n\n\tpython -m pip install -r requirements.txt")
    exit()