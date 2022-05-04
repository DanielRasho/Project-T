import sqlite3;
from database_enums import DatosUsuario, DatosBusqueda, ModoOrden;

connection = sqlite3.connect('data/statistics.db');
db = connection.cursor();

def iniciar_db():
    query_usuarios = 'CREATE TABLE if not exists "usuarios" ("id" INTEGER NOT NULL UNIQUE, "usuario" TEXT, "telefono" INTEGER, "edad" INTEGER, "genero" INTEGER, PRIMARY KEY("id" AUTOINCREMENT))';
    query_busquedas = 'CREATE TABLE if not exists "busquedas" ("valor" TEXT NOT NULL UNIQUE, "conteo" INTEGER DEFAULT 1, PRIMARY KEY("valor"))';
    db.execute(query_usuarios);
    db.execute(query_busquedas);
    connection.commit();

# 0 -> Masculino
# 1 -> Femenino
def crear_usuario(usuario: str, telefono: int, edad: int, genero: int):
    query = 'INSERT INTO usuarios (usuario, telefono, edad, genero) VALUES (?, ?, ?, ?)';
    db.execute(query, (usuario, telefono, edad, genero));
    connection.commit();
    
def obtener_usuarios():
    usuarios = [];
    for row in db.execute('SELECT * FROM usuarios'):
        usuarios.append(row);
    
    return usuarios;

def ordenar_usuarios(columna: DatosUsuario, orden: ModoOrden):
    usuarios = [];
    query = 'SELECT * FROM usuarios ORDER BY {} {}'.format(columna.value, orden.value);
    for row in db.execute(query):
        usuarios.append(row);
    
    return usuarios;

def agrupar_usuarios_por_condicion(columna: DatosUsuario, igual_a):
    usuarios = [];
    query = 'SELECT * FROM usuarios WHERE {}={}'.format(columna.value, igual_a);
    
    for row in db.execute(query):
        usuarios.append(row);
    
    return usuarios;



def crear_busqueda(valor: str):
    valor = valor.strip().lower();
    query = 'INSERT INTO busquedas (valor) values (?) ON CONFLICT(valor) DO UPDATE SET conteo=conteo+1';
    db.execute(query, (valor,));
    connection.commit();

def obtener_busquedas():
    busquedas = [];
    for row in db.execute('SELECT * FROM busquedas'):
        busquedas.append(row);
    
    return busquedas;

def ordenar_busquedas(columna: DatosBusqueda, orden: ModoOrden):
    busquedas = [];
    query = 'SELECT * FROM busquedas ORDER BY {} {}'.format(columna.value, orden.value);
    for row in db.execute(query):
        busquedas.append(row);
    
    return busquedas;



iniciar_db();

#crear_usuario('Juan', 63127865, 20, 0);
#crear_usuario('Marta', 34754211, 17, 1);
#obtener_usuarios();
#ordenar_usuarios(DatosUsuario.EDAD, ModoOrden.DESC);
#agrupar_usuarios_por_condicion(DatosUsuario.GENERO, 1);

#obtener_busquedas();
#crear_busqueda('carpintero');
#ordenar_busquedas(DatosBusqueda.CONTEO, ModoOrden.DESC);