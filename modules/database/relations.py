import pandas as pd 
import numpy as np 

def aniadir_un_contacto(): ##Funcion para agregar un usario a la lista de contactos
    numeros_de_telefono=[ ] ##Lista vacia donde se guardaran los numeros de los contactos que ingrese el usuario
    usuario = 1 

    nuevos_contactos = [input("Agrega los numeros separados por comas ",": \n")] ##Pide al usuario los numeros que desea agregar a la lista

    numeros_de_telefono.append(nuevos_contactos) ##Se agregan los numeros escritos a la lista

    print("Lista nueva de contactos es la siguiente: ",numeros_de_telefono) ##Muestra el valor de la "nueva lista" o lista actualizada

    df = pd.DataFrame({'ID' : [usuario], 'Numero de telefono de sus contactos' : [numeros_de_telefono] }) ##Tabla de "Excel" mostrando como columna 1 el ID del usuario y columna 2 los numeros de telefonos de los contctos 
    df.head()

def eliminar_un_contacto():

    ##Para esta funcion en teoria creo que ya deberia de estar la lista primero y no volverlos a pedir pero no se 

    numeros_de_telefono=[ ] ##Lista vacia donde se guardaran los numeros de los contactos que ingrese el usuario
    usuario = 1 ##ayuda con esto no se que hacerle 

    nuevos_contactos = input("Agrega los numeros separados por comas: \n") ##Pide al usuario los numeros que desea agregar a la lista

    numeros_de_telefono.append(nuevos_contactos) ##Se agregan los numeros escritos a la lista

    print("Lista nueva de contactos es la siguiente: ",numeros_de_telefono) ##Muestra el valor de la "nueva lista" o lista actualizada

    print(numeros_de_telefono)
##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##
    ##Realmente creo que esta seria la funcion que elimina el numero(contacto) que escriba el usuario
    ##Tambien no se como hacer para que automaticamente se separen por comas en las listas, por ahora solo funciona pidiendole al usuario que esriba los numeros telefonicos separandolos por comas

    numero_telefonicos = input("Ingrese los numero telefonicos: ") ##Ingrese los numero telefonicos para que se guarden en una lista

    lista_numeros_telefonicos = numero_telefonicos.split(',') ##Convierte el tipo texto(cadena) en una lista

    print("Lista nueva: ",lista_numeros_telefonicos) ##Solo muestra la lista con los numero que ingreso el usuario

    numeros_eliminados = input("Ingrese el numero que quiere eliminar de la lista: ") ## Le pregunta al usuario que numero quiere eliminar y lo guarda en una variable

    for x in lista_numeros_telefonicos: ##ciclo for para que busque en toda la lista el valor que tiene que eliminar
        if x == numeros_eliminados: ##Si coincide exactamente con el que quiere eliminar lo elimina
            lista_numeros_telefonicos.remove(x) ##Leer arriba
        
    print(lista_numeros_telefonicos) ##Muestra la lista actualizada
