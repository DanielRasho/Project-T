import config.setup
try:
    import curses
except:
    print("curses is not installed, try running:\npython -m pip install windows-curses")
    exit()
from modules.interface.menus import *
from typing import Tuple
from config.definitions import CARPETA_RAIZ
from modules.database.lector_DB import Base_De_Datos
from modules.database.objects_DB import Usuario
from modules.database.campos_DB import (
    Nombres_Tablas,
)

RUTA = CARPETA_RAIZ + "/data/database.db"
ESCRITOR_DB = Base_De_Datos(
    RUTA, Nombres_Tablas.USUARIOS, Nombres_Tablas.CONTACTOS, Nombres_Tablas.OCUPACIONES
)

banner = r"""
     ________                    __         
    / ____/ /_  ____ _____ ___  / /_  ____ _
   / /   / __ \/ __ `/ __ `__ \/ __ \/ __ `/
  / /___/ / / / /_/ / / / / / / /_/ / /_/ / 
  \____/_/ /_/\__,___/ /_/ __/_.___/\__,_/  
               \ \/ /___ _/ /               
                \  / __ `/ /                
                / / /_/ /_/                 
               /_/\__,_(_)                  
                                           
"""
telefono_usuario = None
contrasena_usuario = None


def login_page(screen) -> Tuple[int, str]:
    telefono = None
    contrasena = None
    telefono_valido = False
    continuar_verificacion = True
    while continuar_verificacion == True:
        screen.clear()
        telefono = textbox_builder(screen, 50, 10, "INGRESA TU TELEFONO", "ENTER")
        telefono_valido = es_telefono_valido(telefono)
        screen.clear()
        contrasena = textbox_builder(screen, 50, 10, "INGRESA TU CONTRASENA", "ENTER")
        existe_usuario = ESCRITOR_DB.validar_usuario(telefono, contrasena)

        if existe_usuario == False or telefono_valido == False:
            alert_message(
                screen,
                50,
                5,
                "ATENCION",
                "No existe ningun usuario con ese telefono y contrasena",
                "ENTER",
            )
            continuar_verificacion = confirmation_box(
                screen, "¿Quieres seguir intentando?"
            )
        else:
            return (telefono, contrasena)
    return (None, None)

def signup_page(screen):
    nombre = None
    apellido = None
    telefono = None
    contrasena = None
    genero = None
    edad = None
    continuar_registro = True
    hay_campos_invalidos = False
    while continuar_registro == True:
        telefono = textbox_builder(screen, 50, 10, "¿Cual es tu telefono?", "ENTER")
        contrasena = textbox_builder(screen, 50, 10, "¿Cual es tu contrasena?", "ENTER")
        nombre = textbox_builder(screen, 50, 10, "¿Cual es tu nombre?", "ENTER")
        apellido = textbox_builder(
            screen, 50, 10, "¿Cuales son tus apellidos?", "ENTER"
        )
        edad = textbox_builder(screen, 50, 10, "¿Cual es tu edad?", "ENTER")
        genero = menu_builder(
            screen,
            50,
            "¿Cual es tu genero?",
            ["Hombre", "Mujer"],
            "Presionar <Enter> para confirmar.",
        )
        genero = 0 if genero == "Hombre" else 1

        if es_telefono_valido(telefono) == False:
            hay_campos_invalidos = True
        if edad.isnumeric() == False:
            hay_campos_invalidos = True

        if hay_campos_invalidos == True:
            alert_message(
                screen,
                50,
                5,
                "ATENCION",
                "Algunos campos que ingresaste no son validos...",
                "ENTER",
            )
            continuar_registro = confirmation_box(screen, "¿Quieres seguir intentando?")
        if hay_campos_invalidos == False:
            usuario = Usuario(
                telefono, contrasena, genero, edad, nombre, apellido, True, True
            )
            if ESCRITOR_DB.registrar_usuario(usuario) == False:
                alert_message(
                    screen,
                    50,
                    5,
                    "ATENCION",
                    "Parece que ya existe un usuario con ese telefono...",
                    "ENTER",
                )
                continuar_registro = confirmation_box(
                    screen, "¿Quieres volver a intentar?"
                )
            else:
                alert_message(
                    screen,
                    50,
                    5,
                    "EXITOS!",
                    "Tu usuario a sido registrado con exito, disfruta!",
                    "ENTER",
                )
                break

def main_page(screen, usuario: Usuario):
    while True:
        option = menu_builder(
            screen,
            50,
            "¿Que quieres hacer?",
            ["Buscar Trabajador", "Ver mi perfil"],
            "Presiona <Enter> para continuar.",
            ["Salir"]
        )
        if option == "Buscar Trabajador":
            search_page(screen, usuario.TELEFONO, usuario.CONTRASENA)
        elif option == "Ver mi perfil":
            user_page(screen, usuario)
        elif option == "Salir":
            break

def user_page(screen, usuario: Usuario):
    while True:
        option = menu_builder(
            screen,
            50,
            "MI PERFIL",
            [
                "Ver mis datos",
                "Agregar contacto",
                "Eliminar contacto",
                "Agregar ocupacion",
                "Eliminar ocupacion",
            ],
            "Presionar <Enter> para continuar.",
            ["Regresar"],
        )
        if option == "Ver mis datos":
            usuario = ESCRITOR_DB.obtener_usuario(usuario.TELEFONO, usuario.CONTRASENA)
            alert_message(screen, 50, 30, "MI PERFIL", usuario.user_as_str(), "ENTER")
        elif option == "Agregar contacto":
            telefono_contacto = textbox_builder(
                screen, 50, 10, "Ingresa el telefono de tu conocido:", "Enter"
            )
            
            if (
                es_telefono_valido(telefono_contacto) == False
                or ESCRITOR_DB.existe_contacto(usuario.TELEFONO, telefono_contacto) == True
                or ESCRITOR_DB.existe_usuario(telefono_contacto) == False
            ):
                alert_message(
                    screen,
                    50,
                    8,
                    "ATENCION",
                    "Parece que el telefono ingresado no es valido o ya esta en tu lista de contactos. Recuerda que solo puedes anadir telefonos de personas que esten registradas en la app",
                    "ENTER",
                )
            else:
                ESCRITOR_DB.agregar_contacto(usuario, telefono_contacto)
                alert_message(
                    screen,
                    50,
                    5,
                    "EXITO",
                    "Tu contacto fue agregado con exito",
                    "ENTER",
                )

        elif option == "Eliminar contacto":
            telefono_contacto = textbox_builder(
                screen, 50, 10, "Ingresa el telefono de tu conocido:", "Enter"
            )
            if (
                es_telefono_valido(telefono_contacto) == False
                or ESCRITOR_DB.existe_contacto(usuario.TELEFONO, telefono_contacto)
                == False
            ):
                alert_message(
                    screen,
                    50,
                    5,
                    "ATENCION",
                    "Parece que el telefono ingresado no es valido, o no esta en tu lista de contactos",
                    "ENTER",
                )
            else:
                ESCRITOR_DB.eliminar_contacto(usuario.TELEFONO, telefono_contacto)
                alert_message(
                    screen,
                    50,
                    5,
                    "EXITO",
                    "Tu contacto ha sido removido con exito",
                    "ENTER",
                )
        elif option == "Agregar ocupacion":
            ocupacion = textbox_builder(
                screen, 50, 10, "Ingresa tu nuevo ocupacion:", "Enter"
            )
            
            if ESCRITOR_DB.existe_ocupacion(usuario.TELEFONO, ocupacion) == True:
                alert_message(
                    screen,
                    50,
                    8,
                    "ATENCION",
                    "Parece que la ocupacion que ingresaste ya existe",
                    "ENTER",
                )
            else:
                ESCRITOR_DB.agregar_ocupacion(usuario, ocupacion)
                alert_message(
                    screen,
                    50,
                    5,
                    "EXITO",
                    "Tu ocupacion fue agregada con exito",
                    "ENTER",
                )

        elif option == "Eliminar ocupacion":
            ocupacion = textbox_builder(
                screen, 50, 10, "Ingresa la ocupacion a eliminar:", "Enter"
            )
            
            if ESCRITOR_DB.existe_ocupacion(usuario.TELEFONO, ocupacion) == False:
                alert_message(
                    screen,
                    50,
                    8,
                    "ATENCION",
                    "Parece que la ocupacion que ingresaste no existe.",
                    "ENTER",
                )
            else:
                ESCRITOR_DB.eliminar_ocupacion(usuario.TELEFONO, ocupacion)
                alert_message(
                    screen,
                    50,
                    5,
                    "EXITO",
                    "Tu ocupacion fue eliminada con exito.",
                    "ENTER",
                )
        elif option == "Regresar":
            break

def search_page(screen, telefono, contrasena):
    value = textbox_builder(screen, 50, 10, "Buscador de trabajadores", "Ingresa una palabra clave")
    usuario = ESCRITOR_DB.obtener_usuario(telefono, contrasena)
    coincidencias = ESCRITOR_DB.busqueda_recursiva_por_ocupacion(usuario, value)

    alert_message(screen, 50, 20, "RESULTADOS", "Segun tus contactos, estos numeros podrian interesarte:\n\n" + "".join(coincidencias), "ENTER")

def main(screen: curses.window):
    # MAIN SETTINGS
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    print_centered(screen, banner, optional_message="Presionar cualquier tecla")
    screen.getch()

    # MAIN FLOW
    while True:
        screen.clear()
        screen.refresh()
        selected_option = menu_builder(
            screen,
            40,
            "BIENVENIDO",
            ["Ingresar", "Registrarme", "Sobre nosotros", "Ver tablas"],
            "Presionar <Enter> para confirmar",
            default_options=["Salir"],
        )
        screen.clear()

        if selected_option == "Ingresar":
            telefono_usuario, contrasena_usuario = login_page(screen)
            if telefono_usuario is not None or contrasena_usuario is not None:
                usuario = ESCRITOR_DB.obtener_usuario(telefono_usuario, contrasena_usuario)
                main_page(screen, usuario)

        elif selected_option == "Registrarme":
            signup_page(screen)
        elif selected_option == "Sobre nosotros":
            alert_message(
                screen,
                60,
                20,
                "SOBRE NOSOTROS",
                r"""
Hola! somos Chamba Ya! un programa para buscar y dar trabajo, cualquiera puede registrarse! aunque no disponga de un diploma academico, basta con ser bueno en tu oficio...
                
La aplicacion funciona recomendandote trabajadores, basado en la lista de contactos de tus conocidos.
                
Disfruta!


    Atentamente,
    El equipo de ChambaYa!""",
                "ENTER",
            )
        elif selected_option == "Ver tablas":
            screen.clear()
            screen.addstr(ESCRITOR_DB.obtener_dataframes_str())
            screen.addstr("\n\nPresionar cualquier tecla para continuar...")
            screen.refresh()
            screen.getch()
        elif selected_option == "Salir":
            break


curses.wrapper(main)
