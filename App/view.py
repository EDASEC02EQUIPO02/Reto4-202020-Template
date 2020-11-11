"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
from DISClib.ADT import list as lt
import timeit
from DISClib.ADT.graph import gr
from time import process_time
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de buses de singapur")
    print("3- Calcular componentes conectados")
    print("4- Establecer estación base:")
    print("5- Hay camino entre estacion base y estación: ")
    print("6- Ruta de costo mínimo desde la estación base y estación: ")
    print("7- Estación que sirve a mas rutas: ")
    print("0- Salir")
    print("*******************************************")


recursionLimit = 10000
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()
    elif int(inputs[0]) == 2:
        t1 = process_time()
        print("\nCargando información de CitiBike ....")
        controller.loadTrips(cont)
        numedges = controller.totalConnections(cont)
        numvertex = controller.totalStops(cont)
        print('Numero de vertices: ' + str(numvertex))
        print('Numero de arcos: ' + str(numedges))
        #print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
        sys.setrecursionlimit(recursionLimit)
        print('La cantidad total de viajes es de: ' + str(lt.size(cont['lsttrips'])))
        #print('El limite de recursion se ajusta a: ' + str(recursionLimit))
        t2 = process_time()
        print("El tiempo de procesamiento es de: ", t2 - t1)
    elif int(inputs[0]) == 3:
        t1 = process_time()
        scc = controller.connectedComponents(cont)
        origin = input("Ingrese el ID de la estación de origen: ")
        dest = input("Ingrese el ID de la estación de destino: ")
        print('El número de componentes conectados es: ' + str(scc))
        resp = controller.sameCC(cont, origin, dest)
        if resp == False:
            print("No están fuertemente conectados")
        else: 
            print("Están fuertemente conectados")
        t2 = process_time()
        print("El tiempo de procesamiento es de: ", t2 - t1)
    else:
        sys.exit(0)
sys.exit(0)

