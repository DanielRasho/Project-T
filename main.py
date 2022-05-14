from ast import Return
import config.setup
from modules.interface.menus import menu_builder
from modules.interface.menus import datosANDvalidacion_numeros
from modules.database.users import Base_de_datos


accion =  menu_builder('Bienvenido a Proyecto T',
            ['Ingresar', 'Registrarse'],
            '',
            return_value= True, default_options=['Salir',])

Base_de_datos = Base_de_datos("data/users.csv")

while accion == 'Ingresar': 
    usuario=datosANDvalidacion_numeros()
    contraseña=input('Ingrese su contraseña\n')
    verifacion=Base_de_datos.validar_usuario(usuario,contraseña) #aquí se está usando una función nueva
    verifacion=True
    while verifacion==False:
        accionDos=menu_builder('Los datos no coinciden',
                    ['Intentarlo de nuevo', 'Registrarse'],
                    '',
            return_value= False, default_options=['Salir',])
        if accionDos==0:
            usuario=datosANDvalidacion_numeros()
            contraseña=input('Ingrese su contraseña\n')
            #Base_de_datos = Base_de_datos("data/users.csv")
            verifacion=Base_de_datos.validar_usuario(usuario,contraseña)
        if accionDos==1:
            break
        if accionDos==2:
            exit()
    
    if verifacion==True:
        seccion=menu_builder('Menus',
            ['Buscar', 'Recomendados', 'Agregar'],
            '',
            return_value= False, default_options=['Salir',])
        if seccion==0:
            busqueda=input('¿Qué estás buscando?\n') 
            busqueda=busqueda.lower()
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
    
        
        

if accion == 'Registrarse':
    new_usuario_telefono=usuario=datosANDvalidacion_numeros()
    genero_usuario= menu_builder('Ingrese su género ',
            ['Hombre'],
            '',
            return_value= True, default_options=['Mujer'])
    edad_usuario=int(input('Ingrese su edad\n'))
    nombre_usuario=input('Ingrese su nombre\n')
    apellido_usario=input('Ingrese su apellido\n')
    temporal=True
    etiquetas=[]
    while temporal:
        etiqueta=input('Ingrese etiqueta\n')
        etiqueta=etiqueta.lower()
        etiquetas.append(etiqueta)
        seguir= menu_builder('¿Hay otra etiqueta?',
            ['Sí'],
            '',
            return_value= False, default_options=['No'])
        if seguir == 0:
            temporal=True
        else: 
            temporal=False
    etiquetas = ",".join(etiquetas)
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
    Base_de_datos.crear_usuario(
        new_usuario_telefono,
        contraseña_nuevo_usuario,
        genero_usuario,
        edad_usuario,
        nombre_usuario,
        apellido_usario,
        etiquetas)
    #Parametros: new_usuario_telefono, contraseña_nuevo_usuario
    #Return: (nada)
    #Función que agregue esos datos al csv

elif accion == "Salir":
    exit()
    