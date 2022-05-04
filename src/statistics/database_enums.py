from enum import Enum;

class DatosUsuario(Enum):
    TELEFONO = 'telefono';
    EDAD = 'edad';
    USUARIO = 'usuario';
    GENERO = 'genero'
    
class DatosBusqueda(Enum):
    VALOR = 'valor';
    CONTEO = 'conteo';

class ModoOrden(Enum):
    ASC = 'ASC';
    DESC = 'DESC';