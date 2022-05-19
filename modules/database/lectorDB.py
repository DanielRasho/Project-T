from typing import Any, Dict, List
import pandas as pd
from sqlalchemy import create_engine, true
import sqlalchemy
import re
from .campos_DB import Campos_Usuario, Campos_Contactos, Campos_Ocupacion, Nombres_Tablas

class Lector_BD:
    RUTA:str = ""
    DATOS:pd.DataFrame = None
    ENGINE:sqlalchemy.engine = None
    NOMBRE_TABLA:str = ""
    CAMPOS:List[str] = []

    def __init__(self, ruta:str, nombre_tabla:str):
        if ruta.endswith(".db") == True:
            self.RUTA = ruta
            self.NOMBRE_TABLA = nombre_tabla
            self.DATOS = self.subir_database()
            self.CAMPOS = self.establecer_campos()
        else:
            raise("Tipo de archivo incorrecto. Solo archivos \".db\" admitidos.")   

    def subir_database(self) -> pd.DataFrame:
        if self.RUTA.endswith(".db") == True:
            self.ENGINE = create_engine("sqlite:///" + self.RUTA)
            with self.ENGINE.connect() as conn, conn.begin():
                return pd.read_sql_table(self.NOMBRE_TABLA, self.ENGINE)

    
    def escribir_database(self) -> None:
        self.DATOS.to_sql(self.NOMBRE_TABLA, self.ENGINE, if_exists="replace", index=False)

    def establecer_campos(self):
        return self.DATOS.columns.tolist()
    
    def es_campo_valido(self, campo:str) -> None:
        if campo not in self.CAMPOS:
            raise("columna_indice no existe en la base de datos actual.")

    def existe_item(self, columna_indice:str, indice_buscado:str|int) -> bool:
        self.es_campo_valido(columna_indice)
        if (self.DATOS[columna_indice] == indice_buscado).any() == True:
            return True
        else:
            return False

    def agregar_nuevo_item(self, columna_indice:str, item_id: str|int , campos_item:dict) -> bool:
        self.es_campo_valido(columna_indice)
        if self.existe_item(columna_indice, item_id) == False:
                self.DATOS.set_index(columna_indice, inplace=True)
                self.DATOS.loc[item_id] = campos_item
                self.DATOS.reset_index(inplace=True)
                self.escribir_database()
                return True
        else:
            return False

    def eliminar_item(self, columna_indice:str, item_id: str|int) -> bool:
        self.es_campo_valido(columna_indice)
        if self.existe_item(columna_indice, item_id) == True:
            self.DATOS.set_index(columna_indice, inplace=True)
            self.DATOS.drop(item_id, axis=0, inplace=True)
            self.DATOS.reset_index(inplace=True)
            self.escribir_database()
            return True
        else:
            return False

    def editar_item(self, fila:int|str, columna:str, nuevo_valor: Any, columna_indice:str = None) -> None:
        self.es_campo_valido(columna)
        if columna_indice == columna:
            raise("columna y columna_indice, NO pueden ser iguales.")
        if self.existe_item(columna_indice, fila) == False:
            raise("No existe item con ese indice.")
        if columna is not None:
            self.DATOS.set_index(columna_indice, inplace=True)
        self.DATOS.at[fila, columna] = nuevo_valor
        self.DATOS.reset_index(inplace=True)
        self.escribir_database()

    def editar_item_id(self, id_actual, columna_indice:str, nuevo_id) -> bool:
        self.es_campo_valido(columna_indice)
        if self.existe_item(columna_indice, id_actual) == False:
            raise("No existe item con ese indice.")
        if self.existe_item(columna_indice, nuevo_id) == True:
            raise("Ya existe un usuario con ese telefono.")
        self.DATOS.set_index(columna_indice, inplace=True)
        self.DATOS.rename(index = {id_actual : nuevo_id}, inplace=True)
        self.DATOS.reset_index(inplace=True)
        self.escribir_database()

    def buscar_items(self,  columna:str, valores_buscados:list, metodo:str = "exacto") -> List[Dict]:
        self.es_campo_valido(columna)
        items_encontrados =[]
        for valor in valores_buscados:
            coincidencias:pd.DataFrame = None
            if metodo == "exacto":
                coincidencias = self.DATOS.loc[self.DATOS[columna] == valor]
            elif metodo == "parcial":
                coincidencias = self.DATOS.loc[self.DATOS[columna].str.contains(valor, flags=re.IGNORECASE)]
            items_encontrados.append(coincidencias)
        return pd.concat(items_encontrados).to_dict(orient = "records")

    def obtener_item(self, columna_indice:str, item_id: str|int) -> Dict:
        self.es_campo_valido(columna_indice)
        if self.existe_item(columna_indice, item_id) == True:
            temp_datos = self.DATOS.set_index(columna_indice)
            item_info:Dict = temp_datos.loc[item_id].to_dict()  # Return a dict, without the id info
            item_info.update({columna_indice: item_id})         # So here just appending the given id to the dict
            return item_info

    def agregar_campo(self, nombre_campo:str, default_value: Any) -> None:
        if nombre_campo not in self.CAMPOS:
            self.DATOS.insert(column=nombre_campo, value=default_value)
            self.escribir_database()
        else:
            raise("Esa columna ya existe en el registro")

    def eliminar_campos(self, nombre_campos:str|list) -> None:
        if nombre_campos not in self.CAMPOS:
            self.DATOS.drop(nombre_campos, axis=1,inplace=True)
            self.escribir_database()
        else:
            raise("Esa columna no existe en el registro")

    def renombrar_campo(self, nombre_campo:str, nuevo_nombre:str) -> None:
        if nombre_campo not in self.CAMPOS:
            self.DATOS.rename({nombre_campo: nuevo_nombre}, axis=1, inplace=True)
            self.escribir_database()
        else:
            raise("Esa columna no existe en el registro")

    def obtener_dataframe(self) -> pd.DataFrame:
        return self.DATOS


class Usuario:
    TELEFONO = ""
    CONTRASENA = ""
    GENERO = ""
    EDAD = ""
    NOMBRE = ""
    APELLIDO = ""

    def __init__(
        self,
        telefono: int,
        contrasena: str,
        genero: str,
        edad: int,
        nombre: str,
        apellido: str,
    ) -> None:
        self.TELEFONO = telefono
        self.CONTRASENA = contrasena
        self.GENERO = genero
        self.EDAD = edad
        self.NOMBRE = nombre
        self.APELLIDO = apellido
        
    def user_as_dict(self, devolver_telefono = True):
        usuario = {
            Campos_Usuario.TELEFONO : self.TELEFONO,
            Campos_Usuario.CONTRASENA : self.CONTRASENA,
            Campos_Usuario.GENERO : self.GENERO,
            Campos_Usuario.EDAD : self.EDAD,
            Campos_Usuario.NOMBRE : self.NOMBRE,
            Campos_Usuario.APELLIDO : self.APELLIDO
            }
        if devolver_telefono == True:
            return usuario
        else:
            usuario.pop("telefono")
            return usuario

class BD_usuarios:
    LECTOR_DB:Lector_BD = None

    def __init__(self, ruta:str, nombre_tabla_usuarios:Nombres_Tablas):
        self.LECTOR_DB = Lector_BD(ruta, nombre_tabla_usuarios)

    def existe_usuario(self, telefono: int) -> bool:
        return self.LECTOR_DB.existe_item(Campos_Usuario.TELEFONO, telefono)

    def crear_usuario(self, usuario: Usuario) -> bool:
        return self.LECTOR_DB.agregar_nuevo_item(Campos_Usuario.TELEFONO, usuario.TELEFONO, usuario.user_as_dict())

    def eliminar_usuario(self, usuario:Usuario) -> bool:
        return self.LECTOR_DB.eliminar_item(Campos_Usuario.TELEFONO, usuario.TELEFONO)

    def validar_usuario(self, telefono: int, contrasena: str) -> Usuario:
        if self.existe_usuario(telefono) == True:
            datos = self.LECTOR_DB.obtener_dataframe()
            datos.set_index(Campos_Usuario.TELEFONO)
            if datos.loc[telefono][Campos_Usuario.CONTRASENA] == contrasena:
                return True
        return False

    def editar_usuario(self, usuario:Usuario):
        nuevos_valores = usuario.user_as_dict(devolver_telefono=False).items()
        for campo, valor in nuevos_valores:
            self.LECTOR_DB.editar_item(usuario.TELEFONO, campo, valor, columna_indice=Campos_Usuario.TELEFONO)

    def editar_telefono_usuario(self, usuario:Usuario, nuevo_telefono):
        self.LECTOR_DB.editar_item_id(usuario.TELEFONO, Campos_Usuario.TELEFONO, nuevo_telefono)

    def obtener_propiedades_usuario(self, telefono:int):
        return self.LECTOR_DB.obtener_item(Campos_Usuario.TELEFONO, telefono)

    def obtener_dataframe(self):
        return self.LECTOR_DB.obtener_dataframe()

class BD_contactos:
    LECTOR_DB:Lector_BD = None
    def __init__(self, ruta:str, tabla_ocupaciones:Nombres_Tablas):
        self.LECTOR_DB = Lector_BD(ruta, tabla_ocupaciones)
    def agregar_contacto(self, usuario:Usuario, oficio:str) -> bool:
        pass
    def eliminar_contacto(self, usuario:Usuario, oficio:str) -> bool:
        pass
    def obtener_contactos_usuario(self, usuario:Usuario) -> dict:
        pass

class BD_ocupaciones:
    LECTOR_DB:Lector_BD = None
    def __init__(self, ruta:str, nombre_tabla_usuarios:Nombres_Tablas):
        self.LECTOR_DB = Lector_BD(ruta, nombre_tabla_usuarios)

    def agregar_ocupacion(self, usuario:Usuario, oficio:str) -> bool:
        pass
    def eliminar_ocupacion(self, usuario:Usuario, oficio:str) -> bool:
        pass
    def obtener_ocupaciones_usuario(self, usuario:Usuario) -> dict:
        pass
    def buscar_por_ocupacion(self, oficio:str) -> List[dict]:
        pass

if __name__ == "__main__":
    uwu = Lector_BD("statistics.db", "usuarios")
    print(uwu.DATOS)
