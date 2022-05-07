import pandas as pd 
import numpy as np 

##Funcion para agregar numeros a la lista 
def agregar_numeros_a_listas():

    lista_mumeros_de_telefonos = [] ##Lista vacia de numeros

    numeros = input("Agregue sus numeros: ")## Variable que alamcena los numeros para despues agregarlos a la lista

    lista_mumeros_de_telefonos.append(numeros)## Agregar la variable que contiene los numeros a la lista

    seguir_agregando_numeros = input("Quiere agregar otro numero? Si(1) No(2)\n") ##Opcion si desea agregar numeros

    while True():
        if seguir_agregando_numeros == "1": ## Si decide agregar mas numeros sale lo siguiente
            [] = input("Agregue el numero : ")
            lista_mumeros_de_telefonos.append([])
            break
        elif seguir_agregando_numeros == "2": ## No se agregan mas numeros
            break
        else: 
            seguir_agregando_numeros = input("Seleccione una opcion valida por favor: Si(1) No(2)") ## Para que seleecioe una opcion valida




    list_rows = [ ['ID', 'Numero de telefonos'],['1', lista_mumeros_de_telefonos] ] ## Agrega la lista de numeros previamente escritos por el usuario.
    np.savetxt("ArchivoCSV.csv", list_rows, delimiter ="|",fmt ='% s') 

