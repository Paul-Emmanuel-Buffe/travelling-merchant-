import matplotlib.pyplot as plt
import pandas as pd

# # Création du dataframe
# df_positions = pd.read_csv('data/villes_france_lat_long.csv')
# print(df_positions)

# # Affichage des points sur une carte
# plt.figure(figsize=(8, 8))

# # Affiche uniquement les points (visibles)
# plt.scatter(df_positions['Longitude'], df_positions['Latitude'], color='blue', s=30)

# # Ratio 1.45 pour préserver les proportions de la France
# plt.gca().set_aspect(1.45)
# plt.axis('off')

# plt.show()

def affichage_voyage(df_positions, parcours=None):
    """Affichage de la carte des villes.
    Si un parcours est fourni, trace aussi le parcours sur la carte."""

    plt.figure(figsize=(10, 10))

    plt.scatter(df_positions['Longitude'], df_positions['Latitude'], color='blue', s=30, zorder=2)

    if parcours is not None:

        longitudes_trajets = []
        latitudes_trajets = []

        for i in parcours:
            longitudes_trajets.append(df_positions.iloc[i]['Longitude'])
            latitudes_trajets.append(df_positions.iloc[i]['Latitude'])

        plt.plot(longitudes_trajets, latitudes_trajets, color='red', linewidth=2, zorder=1)

        plt.gca().set_aspect(1.45)
        plt.axis('off')

        plt.show()

if __name__ == "__main__":

    df_positions = pd.read_csv('../data/villes_france_lat_long.csv')


    parcours_exemple = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    affichage_voyage(df_positions, parcours_exemple)




