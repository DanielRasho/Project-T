import sqlite3;

connection = sqlite3.connect('data/statistics.db');
db = connection.cursor();

#Iniciar base de datos
def iniciar_db():
    query = 'CREATE TABLE IF NOT EXISTS "users" ("id" INTEGER NOT NULL UNIQUE, "usuario" TEXT, "telefono" INTEGER, "edad" INTEGER, PRIMARY KEY("id" AUTOINCREMENT))';
    db.execute(query);

def crear_usuario(usuario, telefono, edad):
    query = 'INSERT INTO users (usuario, telefono, edad) VALUES (?, ?, ?)';
    db.execute(query, (usuario, telefono, edad));

iniciar_db();
crear_usuario('usuario2', 566, 18);

for row in db.execute('SELECT * FROM users'):
    print(row)