import pandas as pd
from affichage import affichage_voyage, afficher_mst, afficher_multigraphe
from complexity import evaluer_complexite
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
    routes_mst, distance_mst = prim_arbre_couvrant(matrice)
    graph = road_to_graph(routes_mst)

    impaires = odd_cities(graph)
    paires = find_odd_best_couple(impaires, matrice)

    multigraph = assemblage_multigraphe(graph, paires, matrice)
    circuit = eulerian_circuit(multigraph)
    distance_totale = round(calculer_distance_totale(circuit, matrice), 2)

    # On retourne également "paires" pour pouvoir les dessiner
    return circuit, distance_totale, routes_mst, round(distance_mst, 2), paires


if __name__ == "__main__":
    df_positions = pd.read_csv('../data/villes_france_lat_long.csv')

    # Exécution standard
    parcours_christofides, distance_totale, routes_mst, distance_mst, paires = main(df_positions)

    # Graphique 1 : Prim (Vert)
    afficher_mst(df_positions, routes_mst)
    print(f"Distance totale du MST (Prim) : {distance_mst} km")

    # Graphique 2 : L'intermédiaire de Christofides (Vert + Orange)
    afficher_multigraphe(df_positions, routes_mst, paires)
    print("Couplage des villes de degré impair généré.")

    # Graphique 3 : Le circuit final (Rouge)
    affichage_voyage(df_positions, parcours_christofides)
    print(f"Distance totale du parcours (Christofides) : {distance_totale} km")

    # Lancement de l'évaluation de complexité
    evaluer_complexite(df_positions, main)