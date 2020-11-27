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
from App import model
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
    print("2- Cargar información de bicicletas de NY")
    print("3- Requerimiento #1")
    print("4- Requerimiento #2")
    print("5- Requerimiento #3")
    print("6- Requerimiento #4")
    print("7- Requerimiento #5")
    print("8- Requerimiento #6")
    print("9- Requerimiento #7")
    print("10- Requerimiento #8")
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
    
    elif int(inputs[0]) == 4:
        t1 = process_time()
        tiempoinicial = input("Ingrese el rango minimo de tiempo en minutos: ")
        tiempofinal = input("Ingrese el rango maximo de tiempo en minutos: ")
        estacion = input("Ingrese el ID de la estacion inicial: ")
        rutas= controller.req2(cont, tiempoinicial, tiempofinal, estacion)
        print(rutas)
        print(len(rutas))      
        t2 = process_time()
        print("El tiempo de procesamiento es de: ", t2 - t1)

    elif int(inputs[0]) == 5:
        t1 = process_time()
        resp = controller.requerimiento_3(cont)
        t2 = process_time()
        print("El tiempo de procesamiento es de: ", t2 - t1)

    elif int(inputs[0]) == 6:
        t1 = process_time()
        TiempoResistencia = input("Tiempo máximo de resistencia en minutos: ")
        IdEstacionI = input("ID de la estación inicial: ")
        rutas=controller.req4(cont, TiempoResistencia, IdEstacionI)
        print(rutas)
        print(len(rutas))
        t2 = process_time()
        print("El tiempo de procesamiento es de: ", t2 - t1)

    elif int(inputs[0]) == 7:
        t1 = process_time()
        print("Ingrese un rango de fechas: (EJ: 0-10, 11-20, 21-30, ...)")
        rangoi = int(input("Ingrese el mínimo de edad: "))
        rangof = int(input("Ingrese el máximo de edad: "))
        controller.Repeticiones(cont, rangoi, rangof)
        t2 = process_time()
        print("El tiempo de procesamiento es de: ", t2 - t1)
    elif int(inputs[0]) == 8:
        t1 = process_time()
        #latitudI = float(input("Ingrese la latitud en la que se encuentra: "))
        #longitudI = float(input("Ingrese la longitud en la que se encuentra: "))
        #latitudF = float(input("Ingrese la latitud del sitio de interes turistico: "))
        #longitudF =float(input("Ingrese la longitud del sitio de interes turistico: "))
        controller.requerimiento_6(cont, 40.76727216, -73.99392888, 40.71754834, -74.01322069)
        t2 = process_time()
        print("El tiempo de procesamiento es de: ", t2 - t1)
    elif int(inputs[0]) == 9:
        RangoEdad = input("Ingrese un rango de edad (Ej: 0-10, 11-20, 21-30...): ")
        parEstaciones = controller.requerimiento_7(cont, RangoEdad)
        print(parEstaciones)
    elif int(inputs[0]) == 10:
        IDBicicleta = input("Ingrese el ID de la bicicleta: ")
        Fecha = input("Ingrese la fecha (DD-MM-AAAA): ")
        rutaBicicleta = controller.requerimiento_8(cont, IDBicicleta, Fecha)
        print(rutaBicicleta)
    

    else:
        sys.exit(0)
sys.exit(0)

#40.76727216
#-73.99392888
#40.71754834
#-74.01322069