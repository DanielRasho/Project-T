from os import path
import database.users
import csv

# parentDir = path.dirname(path.realpath(__file__))
# print(parentDir)
# dataDir = parentDir + "/../data/users.csv"
# print(dataDir)

with open('./data/users.csv', 'w') as uwu:
    writer = csv.writer(['nombre', 'olamundo', 'adios'])
#print(dataDir)
#database.users.actualizar_campos(dataDir)