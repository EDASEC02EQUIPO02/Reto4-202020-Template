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

import config as cf
from App import model
import csv
from DISClib.Algorithms.Graphs import scc
import os
from time import process_time

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(citibike):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadFile(citibike, filename)
    return citibike


def loadFile(citibike, tripfile):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(citibike, trip)
        model.addStationI(citibike, trip)
        model.addStationF(citibike, trip)
        model.addNamesLocations(citibike, trip)
    return citibike

# ___________________________________________________
#  Funciones para los requerimientos:
# ___________________________________________________
def requerimiento_3(citibike):
    return model.requerimiento_3(citibike)

def req4(analyzer, TiempoResistencia, IdEstacionI):
    tiempoSegundos=int(TiempoResistencia)*60
    rutas = model.req4(analyzer, tiempoSegundos, IdEstacionI)
    return rutas

def Repeticiones(cont, rangoi, rangof):
    return model.Repeticiones(cont, rangoi, rangof)

def requerimiento_6(cont, latitudI, longitudI, latitudF, longitudF):
    return model.requerimiento_6(cont, latitudI, longitudI, latitudF, longitudF)



















# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)


def sameCC(sc, station1, station2):
    return model.IsItConnected(sc, station1, station2)


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    return model.minimumCostPaths(analyzer, initialStation)


def hasPath(analyzer, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    return model.hasPath(analyzer, destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    return model.minimumCostPath(analyzer, destStation)


def servedRoutes(analyzer):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    maxvert, maxdeg = model.servedRoutes(analyzer)
    return maxvert, maxdeg
