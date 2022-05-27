from typing import List
from .campos_DB import Campos_Usuario

class Usuario:
    TELEFONO = ""
    CONTRASENA = ""
    GENERO = ""
    EDAD = ""
    NOMBRE = ""
    APELLIDO = ""
    BUSCA_TRABAJO: bool = False
    BUSCA_TRABAJADOR: bool = False
    CONTACTOS: List[int] = []
    OCUPACIONES: List[str] = []

    def __init__(
        self,
        telefono: int,
        contrasena: str,
        genero: str,
        edad: int,
        nombre: str,
        apellido: str,
        busca_trabajo: bool,
        busca_trabajador = bool
    ) -> None:
        self.TELEFONO = telefono
        self.CONTRASENA = contrasena
        self.GENERO = genero
        self.EDAD = edad
        self.NOMBRE = nombre
        self.APELLIDO = apellido
        self.BUSCA_TRABAJO = busca_trabajo
        self.BUSCA_TRABAJADOR = busca_trabajador

    def user_as_dict(self, campos_ignorados:list=[]):
        usuario = {
            Campos_Usuario.TELEFONO: self.TELEFONO,
            Campos_Usuario.CONTRASENA: self.CONTRASENA,
            Campos_Usuario.GENERO: self.GENERO,
            Campos_Usuario.EDAD: self.EDAD,
            Campos_Usuario.NOMBRE: self.NOMBRE,
            Campos_Usuario.APELLIDO: self.APELLIDO,
            Campos_Usuario.BUSCA_TRABAJO: self.BUSCA_TRABAJO,
            Campos_Usuario.BUSCA_TRABAJADOR: self.BUSCA_TRABAJADOR,
            Campos_Usuario.OCUPACIONES: self.OCUPACIONES,
            Campos_Usuario.CONTACTOS: self.CONTACTOS
        }
        for campos in campos_ignorados:
            usuario.pop(campos)
        return usuario

    def establecer_contactos(self, contactos:List[int]) -> None:
        self.CONTACTOS = contactos

    def establecer_ocupaciones(self, ocupaciones: List[str]) -> None:
        self.OCUPACIONES = ocupaciones