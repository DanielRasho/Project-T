from typing import List
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

    def existe_usuario(self, telefono:int):
        # PARAMETROS: telefono del usuario
        # RETORNA: Bool
        # Verifica si un usuario con el telefono dado existe. Devuelve True si existe
        # False si no existe.
        datos = pd.read_csv(self.ruta, sep="|")
        if (datos[Campos_Usuario.telefono.value] == telefono).any() == True:
            return True
        else:
            return False

    def crear_usuario(self, telefono:int, contraseña:str, genero:str, edad:int, nombre:str, apellido:str, etiquetas:list):
        # PARAMETROS: los dichos arriba. 
        # RETORNA: Nada
        # Anade una nueva linea al .csv con los datos del usuario dados
        datos = pd.read_csv(self.ruta , sep="|")
        datos.set_index(Campos_Usuario.telefono.value, inplace=True)
        if self.existe_usuario(telefono) == False:
            datos.loc[telefono] = [contraseña, genero, edad, nombre, apellido, etiquetas]
            datos.to_csv(self.ruta, sep="|")
    
    def elimina_usuario(self, telefono):
        # PARAMETROS: telefono del usuario
        # RETORNA: Nada 
        # Quita la linea que contenga el telefono del usuario dado en el .csv 
        datos = pd.read_csv(self.ruta, sep="|")
        datos.set_index(Campos_Usuario.telefono.value, inplace=True)
        if self.existe_usuario(telefono) == True:
            datos.drop(telefono, axis=0, inplace=True)
            datos.to_csv(self.ruta, sep="|")
    
    def validar_usuario(self, telefono, contrasena):
        # PARAMETROS: telefono y contrasena del usuario
        # RETORNA: Bool
        # Devuelve True si las credenciales dadas coinciden con las guardadas,
        # False si no coinciden.
        datos = pd.read_csv(self.ruta, sep="|")
        datos.set_index(Campos_Usuario.telefono.value, inplace=True)
        if self.existe_usuario(telefono) == True:
            if datos.loc[telefono][Campos_Usuario.contrasena.value] == contrasena:
                return True
            else:
                return False
        else:
            return False

    def buscar_contactos(self, etiqueta:str):
        # PARAMETROS: Palabra a buscar, NOTA solo puede ser uno
        # RETORNA: Lista de numeros telefonicos
        # Devuelve una lista con los numeros de telefono de personas que cumplen con los valores buscados
        datos = pd.read_csv(self.ruta, sep="|")
        datos_etiquetas = datos[[Campos_Usuario.telefono.value, Campos_Usuario.etiquetas.value]]
        usuarios = datos_etiquetas[datos_etiquetas[Campos_Usuario.etiquetas.value].str.contains(etiqueta)]
        return usuarios[Campos_Usuario.telefono.value].to_list()

    def actualizar_usuario(self, telefono, field:Campos_Usuario, nuevo_valor):
        # PARAMETROS: field, es un miembro de la clase Campos_Usuario.
        # RETORNA: Nada.
        # Cambiar el dato de un usuario, EXCEPTO, el numero de telefono.
        datos = pd.read_csv(self.ruta, sep="|")
        datos.set_index(Campos_Usuario.telefono.value, inplace=True)
        if self.existe_usuario(telefono) == True:
            datos.at[telefono, field.value] = nuevo_valor
            datos.to_csv(self.ruta, sep="|")
        
    def obtener_propiedades_usuario(self, telefono):
        # PARAMETROS: telefono del usuario del que se quiere saber
        # RETORNA: Diccionario en formato {"CAMPO": valor ...}. Ej: {"CONTRASENA": "3421", "GENERO" : "HOMBRE" ...}
        # Devuelve un diccionario con todos los campos del usuario con sus valores, sin contar el telefono
        datos = pd.read_csv(self.ruta, sep="|")
        datos.set_index(Campos_Usuario.telefono.value, inplace=True)
        if self.existe_usuario(telefono) == True:
            return datos.loc[telefono].to_dict()

if __name__ == "__main__":
    import os
    uwu = Base_de_datos("test.csv")
    print(uwu.buscar_contactos("a"))