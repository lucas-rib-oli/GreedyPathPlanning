# GreedyPathPlanning
Entregable para la asignatura de Introducción a la Planificación de Robots del Máster de Robótica y Automatización (UC3M)

- Se ha implementado el algoritmo Depth First Search Algorithm como algoritmo greedy necesario para el punto de este trabajo.
- Las tareas realizadas se encuentran implementadas en un fichero .py [here](src/python/algorithms/greedy_algorithms/main_greedy.py) donde se encuentran los distintos algoritmos greedy implementados

# Extras
- Extra 1: Se ha realizado una modificación del código original (Breadth First Search) con el mismo funcionamiento, los cambios se basan en no tener tantas condiciones "if" y hacer el código más escalable a la hora de analizar la vecindad 8.
- Extra 2: Se ha añadido tanto para el algoritmo original como para los algoritmos greedy la opción de utilizar la vecindad 8 (analizar los vecinos de las esquinas). Se puede escoger vecindad 4 o vecindad 8 para cada uno de los algoritmos.
- Extra 3: Se ha implementado el algoritmo A^*
- Extra 4: Se ha implementado el algoritmo Best First Search
- Extra 5: Para los algoritmos no unitarios se puede usar dos funciones de coste, la distancia euclídea o la distancia Manhattan.
- Extra 6: Se ha modificado la impresión del mapa por consola añadiendo colores para facilitar la comprensión del mismo. 
- Extra 7: En el mapa se puede ver la posición del nodo actual que se indica con el color magenta, también los nodos libres (verde), visitados (azul) y ocupados (rojo), el punto de inicio (cian), y el punto de meta (amarillo).
- Extra 8: Se ha añadido la visualización del mapa por imagen, iteración a iteración se puede ver el progreso en imagen. 
- Extra 9: Se ha añadido la opción de pasar distintos argumentos al código (ruta, número del mapa, punto de inicio, punto de fin, algoritmo a usar, vecindad a usar, función de coste a usar, visualización por imagen).
- Extra 10: Se ha realizado un [shell script](src/bash/execute_script.sh) para ejecutar un determinado algoritmo con una determinada vecindad y una determinada función de coste sobre todos los mapas disponibles con sus respectivos posiciones de inicio y fin. Si se desea se puede modificar este script para modificar los puntos de inicio.
- Extra 11: Se ha añadido el tiempo de ejecución y el número de iteraciones a la hora de ejecutar cada algoritmo
- Extra 12: El código se ha subido a un repositorio de [github](https://github.com/lucas-rib-oli/GreedyPathPlanning)
- Extra 13: Se han realizado comparaciones del tiempo de ejecución y del número de iteraciones para cada algoritmo. Las tablas se adjuntan en este README.
- Extra 14: Se ha habilitado la posibilidad de crear un video poniento el argumento --video a 1. (Nota: viz tiene que tener valor 1)
- Extra 15: Se han grabado algunos videos [here](videos/).

Para ejecutar el código:
```
$ python main_greedy.py --root ROOT/GreedyPathPlanning/ --map 1 --start_x 2 --start_y 2 --end_x 5--end_y 5 --algorithm a_star --neighbourhood 8 --cost euclidean --viz 1 --video 0
```

Para ejecutar el shell script:
```
$ bash execute_script.sh depth 8 euclidean 1
```

## Tiempos de comparación
- Nota: Los tiempos de ejecución son calculados con una vecindad 8 y para los algoritmos no unitarios se ha usado la distancia euclídea como función de coste. Cabe destacar que si se eliminan todas las impresiones por consola claramente el tiempo de ejecución disminuiría. 
### Breadth First Search
<table><tbody>
<!-- START TABLE -->
<!-- TABLE HEADER -->
<th valign="bottom">Mapa</th>
<th valign="bottom">Tiempo de ejecución<br/>(ms)</th>
<th valign="bottom">Número de iteraciones</th>

<!-- TABLE BODY -->
<!-- ROW: Mapa 1 -->
 <tr><td align="left"><a href="map1/">1</a></td>
<td align="center">3.01</td>
<td align="center">28</td>
</tr>
<!-- ROW: Mapa 2 -->
 <tr><td align="left"><a href="map2/">2</a></td>
<td align="center">13.75</td>
<td align="center">62</td>
</tr>

<!-- ROW: Mapa 3 -->
 <tr><td align="left"><a href="map3/">3</a></td>
<td align="center">145.98</td>
<td align="center">251</td>
</tr>

<!-- ROW: Mapa 4 -->
 <tr><td align="left"><a href="map4/">4</a></td>
<td align="center">215.25</td>
<td align="center">320</td>
</tr>

<!-- ROW: Mapa 5 -->
 <tr><td align="left"><a href="map5/">5</a></td>
<td align="center">364.29</td>
<td align="center">409</td>
</tr>

<!-- ROW: Mapa 6 -->
 <tr><td align="left"><a href="map6/">6</a></td>
<td align="center">55.24</td>
<td align="center">170</td>
</tr>

<!-- ROW: Mapa 7 -->
 <tr><td align="left"><a href="map7/">7</a></td>
<td align="center">363.71</td>
<td align="center">411</td>
</tr>

<!-- ROW: Mapa 8 -->
 <tr><td align="left"><a href="map8/">8</a></td>
<td align="center">56.07</td>
<td align="center">176</td>
</tr>

<!-- ROW: Mapa 9 -->
 <tr><td align="left"><a href="map9/">9</a></td>
<td align="center">420.94</td>
<td align="center">449</td>
</tr>

<!-- ROW: Mapa 10 -->
 <tr><td align="left"><a href="map10/">10</a></td>
<td align="center">835.63</td>
<td align="center">647</td>
</tr>

<!-- ROW: Mapa 11 -->
 <tr><td align="left"><a href="map11/">11</a></td>
<td align="center">632.38</td>
<td align="center">492</td>
</tr>
</tbody></table>


### Depth First Search Algorithm
<table><tbody>
<!-- START TABLE -->
<!-- TABLE HEADER -->
<th valign="bottom">Mapa</th>
<th valign="bottom">Tiempo de ejecución<br/>(ms)</th>
<th valign="bottom">Número de iteraciones</th>

<!-- TABLE BODY -->
<!-- ROW: Mapa 1 -->
 <tr><td align="left"><a href="map1/">1</a></td>
<td align="center">1.05</td>
<td align="center">9</td>
</tr>
<!-- ROW: Mapa 2 -->
 <tr><td align="left"><a href="map2/">2</a></td>
<td align="center">6.99</td>
<td align="center">23</td>
</tr>

<!-- ROW: Mapa 3 -->
 <tr><td align="left"><a href="map3/">3</a></td>
<td align="center">88.33</td>
<td align="center">157</td>
</tr>

<!-- ROW: Mapa 4 -->
 <tr><td align="left"><a href="map4/">4</a></td>
<td align="center">58.28</td>
<td align="center">108</td>
</tr>

<!-- ROW: Mapa 5 -->
 <tr><td align="left"><a href="map5/">5</a></td>
<td align="center">54.79</td>
<td align="center">82</td>
</tr>

<!-- ROW: Mapa 6 -->
 <tr><td align="left"><a href="map6/">6</a></td>
<td align="center">16.19</td>
<td align="center">43</td>
</tr>

<!-- ROW: Mapa 7 -->
 <tr><td align="left"><a href="map7/">7</a></td>
<td align="center">188.68</td>
<td align="center">201</td>
</tr>

<!-- ROW: Mapa 8 -->
 <tr><td align="left"><a href="map8/">8</a></td>
<td align="center">37.67</td>
<td align="center">99</td>
</tr>

<!-- ROW: Mapa 9 -->
 <tr><td align="left"><a href="map9/">9</a></td>
<td align="center">304.71</td>
<td align="center">308</td>
</tr>

<!-- ROW: Mapa 10 -->
 <tr><td align="left"><a href="map10/">10</a></td>
<td align="center">136.48</td>
<td align="center">103</td>
</tr>

<!-- ROW: Mapa 11 -->
 <tr><td align="left"><a href="map11/">11</a></td>
<td align="center">43.69</td>
<td align="center">43</td>
</tr>
</tbody></table>


### Best First Search Algorithm
<table><tbody>
<!-- START TABLE -->
<!-- TABLE HEADER -->
<th valign="bottom">Mapa</th>
<th valign="bottom">Tiempo de ejecución<br/>(ms)</th>
<th valign="bottom">Número de iteraciones</th>

<!-- TABLE BODY -->
<!-- ROW: Mapa 1 -->
 <tr><td align="left"><a href="map1/">1</a></td>
<td align="center">1.95</td>
<td align="center">6</td>
</tr>
<!-- ROW: Mapa 2 -->
 <tr><td align="left"><a href="map2/">2</a></td>
<td align="center">2.39</td>
<td align="center">13</td>
</tr>

<!-- ROW: Mapa 3 -->
 <tr><td align="left"><a href="map3/">3</a></td>
<td align="center">49.67</td>
<td align="center">102</td>
</tr>

<!-- ROW: Mapa 4 -->
 <tr><td align="left"><a href="map4/">4</a></td>
<td align="center">146.25</td>
<td align="center">209</td>
</tr>

<!-- ROW: Mapa 5 -->
 <tr><td align="left"><a href="map5/">5</a></td>
<td align="center">145.90</td>
<td align="center">164</td>
</tr>

<!-- ROW: Mapa 6 -->
 <tr><td align="left"><a href="map6/">6</a></td>
<td align="center">19.89</td>
<td align="center">59</td>
</tr>

<!-- ROW: Mapa 7 -->
 <tr><td align="left"><a href="map7/">7</a></td>
<td align="center">139.67</td>
<td align="center">140</td>
</tr>

<!-- ROW: Mapa 8 -->
 <tr><td align="left"><a href="map8/">8</a></td>
<td align="center">8.51</td>
<td align="center">30</td>
</tr>

<!-- ROW: Mapa 9 -->
 <tr><td align="left"><a href="map9/">9</a></td>
<td align="center">48.97</td>
<td align="center">68</td>
</tr>

<!-- ROW: Mapa 10 -->
 <tr><td align="left"><a href="map10/">10</a></td>
<td align="center">310.38</td>
<td align="center">244</td>
</tr>

<!-- ROW: Mapa 11 -->
 <tr><td align="left"><a href="map11/">11</a></td>
<td align="center">210</td>
<td align="center">174</td>
</tr>
</tbody></table>


### A Star Algorithm
<table><tbody>
<!-- START TABLE -->
<!-- TABLE HEADER -->
<th valign="bottom">Mapa</th>
<th valign="bottom">Tiempo de ejecución<br/>(ms)</th>
<th valign="bottom">Número de iteraciones</th>

<!-- TABLE BODY -->
<!-- ROW: Mapa 1 -->
 <tr><td align="left"><a href="map1/">1</a></td>
<td align="center">1.663</td>
<td align="center">9</td>
</tr>
<!-- ROW: Mapa 2 -->
 <tr><td align="left"><a href="map2/">2</a></td>
<td align="center">5.794</td>
<td align="center">31</td>
</tr>

<!-- ROW: Mapa 3 -->
 <tr><td align="left"><a href="map3/">3</a></td>
<td align="center">136.56</td>
<td align="center">202</td>
</tr>

<!-- ROW: Mapa 4 -->
 <tr><td align="left"><a href="map4/">4</a></td>
<td align="center">202.51</td>
<td align="center">285</td>
</tr>

<!-- ROW: Mapa 5 -->
 <tr><td align="left"><a href="map5/">5</a></td>
<td align="center">250.91</td>
<td align="center">274</td>
</tr>

<!-- ROW: Mapa 6 -->
 <tr><td align="left"><a href="map6/">6</a></td>
<td align="center">45.76</td>
<td align="center">89</td>
</tr>

<!-- ROW: Mapa 7 -->
 <tr><td align="left"><a href="map7/">7</a></td>
<td align="center">291.70</td>
<td align="center">309</td>
</tr>

<!-- ROW: Mapa 8 -->
 <tr><td align="left"><a href="map8/">8</a></td>
<td align="center">45.92</td>
<td align="center">118</td>
</tr>

<!-- ROW: Mapa 9 -->
 <tr><td align="left"><a href="map9/">9</a></td>
<td align="center">151</td>
<td align="center">164</td>
</tr>

<!-- ROW: Mapa 10 -->
 <tr><td align="left"><a href="map10/">10</a></td>
<td align="center">468.77</td>
<td align="center">356</td>
</tr>

<!-- ROW: Mapa 11 -->
 <tr><td align="left"><a href="map11/">11</a></td>
<td align="center">373.09</td>
<td align="center">239</td>
</tr>
</tbody></table>