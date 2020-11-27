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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as en
from DISClib.DataStructures import graphstructure as grh
from DISClib.DataStructures import mapstructure as mp
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import shellsort as ls
from math import radians, cos, sin, asin, sqrt, atan2
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------


def newAnalyzer():
    try:
        citibike = {
                    'graph': None,
                    'lsttrips': None,
                    'divide': None,
                    'grafo': None,
                    'StationI': None,
                    'StationF': None}

        citibike['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                  directed=True,
                                  size=1000,
                                  comparefunction=compareStations)
        citibike['lsttrips'] = lt.newList('SINGLE_LINKED', compareStations)
        citibike['divide'] = {}
        citibike['grafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                  directed=True,
                                  size=1000,
                                  comparefunction=compareStations)
        citibike['StationI'] = mp.newMap( numelements=300317,
                                                    prime=109345121,   
                                                    maptype='CHAINING', 
                                                    loadfactor=1.0, 
                                                    comparefunction=comparer)
        citibike['StationF'] = mp.newMap( numelements=300317,
                                                    prime=109345121,   
                                                    maptype='CHAINING', 
                                                    loadfactor=1.0, 
                                                    comparefunction=comparer)
        citibike['namesI'] = mp.newMap( numelements=300317,
                                                    prime=109345121,   
                                                    maptype='CHAINING', 
                                                    loadfactor=1.0, 
                                                    comparefunction=comparer)
        citibike['namesF'] = mp.newMap( numelements=300317,
                                                    prime=109345121,   
                                                    maptype='CHAINING', 
                                                    loadfactor=1.0, 
                                                    comparefunction=comparer)
        citibike['suscripcion'] = mp.newMap( numelements=300317,
                                                    prime=109345121,   
                                                    maptype='CHAINING', 
                                                    loadfactor=1.0, 
                                                    comparefunction=comparer)
        return citibike
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


def addStationI(citibike, trip):

    if m.contains(citibike["StationI"], trip['start station id']) == True:
        n = m.get(citibike["StationI"], trip['start station id'])
        lt.addLast(en.getValue(n), 2020-int(trip['birth year']))
    else:
        N = lt.newList("ARRAY_LIST")
        lt.addLast(N, 2020-int(trip['birth year']))
        m.put(citibike["StationI"], trip['start station id'], N)

def addStationF(citibike, trip):

    if m.contains(citibike["StationF"], trip['end station id']) == True:
        n = m.get(citibike["StationF"], trip['end station id'])
        lt.addLast(en.getValue(n), 2020-int(trip['birth year']))
    else:
        N = lt.newList("ARRAY_LIST")
        lt.addLast(N, 2020-int(trip['birth year']))
        m.put(citibike["StationF"], trip['end station id'], N)    

def addNamesLocationsI(citibike, trip):
    dicc = {}
    if m.contains(citibike["namesI"], trip['start station id']) == False:
        name = trip['start station name']
        latitud = trip['start station latitude']
        longitud = trip['start station longitude']
        dicc['nombre'] = name
        dicc['latitud'] = latitud
        dicc['longitud'] = longitud
        m.put(citibike["namesI"], trip['start station id'], dicc)
    else:
        None

def addNamesLocationsF(citibike, trip):
    dicc={}
    if m.contains(citibike["namesF"], trip['end station id']) == False:
        name = trip['end station name']
        latitud = trip['end station latitude']
        longitud = trip['end station longitude']
        dicc['nombre'] = name
        dicc['latitud'] = latitud
        dicc['longitud'] = longitud
        m.put(citibike["namesF"], trip['end station id'], dicc)
    else:
        None

def addSuscripcion(citibike, trip):
    listaX=[]
    edad = 2020-int(trip['birth year'])
    estacionI = trip['start station id']
    estacionF = trip['end station id']
    listaX.append(edad)
    listaX.append(estacionI)
    listaX.append(estacionF)
    if m.contains(citibike["suscripcion"], trip['usertype']) == True:
        n = m.get(citibike["suscripcion"], trip['usertype'])
        en.getValue(n).append(listaX)
    else:
        N = []
        N.append(listaX)
        m.put(citibike["suscripcion"], trip['usertype'], N) 

# Funciones para agregar informacion al grafo
def addTrip(citibike, trip):
    """
    """
    lt.addLast(citibike['lsttrips'], trip)
    origin = trip['start station id']
    destination = trip['end station id']
    duration = int(trip['tripduration'])
    age = 2020 - int(trip['birth year'])
    addStation(citibike, origin)
    addStation(citibike, destination)
    addConnection(citibike, origin, destination, duration, age)
    addConnection2(citibike, origin, destination, duration)


def addStation(citibike, stationid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(citibike ['graph'], stationid):
            gr.insertVertex(citibike ['graph'], stationid)

    if not gr.containsVertex(citibike ['grafo'], stationid):
            gr.insertVertex(citibike ['grafo'], stationid)
              
    return citibike


def addConnection2(citibike, origin, destination, duration):
    edge = gr.getEdge(citibike['grafo'], origin, destination)
    if origin != destination:
        gr.addEdge(citibike['grafo'], origin, destination, duration)
    return citibike


#Requerimiento 1 (Grupal)

def addConnection(citibike, origin, destination, duration, age):
    """
    Adiciona un arco entre dos estaciones
    """
    dicc = citibike['divide']
    dicc2 = {}
    edge = gr.getEdge(citibike['graph'], origin, destination)
    if origin != destination:
        if edge is None:
            dicc2["duracion"] = duration
            dicc2["contador"] = 1
            dicc2["edades"] = []
            dicc2["edades"].append(age)
            gr.addEdge(citibike['graph'], origin, destination, dicc2)
            dicc[str(origin)+"-"+str(destination)] = 1
        else:
            dicc[str(origin)+"-"+str(destination)] += 1
            edge['weight']["contador"] += 1
            valor = edge['weight']["duracion"]*(dicc[str(origin)+"-"+str(destination)]-1)
            valor += duration
            edge['weight']["duracion"] = (valor)/ dicc[str(origin)+"-"+str(destination)]
            edge["weight"]["edades"].append(age)
    return citibike



#Requerimiento 2

def req2(citibike, TiempoI, TiempoF, IdEstacionI):
    tiempoRuta=0
    if gr.containsVertex(citibike["graph"], IdEstacionI):
        verticesAdy=gr.adjacents(citibike["graph"], IdEstacionI)
    else:
        return("La estación escogida no existe")
    listaFinal=[]
    if verticesAdy["size"]==0:
        print("La estación escogida no tiene estaciones adyacentes")
    else:
        for i in range(0, (verticesAdy["size"]+1)):
            listaRuta=[]
            vertice=lt.getElement(verticesAdy, i)
            valorArco=gr.getEdge(citibike["graph"], IdEstacionI, vertice)["weight"]["duracion"]
            listaArcos=[]
            tiempoRuta=int(valorArco)
            listaRuta.append(IdEstacionI)
            listaRuta.append(vertice)
            listaArcos.append(valorArco)
            req2Parte2(citibike, TiempoI, TiempoF, vertice, tiempoRuta, listaFinal, IdEstacionI, listaRuta, listaArcos)
    return listaFinal


def req2Parte2(citibike, TiempoI, TiempoF, vertice, tiempoRuta, listaFinal, IdEstacionI, listaRuta, listaArcos):
    verticesAdy = gr.adjacents(citibike["graph"], vertice)
    if (verticesAdy["size"]==0):
        if  int(tiempoRuta)>= int(TiempoI) and int(tiempoRuta)<=int(TiempoF) and (str(listaRuta) + ": " + str(tiempoRuta) + "s " not in listaFinal):
            print("o")
            listaFinal.append(str(listaRuta) + ": " + str(tiempoRuta) + "s ")
        longitud=len(listaArcos)
        if longitud != 0:
            x=listaArcos.pop(len(listaArcos)-1)
            tiempoRuta-=int(x)
            y=listaRuta.pop(len(listaRuta)-1)
    elif (verticesAdy["size"]!=0):
        for j in range(0, (verticesAdy["size"]+1)):
            vertice2=lt.getElement(verticesAdy, j)
            valorArco2=int(gr.getEdge(citibike["graph"], vertice, vertice2)["weight"]["duracion"])
            if int(valorArco2) <= int(TiempoF):
                tiempoRuta+=valorArco2
                listaArcos.append(valorArco2)
                listaRuta.append(vertice2)
                req2Parte2(citibike, TiempoI, TiempoF, vertice2, tiempoRuta, listaFinal, IdEstacionI, listaRuta, listaArcos)
    return listaFinal


#Requerimiento_3
def requerimiento_3(citibike):
    lista = gr.vertices(citibike['grafo'])
    dicc1 = {}
    dicc2 = {}
    dicc3 = {}
    iterador = it.newIterator(lista)
    while it.hasNext(iterador):
        fila = it.next(iterador)
        out = gr.outdegree(citibike['grafo'], fila)
        ins = gr.indegree(citibike['grafo'], fila)
        dicc1[fila] = out
        dicc2[fila] = ins
        dicc3[fila] = out + ins
    salida = mayores(dicc1)
    llegada = mayores(dicc2)
    ambos = menores(dicc3)
    nombres_salida = encontrar(dicc1, salida)
    nombres_llegada = encontrar(dicc2, llegada)
    nombres_ambos = encontrar(dicc3, ambos)
    print("Las 3 mejores estaciones de salida son: ")
    nombresI(nombres_salida, citibike)
    print("\nLas 3 mejores estaciones de llegada son: ")
    nombresF(nombres_llegada, citibike)
    print("\nLas 3 peores estaciones de llegada/salida son: ")
    for i in range(0,3):
        if mp.contains(citibike["namesI"], nombres_ambos[i]):
            z=m.get(citibike["namesI"], nombres_ambos[i])
            nombreX=en.getValue(z)
            nombreI=nombreX["nombre"]
            print(nombreI)
        else:
            z=m.get(citibike["namesF"], nombres_ambos[i])
            nombreX=en.getValue(z)
            nombreI=nombreX["nombre"]
            print(nombreI)
            
def mayores(dicc):
    lista = []
    lista2 = []
    for i in dicc:
        lista.append(dicc[i])
    new = sorted(lista, reverse=True)
    for i in range(0, 3):
        dato = new[i]
        lista2.append(dato)
    return lista2
    
def menores(dicc):
    lista = []
    lista2 = []
    for i in dicc:
        lista.append(dicc[i])
    lista.sort()
    for i in range(0, 3):
        dato = lista[i]
        lista2.append(dato)
    return lista2

def encontrar(dicc, lista):
    lst = []
    for i in range(0,3):
        for j in dicc:
            if dicc[j] == lista[i]:
                lst.append(j)
    return lst
            
def nombresI(lista, citibike):
    for i in range(0,3):
        z=m.get(citibike["namesI"], lista[i])
        nombreX=en.getValue(z)
        nombreI=nombreX["nombre"]
        print(nombreI)

def nombresF(lista, citibike):
    for i in range(0,3):
        z=m.get(citibike["namesF"], lista[i])
        nombreX=en.getValue(z)
        nombreI=nombreX["nombre"]
        print(nombreI)
            



#Requerimiento 4

def req4(citibike, TiempoResistencia, IdEstacionI):
    tiempoRuta=0
    if gr.containsVertex(citibike["graph"], IdEstacionI):
        verticesAdy=gr.adjacents(citibike["graph"], IdEstacionI)
        z=m.get(citibike["namesI"], IdEstacionI)
        nombreX=en.getValue(z)
        nombreI=nombreX["nombre"]
    else:
        return("La estación escogida no existe")
    listaFinal=[]
    if verticesAdy["size"]==0:
        print("La estación escogida no tiene estaciones adyacentes")
    else:
        for i in range(0, (verticesAdy["size"]+1)):
            tiempoRuta=0
            listaRuta=lt.newList("SINGLED_LINKED")
            listaArcos=[]
            vertice=lt.getElement(verticesAdy, i)
            lt.addLast(listaRuta, vertice)
            valorArco=gr.getEdge(citibike["graph"], IdEstacionI, vertice)["weight"]["duracion"]
            listaArcos.append(valorArco)
            tiempoRuta=int(valorArco)
            req4Parte2(citibike, TiempoResistencia, vertice, tiempoRuta, listaRuta, listaFinal, IdEstacionI, listaArcos, nombreI)                                        
    return listaFinal

def req4Parte2(citibike, TiempoResistencia, vertice, tiempoRuta, listaRuta, listaFinal, IdEstacionI, listaArcos, nombreI):
    verticesAdy = gr.adjacents(citibike["graph"], vertice)
    if verticesAdy["size"]==0:
        if int(tiempoRuta)<=int(TiempoResistencia) and vertice!=IdEstacionI:
            o=m.get(citibike["namesF"], vertice)
            nombreO=en.getValue(o)
            nombreP=nombreO["nombre"]
            if (nombreI+" - "+nombreP +": " + str(tiempoRuta)+ "s ") not in listaFinal:
                listaFinal.append(nombreI+" - "+nombreP+": " + str(tiempoRuta) + "s ")
        y=lt.removeLast(listaRuta)
        longitud=len(listaArcos)
        if longitud != 0:
            x=listaArcos.pop(len(listaArcos)-1)
            tiempoRuta-=int(x)
    elif (verticesAdy["size"]!=0):
        for j in range(0, (verticesAdy["size"]+1)):
            vertice2=lt.getElement(verticesAdy, j)
            valorArco2=int(gr.getEdge(citibike["graph"], vertice, vertice2)["weight"]["duracion"])
            tiempoRuta+=valorArco2
            listaArcos.append(valorArco2)
            if listaRuta["size"]==0:
                None
            elif (vertice2 in listaRuta or int(tiempoRuta)>int(TiempoResistencia)):
                None
            elif int(tiempoRuta)<=int(TiempoResistencia):
                r=m.get(citibike["namesF"], vertice2)
                nombreE=en.getValue(r)
                nombreT=nombreE["nombre"]
                if (nombreI+" - "+nombreT +": " + str(tiempoRuta)+ "s ") not in listaFinal:
                    listaFinal.append(nombreI+" - "+nombreT+": "+ str(tiempoRuta) + "s ")
                lt.addLast(listaRuta, vertice2)
                req4Parte2(citibike, TiempoResistencia, vertice2, tiempoRuta, listaRuta, listaFinal, IdEstacionI, listaArcos, nombreI)
    return listaFinal




#Requerimiento 5 (grupal)

def Repeticiones(citibike, rangoI, rangoF):
    stationI = citibike['StationI']
    stationF = citibike['StationF']
    edadI = mp.keySet(stationI)
    edadF = mp.keySet(stationF)
    infoI = recorridos(edadI, stationI, rangoI, rangoF)
    infoF = recorridos(edadF, stationF, rangoI, rangoF)
    sI = maximoDicc(infoI)
    sF = maximoDicc(infoF)
    print("La estación de la que más personas salen, con ese rango de edad es: " + str(sI))
    print("La estación de la que más personas llegan, con ese rango de edad es: " + str(sF))
    camino = bfs.BreadhtFisrtSearch(citibike['graph'], sI)
    caminofinal = bfs.hasPathTo(camino, sF)
    print("Su camino es el siguiente: ")
    if caminofinal == True:
        ultimo = bfs.pathTo(camino, sF)
        iterador = it.newIterator(ultimo)
        while it.hasNext(iterador):
            fila = it.next(iterador)
            print(fila)
    else:
        print("No hay camino para ese rango de edades")

def recorridos(lista, mapa, rangoI, rangoF):
    dicc = {}
    iterador = it.newIterator(lista)
    while it.hasNext(iterador):
        fila = it.next(iterador)
        edades = m.get(mapa, fila)
        edades2 = en.getValue(edades)
        iterador2 = it.newIterator(edades2)
        while it.hasNext(iterador2):
            eda = int(it.next(iterador2))
            if eda >= rangoI and eda <= rangoF:
                if fila not in dicc:
                    dicc[fila] = 1
                else:
                    dicc[fila] += 1
    return dicc

def maximoDicc(dicc):
    if len(dicc) == 0:
        return "no hay estación"
    m = (max(dicc.values()))
    for i in dicc:
        if m == dicc[i]:
            va = i
    return va





#Requerimiento 6 (grupal)

def requerimiento_6(citibike, latitudI, longitudI, latitudF, longitudF):
    lista = []
    DistanciaI = NearestStation(citibike, latitudI, longitudI)
    DistanciaF = NearestStation(citibike, latitudF, longitudF)
    stationI = minimoDicc(DistanciaI)
    stationF = minimoDicc(DistanciaF)
    camino = bfs.BreadhtFisrtSearch(citibike['graph'], stationI)
    caminofinal = bfs.hasPathTo(camino, stationF)
    if caminofinal == True:
        ultimo = bfs.pathTo(camino, stationF)
        iterador = it.newIterator(ultimo)
        while it.hasNext(iterador):
            fila = it.next(iterador)
            lista.append(fila)
    else:
        print("No hay camino entre las dos estaciones")
    tiempo = 0
    for i in range(0, len(lista)-1):
        arco = gr.getEdge(citibike['graph'], lista[i], lista[i+1])["weight"]["duracion"]
        tiempo += arco
    print("La estación incial más cercana es: " + stationI)
    print("La estación final más cercana es: " + stationF)
    print("La duración del viaje es de: " + str(tiempo))
    print("La ruta es: " + str(lista))
 
def NearestStation(citibike, latitud, longitud):
    dicc2 = {}
    listaI = m.keySet(citibike['namesI'])
    iteradorI = it.newIterator(listaI)
    listaF = m.keySet(citibike['namesF'])
    iteradorF = it.newIterator(listaF)
    while it.hasNext(iteradorI):
        info = it.next(iteradorI)
        info2 = m.get(citibike['namesI'], info)
        dicc = en.getValue(info2)
        latitudv = dicc['latitud']
        longitudv = dicc['longitud']
        distancia = float(calcularDistancia(latitud, latitudv, longitud, longitudv))
        dicc2[info] = distancia
    while it.hasNext(iteradorF):
        info = it.next(iteradorF)
        info2 = m.get(citibike['namesF'], info)
        dicc = en.getValue(info2)
        latitudv = dicc['latitud']
        longitudv = dicc['longitud']
        distancia = float(calcularDistancia(latitud, latitudv, longitud, longitudv))
        dicc2[info] = distancia
    return dicc2

def calcularDistancia(lat1, lat2, lon1, lon2): 
    lon1 = radians(float(lon1)) 
    lon2 = radians(float(lon2))
    lat1 = radians(float(lat1)) 
    lat2 = radians(float(lat2))

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    
    c = 2 * atan2(sqrt(a), sqrt(1 - a)) 

    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371

    # calculate the result 
    return(c * r) 

def minimoDicc(dicc):
    if len(dicc) == 0:
        return "No existe la estación"
    m = (min(dicc.values()))
    for i in dicc:
        if m == float(dicc[i]):
            va = i
    return va




#Requerimiento 7

def requerimiento_7(citibike, rangoI, rangoF):
    dicc = {}
    lista = m.keySet(citibike['suscripcion'])
    iterador = it.newIterator(lista)
    while it.hasNext(iterador):
        info = it.next(iterador)
        if info == "Customer":
            info2 = m.get(citibike['suscripcion'], info)
            listaX = en.getValue(info2)
            for i in range(0, len(listaX)-1):
                if int(listaX[i][0])<=int(rangoF) and int(listaX[i][0])>=int(rangoI):
                    if listaX[i][1] +"-"+ listaX[i][2] not in dicc:
                        dicc[listaX[i][1] +"-"+ listaX[i][2]]=1
                    else:
                        dicc[listaX[i][1] +"-"+ listaX[i][2]]+=1
    x = (max(dicc.values()))
    for i in dicc:
        if x == float(dicc[i]):
            va = i
    print("Las estaciones adyacentes más utilizadas son: " + str(va))
    print("Con un total de viajes de: " + str(x))
    print("")
    print("Las estaciones que cumplen las condiciones son las siguientes: ")
    for i in dicc:
        llave=i
        valor=dicc[i]
        print(str(i) +": "+ str(dicc[i]))



#Requerimiento 8

#def requerimiento_8(citibike, IDBicicleta, Fecha):
    





# ==============================
# Funciones de consulta
# ==============================

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['graph'])
    return scc.connectedComponents(analyzer['components'])


def IsItConnected(analyzer, verta, vertb):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    if gr.containsVertex(analyzer["graph"], verta) and gr.containsVertex(analyzer["graph"], vertb):
        analyzer['components'] = scc.KosarajuSCC(analyzer['graph'])
        return scc.stronglyConnected(analyzer['components'], verta, vertb)
    else: 
        print("La estación no existe")
        return False


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['graph'], initialStation)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])


def servedRoutes(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['stops'])
    itlstvert = it.newIterator(lstvert)
    maxvert = None
    maxdeg = 0
    while(it.hasNext(itlstvert)):
        vert = it.next(itlstvert)
        lstroutes = m.get(analyzer['stops'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg




# ==============================
# Funciones Helper
# ==============================
def numSCC(graph, sc):
    sc = scc.KosarajuSCC(graph)
    return scc.connectedComponents(sc)

def sameCC(sc, station1, station2):
    sc = scc.KosarajuSCC(graph)
    return scc.stronglyConnected(sc, station1, station2)





# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def comparer(keyname, value):
    entry = en.getKey(value)
    if (keyname == entry):
        return 0
    elif (keyname > entry):
        return 1
    else:
        return -1