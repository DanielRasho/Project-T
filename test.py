import pandas as pd
from modules.database.lector_DB import BD_contactos, BD_ocupaciones, Lector_BD, BD_usuarios, BD
from config.definitions import CARPETA_RAIZ
from modules.database.campos_DB import Nombres_Tablas
from modules.database.objects_DB import Usuario

ruta = "./data/database.db"

base_de_datos = BD(ruta, Nombres_Tablas.USUARIOS, Nombres_Tablas.CONTACTOS, Nombres_Tablas.OCUPACIONES)
