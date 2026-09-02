# Main: Orchestration du programme pour résoudre le problème du voyageur de commerce (TSP) en utilisant l'algorithme de Christofides et un algorithme génétique.
import pandas as pd
from distances import matrice_distances

df_positions = pd.read_csv('../data/villes_france_lat_long.csv')
matrice_distances = matrice_distances(df_positions)
print(matrice_distances)

