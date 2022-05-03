import sqlite3;
from database_enums import DatosUsuario, ModoOrden;

connection = sqlite3.connect('data/statistics.db');
db = connection.cursor();

def iniciar_db():
    query_usuarios = 'CREATE TABLE if not exists "usuarios" ("id" INTEGER NOT NULL UNIQUE, "usuario" TEXT, "telefono" INTEGER, "edad" INTEGER, PRIMARY KEY("id" AUTOINCREMENT))';
    query_busquedas = 'CREATE TABLE if not exists "busquedas" ("valor" TEXT NOT NULL UNIQUE, "conteo" INTEGER DEFAULT 1, PRIMARY KEY("valor"))';
    db.execute(query_usuarios);
    db.execute(query_busquedas);
    connection.commit();

def crear_usuario(usuario, telefono, edad):
    query = 'INSERT INTO usuarios (usuario, telefono, edad) VALUES (?, ?, ?)';
    db.execute(query, (usuario, telefono, edad));
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

def crear_busqueda(valor):
    valor = valor.strip().lower();
    query = 'INSERT INTO busquedas (valor) values (?) ON CONFLICT(valor) DO UPDATE SET conteo=conteo+1';
    db.execute(query, (valor,));
    connection.commit();

def obtener_busquedas():
    busquedas = [];
    for row in db.execute('SELECT * FROM busquedas'):
        busquedas.append(row);
    
    return busquedas;

iniciar_db();
#crear_usuario('Juan', 63127865, 20);
#obtener_usuarios();
#ordenar_usuarios(DatosUsuario.EDAD, ModoOrden.DESC);

#obtener_busquedas();
#crear_busqueda('carpintero');