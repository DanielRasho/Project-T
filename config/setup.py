import pkg_resources    # Functionalities to check project requirements.
from pkg_resources import DistributionNotFound
from os import path, _exit
import sys
import subprocess
from config.definitions import CARPETA_RAIZ

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
    try :
        opcion = input("\nDEPENDENCIAS FALTANTES: quieres instalarlas?\nSi[s], No[n]:")
        if opcion == 's':
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r' , REQUIREMENTS_FILE_PATH])
            input("\n\n\tINSTALACION TERMINADA. presiona <Enter> para continuar...\n")
        elif opcion == 'n':
            print("Abortando instalacion...")
            _exit(1)
        else:
            print("Opcion no valida, abortando ejecucion.")
            _exit(1)
    except:
        print("Pip parece no estar instalado, intenta ejecutar el siguiente comando:\n\n\tpython -m ensurepip --upgrade")
        _exit(1)
