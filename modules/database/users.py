from importlib.resources import path
from operator import index
from os import sep
from tkinter.font import names
from unicodedata import name
import pandas as pd
from enum import Enum

class Campos_Usuario(Enum):
    telefono = "TELEFONO"
    contrasena = "CONTRASENA"
    genero ="GENERO"
    edad = "EDAD"
    nombre = "NOMBRE"
    apellido = "APELLIDO"
    etiquetas = "ETIQUETAS"

class Base_de_datos:
    ruta = ""
    def __init__(self, ruta):
        self.ruta = ruta

    def crea_usuario():
        pass

    def elimina_usuario():
        pass

    def buscar_usuario():
        pass

    def existe_usuario():
        pass

    def obtener_propiedades_usuario():
        pass

    def validar_usuario():
        pass

if __name__ == "__main__":
    import os
    ruta = os.path.realpath(os.path.join(__file__, "../../../data/users.csv"))


    def crear_usuario(telefono, contraseña, genero, edad, nombre, apellido, etiquetas):
        datos = pd.read_csv(ruta, sep="|")
        datos = datos.set_index("TELEFONO")
        datos.loc[telefono] = [contraseña, genero, edad, nombre, apellido, etiquetas]
        datos.to_csv(ruta, sep="|")

    def existe_usuario(telefono):
        datos = pd.read_csv(ruta, sep="|")
        datos = datos.set_index("TELEFONO")
        print(datos)
        if (datos.loc[telefono] == telefono).any() == True:
            print("EXITOS")
        else:
            print("TROSTE")
        
    crear_usuario(3432, 1, 2, 3, 4, 5, 6)
    existe_usuario(3433)