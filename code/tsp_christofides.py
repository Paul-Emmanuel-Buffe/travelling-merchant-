# tsp_christofides.py

import pandas as pd
import networkx as nx

from distances import matrice_distances
from prim import prim_arbre_couvrant

def road_to_graph(routes_mst):
    """ Convertit la liste des routes de l'arbre couvrant en un graphe NetworkX """

    graph = nx.Graph() # création d'un graphe non orienté vide  

    for depart, arrivee, distance in routes_mst:
        graph.add_edge(depart, arrivee, weight=distance)

    return graph

def odd_cities(graph):
    """ Retourne la liste des villes de degré impair dans le graphe """
    return[ville for ville, degree in graph.degree() if degree % 2 != 0]

def find_odd_best_couple(villes_impaires, matrice):

    temp_graph = nx.Graph()
    n =len(villes_impaires)

    for i in range(n):
        for j in range(i+1, n):
            u=villes_impaires[i]
            v=villes_impaires[j]
            temp_graph.add_edge(u, v, weight= matrice[u][v])

    return nx.min_weight_matching(temp_graph, weight='weight')

def assemblage_multigraphe(graph, couplage, matrice):

    multigraph = nx.MultiGraph(graph)

    for u, v in couplage:
        multigraph.add_edge(u, v, weight=matrice[u][v])
    return multigraph


def eulerian_circuit (multigraph, start_city = 0):
    circuit_eulerien = list(nx.eulerian_circuit(multigraph, source=start_city))

    villes_visitees = set()
    tour_final = []

    for u, _ in circuit_eulerien:
        if u not in villes_visitees:
            tour_final.append(u)
            villes_visitees.add(u)
    tour_final.append(tour_final[0])  # Retour à la ville de départ
    return tour_final

def calculer_distance_totale(tour, matrice):
    distance_totale = 0
    for i in range(len(tour) - 1):
        distance_totale += matrice[tour[i]][tour[i + 1]]
    return distance_totale

if __name__ == "__main__":
    df_positions = pd.read_csv('../data/villes_france_lat_long.csv')

    matrice_test = matrice_distances(df_positions)

    routes, distance_totale = prim_arbre_couvrant(matrice_test)

    graph = road_to_graph(routes)

    villes_impaires = odd_cities(graph)
    print("Graphe créé à partir des routes de l'arbre couvrant :")
    print(graph.edges(data=True))

    print("Villes de degré impair dans le graphe :")
    print(villes_impaires)

    print("Couplage optimal des villes de degré impair :")
    print(find_odd_best_couple(villes_impaires, matrice_test))

    print("Multigraphe après l'ajout des arêtes du couplage optimal :")
    print(assemblage_multigraphe(graph, find_odd_best_couple(villes_impaires, matrice_test), matrice_test))

    print("Circuit eulérien /TSP final:")
    print("Distance totale :")
    distance_totale = calculer_distance_totale(eulerian_circuit(assemblage_multigraphe(graph, find_odd_best_couple(villes_impaires, matrice_test), matrice_test)), matrice_test)
    print(round(distance_totale, 2))  