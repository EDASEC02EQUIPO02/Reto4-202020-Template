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
        citibike['names'] = mp.newMap( numelements=300317,
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

def addNamesLocations(citibike, trip):
    dicc = {}
    if m.contains(citibike["names"], trip['start station id']) == False:
        name = trip['start station name']
        latitud = trip['start station latitude']
        longitud = trip['start station longitude']
        dicc['nombre'] = name
        dicc['latitud'] = latitud
        dicc['longitud'] = longitud
        m.put(citibike["names"], trip['start station id'], dicc)
    else:
        None

    if m.contains(citibike["names"], trip['end station id']) == False:
        name = trip['end station name']
        latitud = trip['end station latitude']
        longitud = trip['end station longitude']
        dicc['nombre'] = name
        dicc['latitud'] = latitud
        dicc['longitud'] = longitud
        m.put(citibike["names"], trip['end station id'], dicc)
    else:
        None
    


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
    print(infoI)
    print(infoF)
    print("La estación en la que más personas salen ese rango de edad es: " + str(sI))
    print("La estación en la que más personas llegan ese rango de edad es: " + str(sF))
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
"""
def req_3(citibike, origin, tiempo1, tiempo2):
    citibike['components'] = scc.KosarajuSCC(citibike['graph'])
    #valor = scc.sccCount(citibike['graph'], citibike['components'], origin)
    value = m.get(citibike['components']['idscc'], origin)['value'] #numero de componente
    ayuda = origin
    algo = "hola"
    nombre = origin
    while origin != algo:
        algo = origin
        lista = gr.adjacents(citibike['graph'], origin)
        valor = Funcion_adyacente(lista, value, citibike, algo)
        lista_de_nombres = Funcion_recorrido(valor, algo, value)
        while j < len(lista_de_nombres):
        

def Funcion_recorrido(dicc, name, value):
    lista = []
    dicc = {}
    if len(valor) == 1:
        for i in valor:
            nombre = i
            return lista.append(nombre)
    if len(valor) > 1:
        for i in valor:
            nombre = i
            lista = gr.adjacents(citibike['graph'], i)
            valor = Funcion_adyacente(lista, value, citibike, i)
            nombre2 = Funcion_recorrido(valor, i, value)
            dicc[i] = nombre2
            lista.append(dicc)
        
def Funcion_adyacente(lista, value, graph, origin):
    lst = []
    lista = it.newIterator(lista)
    while it.hasNext(lista):
        fila = it.next(lista)
        kosa = m.get(graph['components']['idscc'], fila)['value']
        if kosa  == value:
            lst.append(fila)
    if len(lst) > 1:
        dicc = {}
        j = 0
        while j < len(lst):
            final = lst[j]
            arco = gr.getEdge(graph['graph'], origin, final)
            time = arco['weight']["duracion"]
            dicc[final] = time
            j += 1
        return dicc
    else:
        final = lst[0]
        arco = gr.getEdge(graph['graph'], origin, final)
        print(arco)
        time = arco['weight']["duracion"]
        menor = time
        return {final: menor}
"""
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
    nombres(nombres_salida)
    print("\nLas 3 mejores estaciones de llegada son: ")
    nombres(nombres_llegada)
    print("\nLas 3 peores estaciones de llegada/salida son: ")
    nombres(nombres_ambos)


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
            
def nombres(lista):
    for i in range(0,3):
        print(lista[i])
            
#Requerimiento 4

def req4(citibike, TiempoResistencia, IdEstacionI):
    tiempoRuta=0
    if gr.containsVertex(citibike["graph"], IdEstacionI):
        verticesAdy=gr.adjacents(citibike["graph"], IdEstacionI)
    else:
        return("La estación escogida no existe")
    listaFinal=[]
    if verticesAdy["size"]==0:
        print("La estación escogida no tiene estaciones adyacentes")
    else:
        for i in range(1, (verticesAdy["size"]+1)):
            listaRuta=lt.newList("SINGLED_LINKED")
            listaArcos=[]
            vertice=lt.getElement(verticesAdy, i)
            lt.addLast(listaRuta, vertice)
            valorArco=gr.getEdge(citibike["graph"], IdEstacionI, vertice)["weight"]["duracion"]
            listaArcos.append(valorArco)
            tiempoRuta=int(valorArco)
            req4Parte2(citibike, TiempoResistencia, vertice, tiempoRuta, listaRuta, listaFinal, IdEstacionI, listaArcos)                                        
    return listaFinal


def req4Parte2(citibike, TiempoResistencia, vertice, tiempoRuta, listaRuta, listaFinal, IdEstacionI, listaArcos):
    verticesAdy = gr.adjacents(citibike["graph"], vertice)
    if verticesAdy["size"]==0 and int(tiempoRuta)<=int(TiempoResistencia) and vertice!=IdEstacionI:
        if (IdEstacionI+"-"+vertice +": " + str(tiempoRuta)) not in listaFinal:
            listaFinal.append(IdEstacionI+"-"+vertice +": " + str(tiempoRuta) + "s ")
        y=lt.removeLast(listaRuta)
        longitud=len(listaArcos)
        if longitud != 0:
            x=listaArcos.pop(len(listaArcos)-1)
            tiempoRuta-=int(x)
    elif (verticesAdy["size"]!=0):
        for j in range(1, (verticesAdy["size"]+1)):
            vertice2=lt.getElement(verticesAdy, j)
            valorArco2=int(gr.getEdge(citibike["graph"], vertice, vertice2)["weight"]["duracion"])
            tiempoRuta+=valorArco2
            if listaRuta["size"]==0:
                None
            elif (vertice2 in listaRuta or int(tiempoRuta)>int(TiempoResistencia)):
                None
            elif int(tiempoRuta)<=int(TiempoResistencia):
                listaFinal.append(IdEstacionI+"-"+vertice2+": "+ str(tiempoRuta))
                lt.addLast(listaRuta, vertice2)
                req4Parte2(citibike, TiempoResistencia, vertice2, tiempoRuta, listaRuta, listaFinal, IdEstacionI, listaArcos)
    return listaFinal



#Requerimiento 6 (grupal)

def requerimiento_6(citibike, latitudI, longitudI, latitudF, longitudF):
    lista = []
    DistanciaI = NearestStation(citibike, latitudI, longitudI)
    DistanciaF = NearestStation(citibike, latitudF, longitudF)
    stationI = minimoDicc(DistanciaI)
    stationF = minimoDicc(DistanciaF)
    print(stationI)
    print(stationF)
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
    for i in range(1, len(lista)-1):
        arco = gr.getEdge(citibike['graph'], lista[i], lista[i+1])
        tiempo += arco['weight']['duracion']
    print("La estación incial más cercana es: " + stationI)
    print("La estación final más cercana es: " + stationF)
    print("La duración del viaje es de: " + str(tiempo))
    print("La ruta es: " + str(lista))

        
def NearestStation(citibike, latitud, longitud):
    dicc2 = {}
    lista = m.keySet(citibike['names'])
    iterador = it.newIterator(lista)
    while it.hasNext(iterador):
        info = it.next(iterador)
        info2 = m.get(citibike['names'], info)
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
    print(dicc)
    m = (min(dicc.values()))
    for i in dicc:
        if m == float(dicc[i]):
            va = i
    return va







#Requerimiento 7

#def requerimiento_7(cont, RangoEdad):




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