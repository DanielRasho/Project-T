from ast import Return
import config.setup
from modules.interface.menus import menu_builder, clean_screen
from modules.interface.menus import datosANDvalidacion_numeros

accion =  menu_builder('Bienvenido a Proyecto T',
            ['Ingresar', 'Registrarse'],
            '',
            return_value= True, default_options=['Salir',])
            
if accion == 'Ingresar': 
    usuario=datosANDvalidacion_numeros()
    contraseña=input('Ingrese su contraseña\n')
    #Parametros:usuario, contraseña
    #Return: True or false (logico), dependiendo 
    #Funcion para verificar si el número telefonico coincide con la contraseña. Si coinciden devulve un True, sino un False
    verifacion=True #aquí se va a llamar a la función
    if verifacion==True:
        seccion=menu_builder('Menus',
            ['Buscar', 'Recomendados', 'Agregar'],
            '',
            return_value= False, default_options=['Salir',])
        if seccion==0:
            busqueda=input('¿Qué estás buscando?\n') 
            #Parametros: busqueda
            #Return: lista (lista_trabajadores)
            #Funcion que agrupe todos los trabajadores que le puedan servir al usuario y los guarde en la lista "listado_trabajadores"
            """trabajador_elegido=menu_builder('Tal vez uno de ellos podría ayudarte',
                [listado_trabajadores],
                '',
                return_value= False, default_options=['Salir',])
            print(trabajador_elegido)    ##Aquí no sé cómo le vamos a hacer, pero hay que mostrar los datos del trabajador que escogió
            accion_con_trabajador=menu_builder('¿Quieres consultar con esta persona?',
            ['Llamar', 'Mensaje'],
            '',
            return_value= False, default_options=['Salir',])"""
        
        if seccion==1: 
            #Parametros: (ninguno) 
            #Return: una lista (listado_recomendados)
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
            nuevo_telefono=datosANDvalidacion_numeros()
            nueva_labor=input('Ingrese la labor del trabajador\n')
            #Parametros: nuevo_nombre, nuevo_telefono, nueva_labor
            #Return: (nada)
            #Funcion que agregue estos datos al CSV
            print("Se ha agregado a su lista")
        if seccion==3:
            exit()

elif accion == 'Registrarse':
    new_usuario_telefono=usuario=datosANDvalidacion_numeros()
    contraseña_nuevo_usuario= input('Ingrese su contraseña\n')
    confirmacion=input('Ingrese nuevamente su contraseña\n')
    if contraseña_nuevo_usuario==confirmacion:
        iguales=True
    else:
        iguales=False
    while iguales==False:
        print ("Las contraseñas no coinciden")
        contraseña_nuevo_usuario= input('Ingrese su contraseña\n')
        confirmacion=input('Ingrese nuevamente su contraseña\n')
        if contraseña_nuevo_usuario==confirmacion:
            print('Te has registrado correctamente')
            break
        

    #Parametros: new_usuario_telefono, contraseña_nuevo_usuario
    #Return: (nada)
    #Función que agregue esos datos al csv

elif accion == "Salir":
    exit()
    