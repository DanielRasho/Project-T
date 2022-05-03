import pkg_resources    # Functionalities to check project requirements.
from pkg_resources import DistributionNotFound

"""
This script checks if the user has all dependencies installed. 
    If not, it just stop the execution.
"""
dependencies = []
with open ("requirements.txt", "r") as modules_depedencies:
    for modules in modules_depedencies:
        dependencies.append(modules.rstrip())
try:
    pkg_resources.require(dependencies)
except DistributionNotFound:
    print("\nMissing libreries, if you use pip, try running in this location:\n\n\tpython -m pip install -r requirements.txt")
    exit()