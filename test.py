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

lector = Base_De_Datos(path, Nombres_Tablas.USUARIOS, Nombres_Tablas.CONTACTOS, Nombres_Tablas.OCUPACIONES)

usuario = Usuario(543, "boichi", "Hombre", 23, "Carolyn", "Roldan", True, False)
usuario.establecer_contactos([52, 51, 53])
usuario.establecer_ocupaciones(["carpintero", "pasteles"])

lector.agregar_contacto(usuario, 533)

#lector.registrar_usuario(usuario)

print(lector.busqueda_recursiva_por_ocupacion(usuario, "carpintero"))

lector.mostrar_tablas()
