from enum import Enum;

class DatosUsuario(Enum):
    ID = 'id';
    EDAD = 'edad';
    USUARIO = 'usuario';
    TELEFONO = 'telefono';
    
class DatosBusqueda(Enum):
    VALOR = 'valor';
    CONTEO = 'conteo';

class ModoOrden(Enum):
    ASC = 'ASC';
    DESC = 'DESC';