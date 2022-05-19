import pandas as pd
from modules.database import lectorDB
from modules.database.lectorDB import Lector_BD, BD_usuarios, Usuario
from config.definitions import CARPETA_RAIZ
from sqlalchemy import create_engine

path = CARPETA_RAIZ + "/data/statistics.db"
uwu  = BD_usuarios(path, "usuarios")
print(uwu.obtener_dataframe())
daniel = Usuario(4, "soroArx5#", "Hombre", 18, "Giovanna", "Rayo")
#uwu.editar_telefono_usuario(daniel, 55551117)



#POR SI LA LIO CON LOS NOMBRES
# uwu = Lector_BD(path, "usuarios")
# temp_data = uwu.obtener_dataframe()
# print(temp_data)
# temp_data.drop(["level_0", "index"], axis=1, inplace=True)
# temp_data.reset_index(inplace=True)
# temp_data.rename({"index":"telefono"}, axis=1, inplace=True)
# uwu.DATOS = temp_data
# uwu.escribir_database()
# print(temp_data)
