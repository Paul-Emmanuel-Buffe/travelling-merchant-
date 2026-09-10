import matplotlib.pyplot as plt
import pandas as pd

def affichage_voyage(df_positions, parcours=None):
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

def afficher_multigraphe(df_positions, routes_mst, paires):
    plt.figure(figsize=(10, 10))
    plt.scatter(df_positions['Longitude'], df_positions['Latitude'], color='blue', s=30, zorder=3)

    if routes_mst is not None:
        for depart, arrivee, _ in routes_mst:
            x_coords = [df_positions.iloc[depart]['Longitude'], df_positions.iloc[arrivee]['Longitude']]
            y_coords = [df_positions.iloc[depart]['Latitude'], df_positions.iloc[arrivee]['Latitude']]
            plt.plot(x_coords, y_coords, color='green', linewidth=1.5, zorder=1)

    if paires is not None:
        for u, v in paires:
            x_coords = [df_positions.iloc[u]['Longitude'], df_positions.iloc[v]['Longitude']]
            y_coords = [df_positions.iloc[u]['Latitude'], df_positions.iloc[v]['Latitude']]
            plt.plot(x_coords, y_coords, color='orange', linestyle='--', linewidth=2.5, zorder=2)

    plt.gca().set_aspect(1.45)
    plt.axis('off')
    plt.show()

def afficher_mst(df_positions, routes=None):
    plt.figure(figsize=(10, 10))
    plt.scatter(df_positions['Longitude'], df_positions['Latitude'], color='blue', s=30, zorder=2)

    if routes is not None:
        for depart, arrivee, _ in routes:
            x_coords = [df_positions.iloc[depart]['Longitude'], df_positions.iloc[arrivee]['Longitude']]
            y_coords = [df_positions.iloc[depart]['Latitude'], df_positions.iloc[arrivee]['Latitude']]
            plt.plot(x_coords, y_coords, color='green', linewidth=1.5, zorder=1)

    plt.gca().set_aspect(1.45)
    plt.axis('off')
    plt.show()