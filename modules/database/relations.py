import pandas as pd 

def aniadir_un_contacto(): 
    # PARAMETROS: Numero telefonico
    # RETURNA: int (lista) 
    # FUNCIONALIDAD: Crear una lista para guardar los numeros de los contactos del usuario
    # Agregue el numero que el usurio indique a una lista.

    numeros_de_telefono=[ ]
    usuario = 1 

    nuevos_contactos = [input("Agrega los numeros separados por comas ",": \n")] 

    numeros_de_telefono.append(nuevos_contactos) 

    print("Lista nueva de contactos es la siguiente: ",numeros_de_telefono) 

    df = pd.DataFrame({'ID' : [usuario], 'Numero de telefono de sus contactos' : [numeros_de_telefono] }) 
    df.head()

def eliminar_un_contacto():

    # PARAMETROS: Numero telefonico
    # RETORNA: Int(lista)
    # FUNCIONALIDAD: Elimina el numero del contacto que ingrese el usuario
    # OJITO AL DATO: Para esta funcion en teoria creo que ya deberia de estar la lista primero 
    # Y no volverlos a pedir pero no se 
    #

    numeros_de_telefono=[ ] 

    nuevos_contactos = input("Agrega los numeros separados por comas: \n") 

    numeros_de_telefono.append(nuevos_contactos)

    print("Lista nueva de contactos es la siguiente: ",numeros_de_telefono)

    print(numeros_de_telefono)
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##Realmente creo que esta seria la funcion que elimina el numero(contacto) que escriba el usuario
    ##Tambien no se como hacer para que automaticamente se separen por comas en las listas, por ahora solo funciona pidiendole al usuario que esriba los numeros telefonicos separandolos por comas

    numero_telefonicos = input("Ingrese los numero telefonicos: ") 

    lista_numeros_telefonicos = numero_telefonicos.split(',')

    print("Lista nueva: ",lista_numeros_telefonicos) 

    numeros_eliminados = input("Ingrese el numero que quiere eliminar de la lista: ")

    for x in lista_numeros_telefonicos:
        if x == numeros_eliminados: 
            lista_numeros_telefonicos.remove(x)
        
    print(lista_numeros_telefonicos)
