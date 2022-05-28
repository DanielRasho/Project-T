from config.definitions import CARPETA_RAIZ
from modules.database.lector_DB import Base_De_Datos, Lector_BD
from modules.database.objects_DB import Usuario
from modules.database.campos_DB import (
    Campos_Usuario,
    Campos_Ocupacion,
    Campos_Contactos,
    Nombres_Tablas,
)
from modules.interface.menus import (
    menu_builder,
    clean_screen,
    datosANDvalidacion_numeros,
)

RUTA = CARPETA_RAIZ + "/data/database.db"
ESCRITOR_DB = Base_De_Datos(
    RUTA, Nombres_Tablas.USUARIOS, Nombres_Tablas.CONTACTOS, Nombres_Tablas.OCUPACIONES
)
#ESCRITOR_DB.limpiar_tablas()
clean_screen()

# nombre = int(datosANDvalidacion_numeros())
# contra = input("uwu: ")
# print(ESCRITOR_DB.validar_usuario(nombre, contra))

print(
    """
 _____ _                     _           
/  __ \ |                   | |          
| /  \/ |__   __ _ _ __ ___ | |__   __ _ 
| |   | '_ \ / _` | '_ ` _ \| '_ \ / _` |
| \__/\ | | | (_| | | | | | | |_) | (_| |
 \____/_| |_|\__,_|_| |_| |_|_.__/ \__,_|
                                         
                                         
__   __    _                             
\ \ / /   | |                            
 \ V /__ _| |                            
  \ // _` | |                            
  | | (_| |_|                            
  \_/\__,_(_)    

"""
)
input("Presiona <ENTER> para continuar...")



# MAINLOOP

while True:
    opcion = menu_builder(
        "Hola!",
        ["INGRESAR", "REGISTRARME", "SABER MAS", "MOSTRAR TABLAS"],
        "Muevete con las <FLECHAS> del teclado y confirma con <ENTER>",
        return_value=True,
        default_options=["Salir"],
    )

    clean_screen()

    if opcion == "INGRESAR":
        clean_screen()
        print("Ingresa tus datos")
        telefono = int(datosANDvalidacion_numeros())
        contrasena = input("contrasena: ")
        es_valido = ESCRITOR_DB.validar_usuario(telefono, contrasena)
        if es_valido == False:
            input(
                "Su telefono con contrasena no son validos... Pruebe de nuevo.\nPresiona <Enter> para continuar..."
            )
        else:
            opcion = menu_builder(
                "Que quieres hacer?",
                ["BUSCAR POSIBLES TRABAJADORES", "REVISAR MI PERFIL"],
                "Muevete con las <FLECHAS> del teclado y confirma con <ENTER>",
                return_value=True,
            )
            if opcion == "BUSCAR POSIBLES TRABAJADORES":
                busqueda = input("Ingresa la palabra clave para buscar: ")
                usuario = ESCRITOR_DB.obtener_usuario(telefono, contrasena)
                resultados = ESCRITOR_DB.busqueda_recursiva_por_ocupacion(
                    usuario, busqueda
                )
                input(
                    f"Estos son telefonos de gente que te podría ser de interés:\n{resultados}\nPresionar <Enter> para continuar."
                )
            if opcion == "REVISAR MI PERFIL":
                opcion = menu_builder(
                    "Que quieres hacer?",
                    [
                        "AGREGAR CONTACTO",
                        "ELIMINAR CONTACTO",
                        "AGREGAR OFICIO",
                        "ELIMINAR OFICIO",
                    ],
                    "Muevete con las <FLECHAS> del teclado y confirma con <ENTER>",
                    return_value=True,
                    default_options=["Salir"],
                )
                if opcion == "AGREGAR CONTACTO":
                    usuario = ESCRITOR_DB.obtener_usuario(telefono, contrasena)
                    telefono_contacto = int(datosANDvalidacion_numeros())
                    ESCRITOR_DB.agregar_contacto(usuario, telefono_contacto)
                elif opcion == "ELIMINAR CONTACTO":
                    usuario = ESCRITOR_DB.obtener_usuario(telefono, contrasena)
                    telefono_contacto = int(datosANDvalidacion_numeros())
                    ESCRITOR_DB.eliminar_contacto(usuario.TELEFONO, telefono_contacto)
                elif opcion == "AGREGAR OFICIO":
                    usuario = ESCRITOR_DB.obtener_usuario(telefono, contrasena)
                    ocupacion = input("Ingresa tu ocupacion:")
                    ESCRITOR_DB.agregar_ocupacion(usuario, ocupacion)
                elif opcion == "ELIMINAR OFICIO":
                    usuario = ESCRITOR_DB.obtener_usuario(telefono, contrasena)
                    ocupacion = input("Ingresa tu ocupacion:")
                    ESCRITOR_DB.eliminar_ocupacion(usuario.TELEFONO, ocupacion)
                elif opcion == "Salir":
                    pass

    elif opcion == "REGISTRARME":
        clean_screen()
        print("Genial! Empezemos a ello!")
        nombre = input("Ingresa tu nombres: \n")
        apellido = input("Ingresa tus apellidos: \n")
        genero = menu_builder(
            "¿Cuál es tu sexo?",
            ["HOMBRE", "MUJER"],
            "Muevete con las <FLECHAS> del teclado y confirma con <ENTER>",
            return_value=True,
        )
        edad = 0
        while True:
            try:
                edad = int(input("Ingresa tu edad: \n"))
                break
            except:
                print("No es un numero valido")
        contrasena = input("Cual va a ser tu contraseña?")
        telefono = int(datosANDvalidacion_numeros())
        usuario = Usuario(
            telefono, contrasena, genero, edad, nombre, apellido, True, True
        )

        try:
            hubo_exito = ESCRITOR_DB.registrar_usuario(usuario)
        except:
            print("Oops... parece que ya existe un usuario con esos datos.")

        input(
            "EXITOS, hemos creado un usuario para ti con esos datos!\nPresiona <ENTER>"
        )

    elif opcion == "SABER MAS":
        print(
            "Este es un programa que te recomienda posibles trabajadores basados en las recomendacione de tus amigos."
        )
        print(
            "Dado la falta de tiempo, el codigo tiene muchas funciones y modulos que no se pudieron implementar, en el flujo final."
        )
        input("Presionar <Enter> para regresar...")
    elif opcion == "MOSTRAR TABLAS":
        ESCRITOR_DB.mostrar_tablas()
        input("Presiona <Enter> para continuar...")

    elif opcion == "Salir":
        exit()
