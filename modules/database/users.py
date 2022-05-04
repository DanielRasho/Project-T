import csv

PROPIEDADES_USUARIO = (
    "ID", 
    "CONTRASENA", 
    "NOMBRE", 
    "APELLIDO", 
    "TELEFONO", 
    "TRABAJO")

def actualizar_campos(file_path):
    with open (file_path, 'w') as data_base:
        escritor = csv.reader(data_base, delimiter="|")
        escritor.writeheader(PROPIEDADES_USUARIO)

def crea_usuario():
    pass

def elimina_usuario():
    pass

def buscar_usuario():
    pass

def existe_usuario():
    pass

def obtener_propiedades_usuario():
    pass

def validar_usuario():
    pass