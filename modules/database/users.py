from typing_extensions import Self
import pandas as pd

PROPIEDADES_USUARIO = (
    "TELEFONO", 
    "CONTRASENA",
    "GENERO",
    "EDAD", 
    "NOMBRE", 
    "APELLIDO", 
    "ETIQUETAS")

class Base_de_datos:
    ruta = ""

    def __init__(self, ruta):
        self.ruta = ruta

    def actualizar_campos(self):
        df = pd.read_csv(self.ruta)
        print(pd)

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