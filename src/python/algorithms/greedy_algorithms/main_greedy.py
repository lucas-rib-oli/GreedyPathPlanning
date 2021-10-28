#! /usr/bin/env python
import os
import argparse
import numpy as np
import copy
import cv2
import time

## A nivel mapa
### Del mapa original
### * 0: libre
### * 1: ocupado (muro/obstáculo)
### Nós
### * 2: visitado
### * 3: start
### * 4: goal

## A nivel grafo
### Nós
### * -2: parentId del nodo start
### * -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

## Ejes

## 
# ------------------- Y
# |
# |
# |
# |
# |
# |

# X

## Ansi colors
class bcolors: 
    RESET = '\033[0m'
    BLACK = '\033[30m'     
    RED = '\033[31m'     
    GREEN = '\033[32m'      
    YELLOW = '\033[33m'    
    BLUE = '\033[34m'      
    MAGENTA = '\033[35m'     
    CYAN = '\033[36m'     
    WHITE = '\033[37m'      
    BOLDBLACK = '\033[1m\033[30m'      
    BOLDRED = '\033[1m\033[31m'    
    BOLDGREEN = '\033[1m\033[32m'      
    BOLDYELLOW = '\033[1m\033[33m'      
    BOLDBLUE = '\033[1m\033[34m'      
    BOLDMAGENTA = '\033[1m\033[35m'      
    BOLDCYAN = '\033[1m\033[36m'      
    BOLDWHITE = '\033[1m\033[37m'   

## Initial values are hard-coded (A nivel mapa)

class NeighborsPoint:
    def __init__(self, x, y, position):
        self.x = x
        self.y = y
        self.position = position
        

## Define Node class (A nivel grafo/nodo)

class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
        self.dist = -1 # Distancia al punto final
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId)+\
                         " | distancia " + str (self.dist))
    def __lt__(self, neighbor): # Para ordenar los nodos por distancia al objetivo
        return self.dist < neighbor.dist
         

## creamos función para volcar estructura de datos para mapa
def dumpMap(charMap, currentX = -1, currentY = -1):
    i = 0
    for line in charMap:
        j = 0
        for point in line:
            if i == currentX and j == currentY:
                print (bcolors.BOLDMAGENTA + point + bcolors.RESET + " ", end = '')
            elif point == '0':
                print (bcolors.BOLDGREEN + point + bcolors.RESET + " ", end = '')
            elif point == '1':
                print (bcolors.BOLDRED + point + bcolors.RESET + " ", end = '')
            elif point == '2':
                print (bcolors.BOLDBLUE + point + bcolors.RESET + " ", end = '')
            elif point == '3':
                print (bcolors.BOLDWHITE + point + bcolors.RESET + " ", end = '')
            else:
                print (bcolors.BOLDYELLOW + point + bcolors.RESET + " ", end = '')
            j = j + 1 
        i = i + 1
        print ()

def dumpMapImage (charMap, currentX = -1, currentY = -1):
    
    charMap_copy = copy.deepcopy(charMap)
    
    charMap_copy [currentX][currentY] = '5' # Nodo actual
    map_to_image = getMapInImageCoordinates (charMap_copy) # En coordenadas de una imagen

    row_step = len (charMap)
    col_step = len (charMap[0])
    rows = 50 * row_step
    cols = 50 * col_step
    gridMapImage = np.ones((rows, cols, 3), dtype = "uint8") #3channel

    x = np.linspace(start=0, stop=cols, num=col_step + 1)
    y = np.linspace(start=0, stop=rows, num=row_step + 1)

    tl_points = []
    br_points = []
    for i in range( len (x) - 1 ):
        tl_x_point = x [i]
        br_x_point = x [i + 1]
        for j in range ( len(y) - 1 ):
            tl_y_point = y [j]
            br_y_point = y [j + 1]
            tl_points.append( ( int (tl_x_point), int (tl_y_point) ) )
            br_points.append( ( int (br_x_point), int (br_y_point) ) )

    unordored_map = []
    for i in map_to_image:
        for j in i:
            unordored_map.append (j)
        
    for i in range (len (tl_points)):
        tl_point = tl_points [i]
        br_point = br_points [i]

        if ( unordored_map [i] == '5' ): # Nodo actual
            color = (0, 255, 0)
        elif ( unordored_map [i] == '0' ): # Celda libre
            color = (255, 255, 255)
        elif ( unordored_map [i] == '1' ): # Celda ocupada
            color = (0, 0, 255)
        elif ( unordored_map [i] == '2' ): # Celda visitada
            color = (255, 0, 0)
        elif ( unordored_map [i] == '3' ): # Punto de inicio
            color = (255, 255, 0)
        else: # Meta
            color = (0, 255, 255)
        cv2.rectangle ( gridMapImage, tl_point, br_point, color, thickness = -1 )
        cv2.rectangle ( gridMapImage, tl_point, br_point, (0, 0, 0), thickness = 2 )
   
    gridMapImage_resized = cv2.resize (gridMapImage, (400, 500))
    cv2.imshow('Grid Map Image', gridMapImage_resized)
    cv2.waitKey(10)                

## Salida de la ruta por imagen
def dumpPathImage (charMap, nodes, goalParentId):
    charMap_copy = copy.deepcopy(charMap)

    ok = False
    while not ok:
        for node in nodes:
            if( node.myId == goalParentId ):
                charMap_copy [node.x][node.y] = '6' # Path to goal
                goalParentId = node.parentId
                if( goalParentId == -2):
                    ok = True
    
    map_to_image = getMapInImageCoordinates (charMap_copy) # En coordenadas de una imagen
   
    row_step = len (charMap)
    col_step = len (charMap[0])
    rows = 50 * row_step
    cols = 50 * col_step
    gridMapImage = np.ones((rows, cols, 3), dtype = "uint8") #3channel

    x = np.linspace(start=0, stop=cols, num=col_step + 1)
    y = np.linspace(start=0, stop=rows, num=row_step + 1)

    tl_points = []
    br_points = []
    for i in range( len (x) - 1 ):
        tl_x_point = x [i]
        br_x_point = x [i + 1]
        for j in range ( len(y) - 1 ):
            tl_y_point = y [j]
            br_y_point = y [j + 1]
            tl_points.append( ( int (tl_x_point), int (tl_y_point) ) )
            br_points.append( ( int (br_x_point), int (br_y_point) ) )

    unordored_map = []
    for i in map_to_image:
        for j in i:
            unordored_map.append (j)
        
    for i in range (len (tl_points)):
        tl_point = tl_points [i]
        br_point = br_points [i]

          
        if ( unordored_map [i] == '0' ): # Celda libre
            color = (255, 255, 255)
        elif ( unordored_map [i] == '1' ): # Celda ocupada
            color = (0, 0, 255)
        elif ( unordored_map [i] == '2' ): # Punto visitado
            color = (255, 0, 0)
        elif ( unordored_map [i] == '3' ): # Punto de inicio
            color = (255, 255, 0)
        elif ( unordored_map [i] == '6' ): # Ruta
            color = (0, 0, 0)
        else:
            color = (0, 255, 255) # Meta
        cv2.rectangle ( gridMapImage, tl_point, br_point, color, thickness = -1 )
        cv2.rectangle ( gridMapImage, tl_point, br_point, (0, 0, 0), thickness = 2 )
   
    gridMapImage_resized = cv2.resize (gridMapImage, (400, 500))
    cv2.imshow('Grid Map Image', gridMapImage_resized)
    print (bcolors.BOLDBLUE + "Pulsa una tecla para terminar (con la imagen clickeada)" + bcolors.RESET)
    cv2.waitKey(0)

# Breadth First Search Algorithm
def breadthFS (charMap, args):
    ## `nodes` contendrá los nodos visitados del grafo
    nodes_visited = []
    queue = [] # cola de nodos 

    ## creamos primer nodo
    init = Node(args.start_x, args.start_y, 0, -2)
    # init.dump()  # comprobar que primer nodo bien

    queue.append (init) # Añadimos el primer nodo a la cola

    ## volcamos mapa por consola
    dumpMap(charMap)

    ###### Empieza algoritmo
    goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

    n = 0 # simple contador de nodos
    iterations = 0 # numero de iteraciones a 0
    while len (queue) > 0: # mientras la cola no esté vacia 
        iterations = iterations + 1
        current = queue.pop (0) # El nodo actual es el primer nodo de la cola y borramos el nodo de la cola

        ## añadimos el nodo acutual a `nodes_visited`
        nodes_visited.append(current)
        print( "--------------------- number of nodes: " + str( len (nodes_visited) ) )
        x = current.x
        y = current.y

        current.dump() # volcamos el nodo actual

        if( charMap[x][y] == '4' ): # Si el nodo actual es la meta 
            print ('nodo actual: GOLASOOO !!!')
            goalParentId = current.myId
            return nodes_visited, goalParentId, iterations

        if (args.neighbourhood == 4): # vecindad 4
            neighbors_points = [NeighborsPoint (x - 1, y, "up"),
                                NeighborsPoint (x, y + 1, "right"),
                                NeighborsPoint (x + 1, y, "down"), 
                                NeighborsPoint (x, y - 1, "left")]
        else: # vecindad 8
            neighbors_points = [NeighborsPoint (x - 1, y, "up"),
                                NeighborsPoint (x - 1, y + 1, "up-right"),
                                NeighborsPoint (x, y + 1, "right"),
                                NeighborsPoint (x + 1, y + 1, "down-right"), 
                                NeighborsPoint (x + 1, y, "down"), 
                                NeighborsPoint (x + 1, y - 1, "down-left"),
                                NeighborsPoint (x, y - 1, "left"),
                                NeighborsPoint (x - 1, y - 1, "up-left")]
        for neighbor_point in neighbors_points: # for each neighbor of current
            n = n + 1 # incrementamos el contador
            x_n = neighbor_point.x # coordenadas del nodo vecino
            y_n = neighbor_point.y
            position = neighbor_point.position # posicion del nodo vecino con respecto al nodo actual
            
            if( charMap[x_n][y_n] == '4' ):
                print(position + ": GOALLLL!!!")
                goalParentId = current.myId  # aquí sustituye por real
                return nodes_visited, goalParentId, iterations

            if ( charMap[x_n][y_n] == '2' or  charMap[x_n][y_n] == '1' ): 
                continue # continuamos si está visitado o es obstaculo

            if ( charMap[x_n][y_n] == '0' ): # si está libre (no visitado) marcamos como visitado y lo añadimos a la cola
                 print (position + ": mark visited")
                 newNode = Node (x_n, y_n, n, current.myId)
                 queue.append (newNode) # lo añadimos a la cola
                 charMap[x_n][y_n] = '2' # marcamos como visitado
                 
        dumpMap(charMap, current.x, current.y)
        if (args.viz): # Mostrar imagen
            dumpMapImage (charMap, current.x, current.y)

# Depth First Search Algorithm
def depthFS (charMap, args):
    ## `nodes` contendrá los nodos del grafo
    nodes = []
    explored = []

    ## creamos primer nodo
    init = Node(args.start_x, args.start_y, 0, -2)

    ## añadimos el primer nodo a `nodos`
    nodes.append(init)

    ## volcamos mapa por consola
    dumpMap(charMap, -1, -1)

    ###### Empieza algoritmo
    goalParentId = -1  # -1: parentId del nodo goal PROVISIONAL cuando aun no se ha resuelto

    n = 0
    iterations = 0
    while len (nodes) > 0: # Mientras nodes no esté vacio
        iterations = iterations + 1 # Aumentamos el numero de iteraciones
        print("--------------------- number of nodes: " + str(len(nodes)))
        node = nodes.pop (-1) # Element that is inserted at the last or most recently inserted element.
        node.dump()
        
        x = node.x
        y = node.y
        explored.append (node)

        # Orden de preferencia: left -- down -- right -- up
        if (args.neighbourhood == 4):
            neighbors_points = [NeighborsPoint (x - 1, y, "up"),
                                NeighborsPoint (x, y + 1, "right"),
                                NeighborsPoint (x + 1, y, "down"), 
                                NeighborsPoint (x, y - 1, "left")]
        else: 
            neighbors_points = [NeighborsPoint (x - 1, y, "up"),
                                NeighborsPoint (x - 1, y + 1, "up-right"),
                                NeighborsPoint (x, y + 1, "right"),
                                NeighborsPoint (x + 1, y + 1, "down-right"), 
                                NeighborsPoint (x + 1, y, "down"), 
                                NeighborsPoint (x + 1, y - 1, "down-left"),
                                NeighborsPoint (x, y - 1, "left"),
                                NeighborsPoint (x - 1, y - 1, "up-left")]
        
        for neighbor_point in neighbors_points:
            n = n + 1
            x_n = neighbor_point.x
            y_n = neighbor_point.y
            position = neighbor_point.position

            if( charMap[x_n][y_n] == '4' ):
                print (position + ': GOLASOOO !!!')
                goalParentId = node.myId
                return explored, goalParentId, iterations

            if ( charMap[x_n][y_n] == '2' or  charMap[x_n][y_n] == '1' ): # si está ocupado o visitado cambiamos dirección
                continue
            if ( charMap[x_n][y_n] == '0' ):
                print (position + ': mark visited')
                newNode = Node(x_n, y_n, n, node.myId)
                charMap[x_n][y_n] = '2'
                nodes.append(newNode)

        dumpMap(charMap, node.x, node.y) # imprimimos mapa
        if (args.viz):
            dumpMapImage (charMap, node.x, node.y)

# Best First Search Algorithm
def bestFS (charMap, args):
    nodes = []
    ## creamos primer nodo
    init = Node(args.start_x, args.start_y, 0, -2)

    if (args.cost == 'euclidean'):
        init.dist = euclideanDistance ( args.end_x, args.end_y, args.start_x, args.start_y ) # distancia Euclidea 
    else:
        init.dist = manhattanDistance ( args.end_x, args.end_y, args.start_x, args.start_y ) # distancia Manhattan 

    
    nodes.append (init) # añadimos el nodo de inicio a la lista
    queue = [] # Nodos ordenados por distancia
    queue.append (init)
    n = 0
    iterations = 0
    while len (queue) > 0: # Mientras la cola no esté vacia

        iterations = iterations + 1 # Aumentamos el numero de iteraciones 
        # vértice de la lista con distancia mínima al objetivo
        node = queue.pop (0) # Eliminamos el nodo actual de la lista de nodos
        nodes.append(node) # Para realizar la regresión de los nodos

        node.dump() # Imprimimos por pantalla el nodo actual
        x = node.x
        y = node.y

        if (args.neighbourhood == 4): # Solo arriba, abajo, derecha e izquierda
            neighbors_points = [NeighborsPoint (x - 1, y, "up"),
                                NeighborsPoint (node.x, y + 1, "right"), 
                                NeighborsPoint (x + 1, y, "down"), 
                                NeighborsPoint (x, y - 1, "left")]
        else: # Incluyendo las esquinas
            neighbors_points = [NeighborsPoint (x - 1, y, "up"),
                                NeighborsPoint (x - 1, y + 1, "up-right"),
                                NeighborsPoint (x, y + 1, "right"),
                                NeighborsPoint (x + 1, y + 1, "down-right"), 
                                NeighborsPoint (x + 1, y, "down"), 
                                NeighborsPoint (x + 1, y - 1, "down-left"),
                                NeighborsPoint (x, y - 1, "left"),
                                NeighborsPoint (x - 1, y - 1, "up-left")]
        
        for neighbor_point in neighbors_points:
            x_n = neighbor_point.x
            y_n = neighbor_point.y
            position = neighbor_point.position
            n = n + 1

            if( charMap[x_n][y_n] == '4' ):
                print (position + ': GOLASOOO !!!')
                goalParentId = node.myId
                return nodes, goalParentId, iterations

            if ( charMap[x_n][y_n] == '2' or  charMap[x_n][y_n] == '1'): # si está ocupado o visitado cambiamos dirección
                continue

            if ( charMap[x_n][y_n] == '0' ):
                print (position + ': mark visited')
                charMap[x_n][y_n] = '2'
                newNode = Node(x_n, y_n, n, node.myId)
                # newNode.dist = np.abs (END_X - x) + np.abs (END_Y - y) # distancia Manhattan
                if (args.cost == 'euclidean'):
                    newNode.dist = euclideanDistance (args.end_x, args.end_y, x_n, y_n) # distancia Euclidea
                else:
                    newNode.dist = manhattanDistance (args.end_x, args.end_y, x_n, y_n) # distancia Manhattan
                queue.append (newNode)
        
        queue.sort() # Ordenamos la cola de nodos por distancia mínima
        dumpMap(charMap, node.x, node.y)
        if (args.viz): # Mostrar por imagen   
            dumpMapImage (charMap, node.x, node.y)
        
            

class AStarNode:
    def __init__(self, x, y, myId, parentId, gScore = -1, fScore = -1):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
        self.dist = -1 # Distancia al punto final
        self.cameFrom = []
        self.gScore = np.inf
        self.fScore = np.inf
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId)+\
                         " | gScore " + str (self.gScore)+\
                         " | fScore " + str (self.fScore) )
    def __lt__(self, neighbor): # Para ordenar los nodos por distancia al objetivo
        return self.fScore < neighbor.fScore
    def __eq__(self, neighbor):
        return self.x == neighbor.x and self.y == neighbor.y

def a_estrellita (charMap, args):
    # El conjunto de nodos descubiertos que pueden necesitar ser (re)ampliados.
    # Inicialmente, sólo se conoce el nodo inicial.
    # Esto se implementa normalmente como una cola de minisuperficie o de prioridad en lugar de un conjunto de hash.
    openSet = []
    init = AStarNode (args.start_x, args.start_y, 0, -2)

    # Para el nodo n, gScore[n] es el coste del camino más barato desde el inicio hasta n conocido actualmente.
    # gScore := map with default value of Infinity
    # gScore[start] := 0
    gScore = []
    init.gScore = 0 # Coste para el inicio 0

    # Para el nodo n, fScore[n] := gScore[n] + h(n). fScore[n] representa nuestra mejor estimación actual sobre lo corto que puede ser un camino 
    # desde el principio hasta el final si pasa por n.
    # fScore := map with default value of Infinity
    # fScore[start] := h(start)
    if (args.cost == 'euclidean'):
        init.fScore = euclideanDistance (args.end_x, args.end_y, args.start_x,  args.start_y) # Se usa como función de coste la distancia euclidea
    else:
        init.fScore = manhattanDistance (args.end_x, args.end_y, args.start_x,  args.start_y) # Se usa como función de coste la distancia Manhattan

    # openSet := {start}
    openSet.append (init)    

    # Para el nodo n, cameFrom[n] es el nodo inmediatamente anterior en el camino más barato desde el inicio
    # a n actualmente conocido.
    # cameFrom := an empty map
    cameFrom = []


    n = 0
    iterations = 0
    while len (openSet) > 0: # while openSet is not empty
        iterations = iterations + 1
        openSet.sort () # Ordenamos los nodos con el fScore más bajo
        # Esta operación puede producirse en tiempo O(1) si openSet es un miniapósito o una cola prioritaria
        # current := the node in openSet having the lowest fScore[] value
        current = openSet [0] # nodo de openSet conel valor fScore[] más bajo
        x = current.x
        y = current.y
        current.dump()

        cameFrom.append (current)

        if( charMap[x][y] == '4' ): # Si el nodo actual es la meta 
            print ('nodo actual: GOLASOOO !!!')
            goalParentId = current.myId
            return cameFrom, goalParentId, iterations

        # Puntos vecinos
        if ( args.neighbourhood == 4): # Solo arriba, abajo, derecha e izquierda
            neighbors_points = [NeighborsPoint (x - 1, y, "up"),
                                NeighborsPoint (x, y + 1, "right"),
                                NeighborsPoint (x + 1, y, "down"), 
                                NeighborsPoint (x, y - 1, "left") ]
        else: # Incluyendo las esquinas
            neighbors_points = [NeighborsPoint (x - 1, y, "up"),
                                NeighborsPoint (x - 1, y + 1, "up-right"),
                                NeighborsPoint (x, y + 1, "right"),
                                NeighborsPoint (x + 1, y + 1, "down-right"), 
                                NeighborsPoint (x + 1, y, "down"), 
                                NeighborsPoint (x + 1, y - 1, "down-left"),
                                NeighborsPoint (x, y - 1, "left"),
                                NeighborsPoint (x - 1, y - 1, "up-left")]


        # openSet.Remove(current)
        openSet.pop (0)
        for neighbor_point in neighbors_points: # for each neighbor of current
            x_n = neighbor_point.x
            y_n = neighbor_point.y
            position = neighbor_point.position

            if( charMap[x_n][y_n] == '4' ): # Si el nodo actual es la meta 
                print (position + ': GOLASOOO !!!')
                goalParentId = current.myId
                return cameFrom, goalParentId, iterations

            if ( charMap[x_n][y_n] == '2' or  charMap[x_n][y_n] == '1' ): # si está ocupado o visitado cambiamos dirección
                continue

            if ( charMap[x_n][y_n] == '0' ):
                if (args.cost == 'euclidean'):
                    neighbor_h = euclideanDistance (args.end_x, args.end_y, neighbor_point.x, neighbor_point.y)
                else:
                    neighbor_h = manhattanDistance (args.end_x, args.end_y, neighbor_point.x, neighbor_point.y)
                neighbor_node = AStarNode (neighbor_point.x, neighbor_point.y, -1, -1)
                
                if (args.cost == 'euclidean'):
                    tentative_gScore = current.gScore + euclideanDistance (x_n, y_n, x, y) # tentative_gScore es la distancia desde el inicio hasta el vecino a través de la corriente
                else:
                    tentative_gScore = current.gScore + manhattanDistance (x_n, y_n, x, y) # tentative_gScore es la distancia desde el inicio hasta el vecino a través de la corriente
                
                if tentative_gScore < neighbor_node.gScore: # Este camino hacia el vecino es mejor que cualquier otro anterior. ¡Grábalo!
                    neighbor_node.cameFrom.append (current) # cameFrom[neighbor] := current
                    neighbor_node.gScore = tentative_gScore
                    neighbor_node.fScore = neighbor_node.gScore + neighbor_h
                    
                    if not (neighbor_node in openSet):
                        print (position + ': mark visited')
                        n = n + 1
                        neighbor_node.myId = n
                        neighbor_node.parentId = current.myId
                        openSet.append (neighbor_node) # if neighbor not in openSet
                        charMap[x_n][y_n] = '2'


        dumpMap( charMap, current.x, current.y ) # imprimimos mapa
        if (args.viz): # Mostrar imagen
            dumpMapImage ( charMap, current.x, current.y )

def euclideanDistance (x2, y2, x1, y1):
    return np.sqrt( np.power ( (x2 - x1), 2 ) + np.power ( (y2 - y1), 2 ) )

def manhattanDistance (x2, y2, x1, y1):
    return  ( np.abs (x2 - x1) + np.abs (y2 - y1) )

def getMapInImageCoordinates (grid_map):
    map_to_image = np.array ( grid_map )
    map_to_image = np.transpose ( map_to_image ) # En coordenadas de una imagen
    return map_to_image

def main ():
    os.system('cls||clear') # Limpiamos consola 
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--root", type=str, default="/media/lsi/1C9E1EC99E1E9AFA/UC3M/Introduccion_Planificacion_Robots/GreedyPathPlanning", help="path to folder map")
    parser.add_argument("--map", type=int, default=1, help="number of map")
    parser.add_argument("--start_x", type=int, default=2, help="start coordinate x")
    parser.add_argument("--start_y", type=int, default=2, help="start coordinate y")
    parser.add_argument("--end_x", type=int, default=7, help="end coordinate x")
    parser.add_argument("--end_y", type=int, default=2, help="end coordinate y")
    parser.add_argument("-a", "--algorithm", type=str, default="a_star", help="breadth / depth / best / a_star")
    parser.add_argument("-n", "--neighbourhood", type=int, default=8, help="4 / 8 neighbourhood to use")
    parser.add_argument("-c", "--cost", type=str, default="euclidean", help="cost fuction to use - euclidean / manhattan")
    parser.add_argument("--viz", type=int, default=1, help="visualization in image")
    args = parser.parse_args()
    print (bcolors.BOLDBLUE+ "------------------------- PARAMETROS -------------------------" + bcolors.RESET)
    print (bcolors.BOLDGREEN + "Mapa: " + bcolors.BOLDCYAN + str(args.map))
    print (bcolors.BOLDGREEN + "Start X: " + bcolors.BOLDCYAN + str(args.start_x))
    print (bcolors.BOLDGREEN + "Start Y: " + bcolors.BOLDCYAN + str(args.start_y))
    print (bcolors.BOLDGREEN + "End X: " + bcolors.BOLDCYAN + str(args.end_x))
    print (bcolors.BOLDGREEN + "End Y: " + bcolors.BOLDCYAN + str(args.end_y))
    print (bcolors.BOLDGREEN + "Algoritmo: " + bcolors.BOLDCYAN + str(args.algorithm))
    print (bcolors.BOLDGREEN + "Vecindad: " + bcolors.BOLDCYAN + str(args.neighbourhood))
    print (bcolors.BOLDGREEN + "Funcion de coste: " + bcolors.BOLDCYAN + str(args.cost))
    print (bcolors.BOLDGREEN + "Visualizacion por imagen: " + bcolors.BOLDCYAN + str(args.viz))
    print (bcolors.BOLDBLUE + "--------------------------------------------------------------" + bcolors.RESET)

    FILE_NAME = os.path.join (args.root, "map" + str(args.map), "map" + str(args.map) + ".csv")

    if (not os.path.exists (FILE_NAME)):
        print (bcolors.BOLDRED + "Path al mapa no encontrado: " + FILE_NAME + bcolors.RESET )
        exit (0)
    START_X = args.start_x
    START_Y = args.start_y
    END_X = args.end_x
    END_Y = args.end_y
    ALGORITHM = args.algorithm

    ## creamos estructura de datos para mapa
    charMap = []    

    ## de fichero, (to parse/parsing) para llenar estructura de datos para mapa
    with open(FILE_NAME) as f:
        line = f.readline()
        while line:
            charLine = line.strip().split(',')
            charMap.append(charLine)
            line = f.readline()
    
    ## a nivel mapa, integramos la info que teníamos de start & end

    charMap[START_X][START_Y] = '3' # 3: start
    charMap[END_X][END_Y] = '4' # 4: goal

    start = time.time() # Para calcular el tiempo de ejecución
    if (ALGORITHM == "breadth"):
        nodes, goalParentId, iterations = breadthFS (charMap, args)
    elif (ALGORITHM == "depth"):
        nodes, goalParentId, iterations = depthFS (charMap, args)
    elif (ALGORITHM == "best"):
        nodes, goalParentId, iterations = bestFS (charMap, args)
    elif (ALGORITHM == "a_star"):
        nodes, goalParentId, iterations = a_estrellita (charMap, args)
    else:
        print (bcolors.BOLDRED + "Algoritmo no implementado" + bcolors.RESET)
        print (bcolors.BOLDCYAN + "Se ejecutara:" + bcolors.BOLDCYAN + " Depth First Search Algorithm" + bcolors.RESET)
        nodes, goalParentId = depthFS (charMap)

    end = time.time()
    
    goal_pared_id_aux = goalParentId
    ## Fase de regresión 
    print('%%%%%%%%%%%%%%%%%%%')
    ok = False
    while not ok:
        for node in nodes:
            if( node.myId == goal_pared_id_aux ):
                node.dump()
                goal_pared_id_aux = node.parentId
                if( goal_pared_id_aux == -2):
                    print("%%%%%%%%%%%%%%%%%2")
                    ok = True
    print( bcolors.BOLDCYAN + 'Tiempo de ejecucion: ' + bcolors.BOLDYELLOW + str (np.round ( (end - start)*1000, 4 ) ) + ' milisegundos' + bcolors.RESET )
    print( bcolors.BOLDCYAN + 'Numero de iteraciones totales: ' + bcolors.BOLDYELLOW + str ( iterations ) + bcolors.RESET )
    input ('pepe')
    if (args.viz):
        dumpPathImage (charMap, nodes, goalParentId)
    

if __name__ == '__main__':
    main()


