# Main: Orchestration du programme pour résoudre le problème du voyageur de commerce (TSP) en utilisant l'algorithme de Christofides et un algorithme génétique.
import pandas as pd
from affichage import affichage_voyage
from distances import matrice_distances
from prim import prim_arbre_couvrant
from tsp_christofides import (
    assemblage_multigraphe,
    calculer_distance_totale,
    eulerian_circuit,
    find_odd_best_couple,
    odd_cities,
    road_to_graph,
)


def main(df_positions):

    matrice = matrice_distances(df_positions)
    routes_mst, _ = prim_arbre_couvrant(matrice)
    graph = road_to_graph(routes_mst)

    impaires = odd_cities(graph)
    paires = find_odd_best_couple(impaires, matrice)

    multigraph = assemblage_multigraphe(graph, paires, matrice)

    circuit = eulerian_circuit(multigraph)

    distance_totale = round(calculer_distance_totale(circuit, matrice), 2)

    return circuit, distance_totale


if __name__ == "__main__":
    # Chargement des positions des villes depuis le fichier CSV
    df_positions = pd.read_csv('../data/villes_france_lat_long.csv')

    # Calcul du parcours optimal et de la distance totale
    parcours_christofides, distance_totale = main(df_positions)

    # Affichage du parcours sur la carte
    affichage_voyage(df_positions, parcours_christofides)

    print(f"Distance totale du parcours : {distance_totale} km")