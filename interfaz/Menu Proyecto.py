from email.policy import default
from operator import truediv
from re import T
from readchar import readkey, key  
from os import system       
import validators;

#Verificar que el valor sea cadena y tenga un carácter como mínimo
def validate_string(value):
    if not validators.length(value, min=1):
        return False;
    return True;

#Verificar que el valor sea de tipo entero y sea 0 como mínimo
def validate_int(value):
    if not validators.between(value, min=0):
        return False;   
    return True;        


def menu_builder(header: str, options: list, footer: str, return_value = False, default_options = []):
    cursor_position = 0
    options += default_options

    while True:
        
        clean_screen()
        print(f"{header}\n")
        for index, option in enumerate(options):
            if index == cursor_position:
                print(f"\t>> {option}")
            else:
                print(f"\t   {option}")
        print(f"\n{footer}")

        
        new_cursor_position = readkey()
        if new_cursor_position == key.UP:         
            cursor_position -= 1
            cursor_position %= len(options)
        elif new_cursor_position == key.DOWN:     
            cursor_position += 1
            cursor_position %= len(options)
        elif new_cursor_position == key.ENTER:   
            if return_value is True: return options[cursor_position]
            else: return cursor_position

   
def clean_screen():
    system("cls")


accion =  menu_builder('Bienvenido a Proyecto T',
            ['Ingresar', 'Registrarse'],
            '',
            return_value= False, default_options=['Salir',])
            

if accion == 0: 
    usuario=input('Ingrese su número de teléfono\n')
    #Agregar función de validación de datos (only numbers)
    contraseña=input('Ingrese su contraseña\n')
    #Funcion para verificar si el número telefonico coincide con la contraseña. Si coinciden devulve un True, sino un False
    verifacion=True #aquí se va a llamar a la función
    if verifacion==True:
        seccion=menu_builder('Menus',
            ['Buscar', 'Recomendados', 'Agregar'],
            '',
            return_value= False, default_options=['Salir',])
        if seccion==0:
            busqueda=input('¿Qué estás buscando?\n') #Agregar función de validación de datos (only letters)
            """Funcion que agrupe todos los trabajadores que le puedan servir al usuario y los guarde en la lista "listado_trabajadores"
            trabajador_elegido=menu_builder('Tal vez uno de ellos podría ayudarte',
                [listado_trabajadores],
                '',
                return_value= False, default_options=['Salir',])
            print(trabajador_elegido)    ##Aquí no sé cómo le vamos a hacer, pero hay que mostrar los datos del trabajador que escogió
            accion_con_trabajador=menu_builder('¿Quieres consultar con esta persona?',
            ['Llamar', 'Mensaje'],
            '',
            return_value= False, default_options=['Salir',])"""
        
        if seccion==1:
            #Funcion que recopile los primeros 5 en el listado de trabajadores y los almacene en la lista "listado_recomendados"
            """trabajador_recomendado=menu_builder('Te recomendamos',
                [listado_recomendados],
                '',
                return_value= False, default_options=['Salir',])
            print(trabajador_recomendado)    ##Aquí no sé cómo le vamos a hacer, pero hay que mostrar los datos del trabajador que escogió
            accion_con_trabajador=menu_builder('¿Quieres consultar con esta persona?',
            ['Llamar', 'Mensaje'],
            '',
            return_value= False, default_options=['Salir',])"""
        if seccion==2:
            nuevo_nombre=input('Ingrese el nombre del trabajador\n')
            nuevo_telefono=int(input('Ingrese el telefono del trabajador\n'))#validar que solo sean numeros
            nuevo_labor=input('Ingrese la labor del trabajador\n')
            #Funcion que agregue estos datos al CSV
            print("Se ha agregado a su lista")
        if seccion==3:
            print("salir")



elif accion == 1:
    new_usuario=input('Ingrese su número de teléfono\n')
    #Agregar función de validación de datos (only numbers)
    contraseña_nuevoUs=t ('Ingrese su contraseña\n')
    #Función que agregue esos datos al csv

elif accion == 2:
    print('salir')
    