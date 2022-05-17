import sqlite3;
from database_enums import DatosUsuario, DatosBusqueda, ModoOrden;

connection = sqlite3.connect('data/statistics.db');
db = connection.cursor();

def iniciar_db():
    query_usuarios = 'CREATE TABLE if not exists "usuarios" ("telefono" INTEGER NOT NULL UNIQUE, "contrasena" TEXT, "genero" INTEGER, "edad" INTEGER, "nombre" TEXT, "apellido" TEXT, PRIMARY KEY("telefono"))';
    query_busquedas = 'CREATE TABLE if not exists "busquedas" ("valor" TEXT NOT NULL UNIQUE, "conteo" INTEGER DEFAULT 1, PRIMARY KEY("valor"))';
    query_contactos = 'CREATE TABLE if not exists "contactos" ("telefono" INTEGER UNIQUE, "contacto" INTEGER, "id" INTEGER PRIMARY KEY AUTOINCREMENT)';
    query_ocupaciones = 'CREATE TABLE if not exists "ocupaciones" ("telefono" INTEGER UNIQUE, "ocupacion" TEXT, "id" INTEGER PRIMARY KEY AUTOINCREMENT)';
    db.execute(query_usuarios);
    db.execute(query_busquedas);
    db.execute(query_contactos);
    db.execute(query_ocupaciones);
    connection.commit();

# 0 -> Masculino
# 1 -> Femenino
def crear_usuario(telefono: int, usuario: str, edad: int, genero: int):
    query = 'INSERT INTO usuarios (telefono, usuario, edad, genero) VALUES (?, ?, ?, ?)';
    db.execute(query, (telefono, usuario, edad, genero));
    connection.commit();
    
def editar_usuario(telefono: int, columna: DatosUsuario, valor):
    if (columna == DatosUsuario.USUARIO): valor = '"{}"'.format(valor);
    
    query = 'UPDATE usuarios SET {} = {} WHERE telefono = {}'.format(columna.value, valor, telefono);
    db.execute(query);
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

def agrupar_usuarios_por_columna(columna: DatosUsuario):
    usuarios = [];
    query = 'SELECT {}, COUNT(telefono) FROM usuarios GROUP BY {}'.format(columna.value, columna.value);
    
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

#crear_usuario(65331782, 'Pablo', 20, 0);
#crear_usuario(36541287, 'Karla', 19, 1);
#editar_usuario(36541287, DatosUsuario.EDAD, 18);
#obtener_usuarios();
#ordenar_usuarios(DatosUsuario.EDAD, ModoOrden.DESC);
#agrupar_usuarios_por_condicion(DatosUsuario.GENERO, 1);
#agrupar_usuarios_por_columna(DatosUsuario.EDAD);


#obtener_busquedas();
#crear_busqueda('carpintero');
#ordenar_busquedas(DatosBusqueda.CONTEO, ModoOrden.DESC);