# GreedyPathPlanning
Entregable para la asignatura de Introducción a la Planificación de Robots del Máster de Róbitica y Automatización (UC3M)

- Se ha implementado el algoritmo Depth First Search Algorithm como algoritmo greedy necesario para el punto de este trabajo.
- Las tareas realizadas se encuentran implementadas en un fichero .py en la ruta (src/python/greedy_algorithms.py) donde se encuentran los distintos algoritmos greedy implementados

# Extras
- Extra 1: Se ha realizado una modificación del código original (Breadth First Search) con el mismo funcionamiento, los cambios se basan en no tener tantas condiciones "if" y hacer el código más escalable a la hora de analizar la vecindad 8.
- Extra 2: Se ha añadido tanto para el algoritmo original como para los algoritmos greedy la opción de utilizar la vecindad 8 (analizar los vecinos de las esquinas). Se puede escoger vecindad 4 o vecindad 8 para cada uno de los algoritmos.
- Extra 3: Se ha implementado el algoritmo A^*
- Extra 4: Se ha implementado el algoritmo Best First Search
- Extra 4: Para los algoritmos no unitarios se puede usar dos funciones de coste, la distancia euclidea o la distancia Manhattan.
- Extra 5: Se ha modificado la impresión del mapa por consola añadiendo colores para facilitar la comprensión del mismo. 
- Extra 6: En el mapa se puede ver la posición del nodo actual que se indica con el color magenta, también los nodos libres (verde), visitados (azul) y ocupados (rojo); el punto de inicio (cian) y punto de meta (amarillo).
- Extra 7: Se añadido la visualización del mapa por imagen, iteración a iteración se puede ver el progreso en imagen. 
- Extra 8: Se ha añadido la opción de pasar distintos argumentos al código (ruta, número del mapa, punto de inicio, punto de fin, algoritmo a usar, vecindad a usar, función de coste a usar, visualización por imagen).
- Extra 9: Se ha realizado un shell script para ejecutar un determinado algoritmo con una determinada vecindad y una determinada funciónde coste sobre todos los mapas disponibles con sus respectivos posiciones de inicio y fin. Si se desea se puede modificar este script para modificar los puntos de inicio. (RUTA AL SHELL SCRIPT)
- Extra : Se ha añadido el tiempo de ejecución y el número de iteraciones a la hora de ejecutar cada algoritmo
- Extra 10: El código se ha subido a repositoria de github
