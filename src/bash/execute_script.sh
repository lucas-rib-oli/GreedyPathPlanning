#!/bin/bash
# ======================================================================== #
# Comprobar si el número de parametros de entradas  es el correcto
if [ "$#" -lt 4 ]; then
    echo "Numero ilegal de parametros"
	echo "Se precisa: algorithm (breadth / depth / best / a_star) / neighbourhood (4 or 8) / cost (euclidean or manhattan) / viz (0 or 1)"
    exit
fi
# Example: bash execute_script.sh a_star 8 euclidean 0
# ======================================================================== #

# ======================================================================== #

declare -a array_start_x=(2 2 4 4 3 2 3 2 3 3 3) # Array con los puntos de inicio de la coordenada X en orden del mapa
declare -a array_start_y=(2 2 10 14 15 2 9 2 9 9 15) # Array con los puntos de inicio de la coordenada Y en orden del mapa

# Ejemplo: array_start_x[0] y array_start_y[0] --> Punto de inicio: X = 2, Y = 2

declare -a array_end_x=(7 10 4 4 3 10 3 10 3 3 3) # Array con los puntos de meta de la coordenada X en orden del mapa
declare -a array_end_y=(2 7 14 10 9 17 15 17 15 15 9) # Array con los puntos de meta de la coordenada Y en orden del mapa

cd ..
cd ..
root=`pwd` # Ruta padre de los mapas
cd src/python/algorithms/greedy_algorithms

algorithm=$1 # breadth / depth / best / a_star
neighbourhood=$2 # 4 / 8
cost=$3 # euclidean / manhattan
viz=$4
pwd
# for t in ${array_start_x[@]}; do
# 	echo "${array_start_x[9]}"
# done

for map in 1 2 3 4 5 6 7 8 9 10 11 
do
	python main_greedy.py --root ${root} --map ${map} --start_x ${array_start_x[$map-1]} --start_y ${array_start_y[$map-1]} --end_x ${array_end_x[$map-1]} --end_y ${array_end_y[$map-1]} --algorithm ${algorithm} --neighbourhood ${neighbourhood} --cost ${cost} --viz ${viz}
done
exit;
