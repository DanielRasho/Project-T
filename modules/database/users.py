import pandas as pd
from enum import Enum

class Campos_Usuario(Enum):
    telefono = "TELEFONO";
    contrasena = "CONTRASENA",
    genero ="GENERO",
    edad = "EDAD", 
    nombre = "NOMBRE", 
    apellido = "APELLIDO", 
    etiquetas = "ETIQUETAS"

class Base_de_datos:
    ruta = ""
    def __init__(self, ruta):
        self.ruta = ruta

    def actualizar_campos(self):
        datos = pd.read_csv()

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