import pandas as pd
from modules.database.lector_DB import (
    BD_contactos,
    BD_ocupaciones,
    Lector_BD,
    BD_usuarios,
    Base_De_Datos,
)
from modules.database.campos_DB import Nombres_Tablas
from modules.database.objects_DB import Usuario

path = "./data/database.db"
uwu = Lector_BD(path, Nombres_Tablas.OCUPACIONES)


'''

database = Base_De_Datos(path, Nombres_Tablas.USUARIOS, Nombres_Tablas.CONTACTOS, Nombres_Tablas.OCUPACIONES)

marcelo = Usuario(54387323, "marcelo", "HOMBRE", 18, "Marcelo2", "Ruiz", True, False)

marcelo.establecer_contactos([45674545])

marcelo.establecer_ocupaciones(["Dibujante", "papel"])

database.eliminar_cuenta_usuario(marcelo)

database.mostrar_tablas()

'''
