import curses

from sqlalchemy import true
from modules.interface.menus import *
from typing import Tuple
from curses.textpad import rectangle
from config.definitions import CARPETA_RAIZ
from modules.database.lector_DB import Base_De_Datos, Lector_BD, Telefono
from modules.database.objects_DB import Usuario
from modules.database.campos_DB import (
    Campos_Usuario,
    Campos_Ocupacion,
    Campos_Contactos,
    Nombres_Tablas,
)

RUTA = CARPETA_RAIZ + "/data/database.db"
ESCRITOR_DB = Base_De_Datos(
    RUTA, Nombres_Tablas.USUARIOS, Nombres_Tablas.CONTACTOS, Nombres_Tablas.OCUPACIONES
)
ESCRITOR_DB.limpiar_tablas()

banner = r"""
 _______                                                           __           
/       \                                                         /  |          
$$$$$$$  | __    __   _______   _______   ______   _______    ____$$ |  ______  
$$ |__$$ |/  |  /  | /       | /       | /      \ /       \  /    $$ | /      \ 
$$    $$< $$ |  $$ |/$$$$$$$/ /$$$$$$$/  $$$$$$  |$$$$$$$  |/$$$$$$$ |/$$$$$$  |
$$$$$$$  |$$ |  $$ |$$      \ $$ |       /    $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |
$$ |__$$ |$$ \__$$ | $$$$$$  |$$ \_____ /$$$$$$$ |$$ |  $$ |$$ \__$$ |$$ \__$$ |
$$    $$/ $$    $$/ /     $$/ $$       |$$    $$ |$$ |  $$ |$$    $$ |$$    $$/ 
$$$$$$$/   $$$$$$/  $$$$$$$/   $$$$$$$/  $$$$$$$/ $$/   $$/  $$$$$$$/  $$$$$$/  
                                                                                
         ______   __                                __                    
        /      \ /  |                              /  |                  
        /$$$$$$  |$$ |____    ______   _____  ____  $$ |____    ______     
        $$ |  $$/ $$      \  /      \ /     \/    \ $$      \  /      \   
        $$ |      $$$$$$$  | $$$$$$  |$$$$$$ $$$$  |$$$$$$$  | $$$$$$  |    
        $$ |   __ $$ |  $$ | /    $$ |$$ | $$ | $$ |$$ |  $$ | /    $$ |  
        $$ \__/  |$$ |  $$ |/$$$$$$$ |$$ | $$ | $$ |$$ |__$$ |/$$$$$$$ |        
        $$    $$/ $$ |  $$ |$$    $$ |$$ | $$ | $$ |$$    $$/ $$    $$ |        
         $$$$$$/  $$/   $$/  $$$$$$$/ $$/  $$/  $$/ $$$$$$$/   $$$$$$$/         
                                               
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
        existe_usuario = ESCRITOR_DB.validar_usuario(int(telefono), contrasena)

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
            return (int(telefono), contrasena)


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


def main_page(screen, usuario: Usuario):
    option = menu_builder(
        screen,
        50,
        "¿Que quieres hacer?",
        ["Buscar Trabajador", "Ver mi perfil"],
        "Presiona <Enter> para continuar.",
    )
    if option == "Buscar Trabajador":
        pass
    elif option == "Ver mi perfil":
        user_page(screen, usuario)


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
            pass
        elif option == "Agregar contacto":
            telefono_contacto = textbox_builder(
                screen, 50, 10, "Ingresa el telefono de tu conocido:", "Enter"
            )
            if (
                es_telefono_valido(telefono_contacto) == False
                or ESCRITOR_DB.existe_contacto(usuario.TELEFONO, telefono_contacto)
                == True
            ):
                alert_message(
                    screen,
                    50,
                    5,
                    "ATENCION",
                    "Parece que el telefono ingresado no es valido, o ya esta en tu lista de contactos",
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
            pass
        elif option == "Agregar ocupacion":
            pass
        elif option == "Eliminar ocupacion":
            pass
        elif option == "Salir":
            break


def search_page(screen):
    pass


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
            ["Ingresar", "Registrarme", "Sobre nosotros", "Estadisticas"],
            "Presionar <Enter> para confirmar",
            default_options=["Salir"],
        )
        screen.clear()

        if selected_option == "Ingresar":
            telefono_usuario, contrasena_usuario = login_page(screen)
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
Hola! somos Chamba Ya! un programa para buscar trabajo, y dar trabajo, especialmente para trabajos mas practicos como la carpinterias o amas de cosas...
                
La aplicacion recomienda trabajadores basado en tus conocidos, y los conocidos de tus conocidos!
                
Disfruta!


    Atentamente,
    El equipo de ChambaYa!""",
                "ENTER",
            )
        elif selected_option == "Estadisticas":
            pass
        elif selected_option == "Salir":
            break


curses.wrapper(main)
