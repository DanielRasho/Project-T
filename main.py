import setup
from modules.interface.menus import menu_builder, clean_screen
import validators;

accion =  menu_builder('Bienvenido a Proyecto T',
            ['Ingresar', 'Registrarse'],
            '',
            return_value= True, default_options=['Salir',])
            
if accion == 'Ingresar': 
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

elif accion == 'Registrarse':
    new_usuario_telefono=input('Ingrese su número de teléfono\n')
    #Agregar función de validación de datos (only numbers)
    contraseña_nuevo_usuario= input('Ingrese su contraseña\n')
    #Función que agregue esos datos al csv

elif accion == "Salir":
    exit()
    