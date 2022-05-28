from typing import Any, Dict, List
import pandas as pd
from sqlalchemy import create_engine, false, true
import sqlalchemy
import re
from .objects_DB import Usuario
from .campos_DB import (
    Campos_Usuario,
    Campos_Contactos,
    Campos_Ocupacion,
    Nombres_Tablas,
)

# TIPOS
Telefono = int


class Lector_BD:
    RUTA: str = ""
    DATOS: pd.DataFrame = None
    ENGINE: sqlalchemy.engine = None
    NOMBRE_TABLA: str = ""
    CAMPOS: List[str] = []

    def __init__(self, ruta: str, nombre_tabla: str):
        if ruta.endswith(".db") == True:
            self.RUTA = ruta
            self.NOMBRE_TABLA = nombre_tabla
            self.DATOS = self.subir_database()
            self.CAMPOS = self.establecer_campos()
        else:
            raise ('Tipo de archivo incorrecto. Solo archivos ".db" admitidos.')

    def subir_database(self) -> pd.DataFrame:
        if self.RUTA.endswith(".db") == True:
            self.ENGINE = create_engine("sqlite:///" + self.RUTA)
            with self.ENGINE.connect() as conn, conn.begin():
                return pd.read_sql_table(self.NOMBRE_TABLA, self.ENGINE)

    def escribir_database(self) -> None:
        self.DATOS.to_sql(
            self.NOMBRE_TABLA, self.ENGINE, if_exists="replace", index=False
        )

    def establecer_campos(self):
        return self.DATOS.columns.tolist()

    def es_campo_valido(self, campo: str) -> None:
        if campo not in self.CAMPOS:
            raise ("columna_indice no existe en la base de datos actual.")

    def existe_item(
        self, indice_buscado: str | int, columna_indice: str = None
    ) -> bool:
        if columna_indice is not None:
            self.es_campo_valido(columna_indice)
            return (self.DATOS[columna_indice] == indice_buscado).any()
        else:
            return indice_buscado in self.DATOS.index

    def agregar_nuevo_item(
        self, item_id: str | int, campos_item: dict, columna_indice: str = None
    ) -> bool:
        if self.existe_item(item_id, columna_indice=columna_indice) == False:

            if (
                columna_indice is not None
            ):  # Estableciendo indice si columna_indice especificado
                self.es_campo_valido(columna_indice)
                self.DATOS.set_index(columna_indice, inplace=True)

            self.DATOS.loc[item_id] = campos_item  # Agregando el item

            if (
                columna_indice is not None
            ):  # Reestableciendo indice si columna_indice especificado
                self.DATOS.reset_index(inplace=True)

            self.escribir_database()
            return True
        else:
            return False

    def eliminar_item(self, item_id: str | int, columna_indice: str = None) -> bool:
        if self.existe_item(item_id, columna_indice=columna_indice) == False:
            return False
        else:
            if columna_indice is not None:
                self.es_campo_valido(columna_indice)
                self.DATOS.set_index(columna_indice, inplace=True)

            self.DATOS.drop(item_id, axis=0, inplace=True)

            if columna_indice is not None:
                self.DATOS.reset_index(inplace=True)
            self.escribir_database()
            return True

    def editar_item(
        self,
        fila: int | str,
        columna: str,
        nuevo_valor: Any,
        columna_indice: str = None,
    ) -> None:
        self.es_campo_valido(columna)
        if columna_indice == columna:
            raise ("columna y columna_indice, NO pueden ser iguales.")
        if self.existe_item(fila, columna_indice=columna_indice) == False:
            raise ("No existe item con ese indice.")
        if columna_indice is not None:
            self.DATOS.set_index(columna_indice, inplace=True)
        self.DATOS.at[fila, columna] = nuevo_valor
        self.DATOS.reset_index(inplace=True)
        self.escribir_database()

    def editar_item_id(self, id_actual, columna_indice: str, nuevo_id) -> bool:
        self.es_campo_valido(columna_indice)
        if self.existe_item(id_actual, columna_indice=columna_indice) == False:
            raise ("No existe item con ese indice.")
        if self.existe_item(nuevo_id, columna_indice=columna_indice) == True:
            raise ("Ya existe un usuario con ese telefono.")
        self.DATOS.set_index(columna_indice, inplace=True)
        self.DATOS.rename(index={id_actual: nuevo_id}, inplace=True)
        self.DATOS.reset_index(inplace=True)
        self.escribir_database()

    def buscar_items(
        self,
        columna: str,
        valores_buscados: list,
        metodo: str = "exacto",
        ignorar_nulos: bool = True,
    ) -> List[Dict]:
        self.es_campo_valido(columna)
        temp_data = self.DATOS
        items_encontrados = []

        if ignorar_nulos == True:
            temp_data.dropna(inplace=True)

        for valor in valores_buscados:
            coincidencias: pd.DataFrame = None
            if metodo == "exacto":
                coincidencias = temp_data[self.DATOS[columna] == valor]
            elif metodo == "parcial":
                coincidencias = temp_data[
                    self.DATOS[columna].str.contains(valor, flags=re.IGNORECASE)
                ]
            items_encontrados.append(coincidencias)

        return pd.concat(items_encontrados).to_dict(orient="records")

    def obtener_item(self, columna_indice: str, item_id: str | int) -> Dict:
        self.es_campo_valido(columna_indice)
        if self.existe_item(item_id, columna_indice=columna_indice) == True:
            temp_datos = self.DATOS.set_index(columna_indice)
            item_info: Dict = temp_datos.loc[
                item_id
            ].to_dict()  # Return a dict, without the id info
            item_info.update(
                {columna_indice: item_id}
            )  # So here just appending the given id to the dict
            return item_info

    def agregar_campo(self, nombre_campo: str, default_value: Any) -> None:
        if nombre_campo not in self.CAMPOS:
            self.DATOS.insert(
                len(self.DATOS.columns), column=nombre_campo, value=default_value
            )
            self.escribir_database()
        else:
            raise ("Esa columna ya existe en el registro")

    def eliminar_campos(self, nombre_campos: list[str]) -> None:
        if nombre_campos not in self.CAMPOS:
            self.DATOS.drop(nombre_campos, axis=1, inplace=True)
            self.escribir_database()
        else:
            raise ("Esa columna no existe en el registro")

    def renombrar_campo(self, nombre_campo: str, nuevo_nombre: str) -> None:
        if nombre_campo not in self.CAMPOS:
            self.DATOS.rename({nombre_campo: nuevo_nombre}, axis=1, inplace=True)
            self.escribir_database()
        else:
            raise ("Esa columna no existe en el registro")

    def ordenar_dataframe(self, campos, ascendente=True) -> None:
        self.DATOS.sort_values(by=campos, ascending=ascendente)
        self.escribir_database()

    def limpiar_dataframe(self) -> None:
        self.DATOS = self.DATOS.iloc[0:0]
        self.escribir_database()

    def obtener_dataframe(self) -> pd.DataFrame:
        return self.DATOS


class BD_usuarios:
    LECTOR_DB_USUARIOS: Lector_BD = None

    def __init__(self, ruta: str, nombre_tabla_usuarios: Nombres_Tablas):
        self.LECTOR_DB_USUARIOS = Lector_BD(ruta, nombre_tabla_usuarios)

    def existe_usuario(self, telefono: int) -> bool:
        return self.LECTOR_DB_USUARIOS.existe_item(
            telefono, columna_indice=Campos_Usuario.TELEFONO
        )

    def crear_usuario(self, usuario: Usuario) -> bool:
        if usuario is None:
            raise (
                "El parametro usuario es tipo None. Intruzca un objeto de la clase Usuario."
            )
        return self.LECTOR_DB_USUARIOS.agregar_nuevo_item(
            usuario.TELEFONO,
            usuario.user_as_dict(),
            columna_indice=Campos_Usuario.TELEFONO,
        )

    def eliminar_usuario(self, telefono: int) -> bool:
        return self.LECTOR_DB_USUARIOS.eliminar_item(telefono, Campos_Usuario.TELEFONO)

    def validar_usuario(self, telefono: int, contrasena: str) -> bool:
        if self.existe_usuario(telefono) == True:
            datos = self.LECTOR_DB_USUARIOS.obtener_dataframe()
            datos.set_index(Campos_Usuario.TELEFONO, inplace=True)
            if datos.loc[telefono][Campos_Usuario.CONTRASENA] == contrasena:
                datos.reset_index(inplace=True)
                return True
            else:
                return False
        else:
            return False

    def editar_usuario(self, usuario: Usuario):
        if usuario is None:
            raise (
                "El parametro usuario es tipo None. Intruzca un objeto de la clase Usuario."
            )
        nuevos_valores = usuario.user_as_dict(
            campos_ignorados=[
                Campos_Usuario.TELEFONO,
                Campos_Usuario.CONTACTOS,
                Campos_Usuario.OCUPACIONES,
            ]
        ).items()
        for campo, valor in nuevos_valores:
            self.LECTOR_DB_USUARIOS.editar_item(
                usuario.TELEFONO, campo, valor, columna_indice=Campos_Usuario.TELEFONO
            )

    def editar_telefono_usuario(self, usuario: Usuario, nuevo_telefono):
        if usuario is None:
            raise (
                "El parametro usuario es tipo None. Intruzca un objeto de la clase Usuario."
            )
        self.LECTOR_DB_USUARIOS.editar_item_id(
            usuario.TELEFONO, Campos_Usuario.TELEFONO, nuevo_telefono
        )

    def obtener_propiedades_usuario(self, telefono: int) -> Dict:
        return self.LECTOR_DB_USUARIOS.obtener_item(Campos_Usuario.TELEFONO, telefono)

    def obtener_dataframe(self):
        return self.LECTOR_DB_USUARIOS.obtener_dataframe()


class BD_contactos:
    LECTOR_DB_CONTACTO: Lector_BD = None

    def __init__(self, ruta: str, tabla_contactos: Nombres_Tablas):
        self.LECTOR_DB_CONTACTO = Lector_BD(ruta, tabla_contactos)

    def obtener_contactos_usuario(self, telefono_usuario: int) -> list[Telefono]:
        contactos = self.LECTOR_DB_CONTACTO.buscar_items(
            Campos_Contactos.TELEFONO, [telefono_usuario], metodo="exacto"
        )
        telefonos_contactos = []
        for contacto in contactos:
            telefonos_contactos.append(contacto[Campos_Contactos.CONTACTOS])
        return telefonos_contactos

    def existe_contacto(self, telefono_usuario, telefono_contacto: int) -> bool:
        return telefono_contacto in self.obtener_contactos_usuario(telefono_usuario)

    def agregar_contacto(self, usuario: Usuario, telefono_contacto: int) -> bool:
        if usuario is None:
            raise (
                "El parametro usuario es tipo None. Intruzca un objeto de la clase Usuario."
            )
        if usuario.TELEFONO == telefono_contacto:
            raise ("El telefono del usuario y el contacto, no pueden ser iguales.")
        if self.existe_contacto(usuario.TELEFONO, telefono_contacto) == True:
            return False
        new_index = len(self.LECTOR_DB_CONTACTO.obtener_dataframe().index)
        hubo_exito = self.LECTOR_DB_CONTACTO.agregar_nuevo_item(
            new_index,
            {
                Campos_Contactos.TELEFONO: usuario.TELEFONO,
                Campos_Contactos.CONTACTOS: telefono_contacto,
            },
            columna_indice=None,
        )

        if hubo_exito == True:
            self.LECTOR_DB_CONTACTO.ordenar_dataframe([Campos_Contactos.TELEFONO])
            return True
        else:
            return False

    def eliminar_contacto(self, telefono_usuario, telefono_contacto: int) -> bool:
        if telefono_usuario == telefono_contacto:
            raise ("El telefono del usuario y el contacto, no pueden ser iguales.")
        elif self.existe_contacto(telefono_usuario, telefono_contacto) == True:
            datos = self.LECTOR_DB_CONTACTO.obtener_dataframe()
            contactos_index = datos.index[
                (datos[Campos_Contactos.TELEFONO] == telefono_usuario)
                & (datos[Campos_Contactos.CONTACTOS] == telefono_contacto)
            ].to_list()
            if len(contactos_index) != 0:
                for contacto in contactos_index:
                    self.LECTOR_DB_CONTACTO.eliminar_item(contacto)
                    return True
        return False

    def obtener_dataframe(self):
        return self.LECTOR_DB_CONTACTO.obtener_dataframe()


# ===========================================================


class BD_ocupaciones:
    LECTOR_DB_OCUPACIONES: Lector_BD = None

    def __init__(self, ruta: str, nombre_tabla_usuarios: Nombres_Tablas):
        self.LECTOR_DB_OCUPACIONES = Lector_BD(ruta, nombre_tabla_usuarios)

    def obtener_ocupaciones_usuario(self, telefono_usuario: int) -> list[str]:
        ocupaciones = self.LECTOR_DB_OCUPACIONES.buscar_items(
            Campos_Ocupacion.TELEFONO, [telefono_usuario], metodo="exacto"
        )
        ocupaciones_usuario = []
        for ocupacion in ocupaciones:
            ocupaciones_usuario.append(ocupacion[Campos_Ocupacion.OCUPACION])
        return ocupaciones_usuario

    def existe_ocupacion(self, telefono_usuario, ocupacion_usuario: str) -> bool:
        return ocupacion_usuario in self.obtener_ocupaciones_usuario(telefono_usuario)

    def agregar_ocupacion(self, usuario: Usuario, ocupacion_usuario: str) -> bool:
        if usuario is None:
            raise (
                "El parametro usuario es tipo None. Intruzca un objeto de la clase Usuario."
            )
        if self.existe_ocupacion(usuario.TELEFONO, ocupacion_usuario) == True:
            return False
        new_index = len(self.LECTOR_DB_OCUPACIONES.obtener_dataframe().index)
        hubo_exito = self.LECTOR_DB_OCUPACIONES.agregar_nuevo_item(
            new_index,
            {
                Campos_Ocupacion.TELEFONO: usuario.TELEFONO,
                Campos_Ocupacion.OCUPACION: ocupacion_usuario,
            },
            columna_indice=None,
        )
        if hubo_exito == True:
            self.LECTOR_DB_OCUPACIONES.ordenar_dataframe([Campos_Contactos.TELEFONO])
            return True
        else:
            return False

    def eliminar_ocupacion(self, usuario: Usuario, ocupacion_usuario: str) -> bool:
        if usuario is None:
            raise (
                "El parametro usuario es tipo None. Intruzca un objeto de la clase Usuario."
            )
        if self.existe_contacto(usuario, ocupacion_usuario) == True:
            datos = self.LECTOR_DB_OCUPACIONES.obtener_dataframe()
            ocupaciones_index = datos.index[
                (datos[Campos_Ocupacion.TELEFONO] == usuario.TELEFONO)
                & (datos[Campos_Ocupacion.OCUPACION] == ocupacion_usuario)
            ].to_list()
            if len(ocupaciones_index) != 0:
                for ocupacion in ocupaciones_index:
                    self.LECTOR_DB_OCUPACIONES.eliminar_item(ocupacion)
                    return True
        return False

    def obtener_dataframe(self):
        return self.LECTOR_DB_OCUPACIONES.obtener_dataframe()


class Base_De_Datos(BD_usuarios, BD_contactos, BD_ocupaciones):
    def __init__(
        self,
        ruta: str,
        nombre_tabla_usuarios,
        nombre_tabla_contactos,
        nombre_tabla_ocupaciones,
    ) -> None:
        BD_usuarios.__init__(self, ruta, nombre_tabla_usuarios)
        BD_contactos.__init__(self, ruta, nombre_tabla_contactos)
        BD_ocupaciones.__init__(self, ruta, nombre_tabla_ocupaciones)

    def obtener_usuario(self, telefono: int, contrasena: str) -> Usuario:
        if self.validar_usuario(telefono, contrasena) == True:
            campos_usuario = self.obtener_propiedades_usuario(telefono)
            ocupaciones_usuario = self.obtener_ocupaciones_usuario(telefono)
            contactos_usuario = self.obtener_contactos_usuario(telefono)
            usuario = Usuario(**campos_usuario)
            usuario.establecer_contactos(contactos_usuario)
            usuario.establecer_ocupaciones(ocupaciones_usuario)
            return usuario

    def registrar_usuario(self, usuario: Usuario) -> bool:
        a = True
        b = True
        c = True
        if usuario is None:
            raise (
                "El parametro usuario es tipo None. Intruzca un objeto de la clase Usuario."
            )
        if self.validar_usuario(usuario.TELEFONO, usuario.CONTRASENA) == False:
            a = self.crear_usuario(usuario)
            for contacto in usuario.CONTACTOS:
                b = self.agregar_contacto(usuario, contacto)
            for ocupacion in usuario.OCUPACIONES:
                c = self.agregar_ocupacion(usuario, ocupacion)
            if a == False:
                raise ("Hubo un error al crear el usuario.")
            elif b == False:
                raise ("Hubor un error al agregar los contactos")
            elif c == False:
                raise ("Hubo un error al agregar las ocupaciones")
            else:
                return True
        return False

    def eliminar_cuenta_usuario(self, telefono_usuario, contrasena: str) -> bool:
        a = True
        b = True
        c = True
        usuario = self.obtener_usuario(telefono_usuario, contrasena)
        if usuario is None:
            raise (
                "El telefono y contrasena dados no corresponde con ningun usuario registrado."
            )
        a = self.eliminar_usuario(usuario.TELEFONO)
        for contacto in usuario.CONTACTOS:
            b = self.eliminar_contacto(usuario.TELEFONO, contacto)
        for ocupacion in usuario.OCUPACIONES:
            c = self.eliminar_ocupacion(usuario, ocupacion)
        if a == False:
            raise ("Hubo un error al eliminar el usuario.")
        elif b == False:
            raise ("Hubor un error al eliminar los contactos")
        elif c == False:
            raise ("Hubo un error al eliminar las ocupaciones")
        else:
            return True

    def busqueda_recursiva_por_ocupacion(
        self, usuario: Usuario, ocupacion: str
    ) -> list[Telefono]:
        if usuario is None:
            raise (
                "El parametro usuario es tipo None. Intruzca un objeto de la clase Usuario."
            )
        posibles_telefonos = set()
        coincidencias_finales = []
        contactos_usuario = self.obtener_contactos_usuario(usuario.TELEFONO)
        posibles_telefonos.update(contactos_usuario)
        for contacto in contactos_usuario:
            temp_contactos = set(self.obtener_contactos_usuario(contacto))
            posibles_telefonos.union(temp_contactos)
        posibles_telefonos.update(contactos_usuario)

        for telefono in posibles_telefonos:
            if self.existe_ocupacion(telefono, ocupacion) == True:
                coincidencias_finales.append(telefono)

        return coincidencias_finales

    def mostrar_tablas(self) -> None:
        print(self.LECTOR_DB_USUARIOS.obtener_dataframe())
        print(self.LECTOR_DB_OCUPACIONES.obtener_dataframe())
        print(self.LECTOR_DB_CONTACTO.obtener_dataframe())

    def limpiar_tablas(self) -> None:
        self.LECTOR_DB_USUARIOS.limpiar_dataframe()
        self.LECTOR_DB_CONTACTO.limpiar_dataframe()
        self.LECTOR_DB_OCUPACIONES.limpiar_dataframe()


if __name__ == "__main__":
    uwu = Lector_BD("database.db", "usuarios")
    print(uwu.DATOS)
