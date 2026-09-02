# Code python pourle calcul de la distance entre deux points géographiques (latitude et longitude) en utilisant la formule de Haversine
import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    """ Calcule de la distance entre deux points GPS"""
    R = 6371

    phi1=np.radians(lat1)
    phi2=np.radians(lat2)
    lambda1=np.radians(lon1)
    lambda2=np.radians(lon2)    

    delta_phi = phi2 - phi1
    delta_lambda = lambda2 - lambda1

    a = np.sin(delta_phi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda/2)**2
    distance = 2 * R * np.arcsin(np.sqrt(a))

    return distance

def matrice_distances(df_positions):
    """ Prend le DataFrame des villes en entrée et retourne une matrice 
    contenant les distances entre chaque paire de villes (poids des arrêtes du MST)
    """

    nombre_villes = len(df_positions)

    matrice_distances = np.zeros((nombre_villes, nombre_villes))

    # Boucle de calcul des distances
    for i in range(nombre_villes):
        for j in range(nombre_villes):
            if i != j:
                lat1, lon1 =df_positions.iloc[i]['Latitude'], df_positions.iloc[i]['Longitude']
                lat2, lon2 = df_positions.iloc[j]['Latitude'], df_positions.iloc[j]['Longitude']
                matrice_distances[i][j] = haversine(lat1, lon1, lat2, lon2)
    return matrice_distances


if __name__ == "__main__":

    df_positions = pd.read_csv('../data/villes_france_lat_long.csv')
    matrice_distances = matrice_distances(df_positions)
    print(matrice_distances)
