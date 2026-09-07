import numpy as np
import pandas as pd
from distances import matrice_distances

def prim_arbre_couvrant(matrice):

    nombre_villes = len(matrice)

    # Etape 1 : La trace des villes vistées
    villes_visitees = [False] * nombre_villes

    # On commence par la ville 0 (initialisation)
    villes_visitees[0] = True
    nombre_villes_visitees = 1

    # liste pour stocker les arretes choisies
    routes_choisies = []
    distance_totale = 0

    # 2. On arrete quand toutes les villes sont visitées

    while nombre_villes_visitees < nombre_villes:

        distance_minimale = float('inf')
        meilleure_route = (None, None)

        for i in range(nombre_villes):
            if villes_visitees[i]:

                for j in range(nombre_villes):
                    if not villes_visitees[j]: 

                        if matrice[i][j] < distance_minimale:
                            distance_minimale = matrice[i][j]
                            meilleure_route = (i, j)


        # 4. l'annexion
        ville_depart, ville_arrivee = meilleure_route

        # ajout de meilleure route trouvée
        routes_choisies.append((ville_depart, ville_arrivee, distance_minimale))
        distance_totale += distance_minimale

        # la nouvelle ville rejoint la liste des villes visitées
        villes_visitees[ville_arrivee] = True
        nombre_villes_visitees += 1

    return routes_choisies, distance_totale


if __name__ == "__main__":
    print("Test")

    df_positions = pd.read_csv('../data/villes_france_lat_long.csv')

    matrice_test = matrice_distances(df_positions)

    routes, distance_totale = prim_arbre_couvrant(matrice_test)

    for route in routes:
        depart, arrivées, distance = route
        print(f"Route de la ville {depart} à la ville {arrivées} avec une distance de {distance}")

    print(f"Distance totale de l'arbre couvrant : {distance_totale}")

    print(prim_arbre_couvrant(matrice_test))