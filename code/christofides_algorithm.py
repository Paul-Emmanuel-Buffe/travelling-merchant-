# start
import pandas as pd
import matplotlib.pyplot as plt

# Création du dataframe
df_positions = pd.read_csv('data/villes_france_lat_long.csv')
print(df_positions)

# Affichage des points sur une carte
plt.figure(figsize=(8, 8))

# Affiche uniquement les points (visibles)
plt.scatter(df_positions['Longitude'], df_positions['Latitude'], color='blue', s=30)

# Ratio 1.45 pour préserver les proportions de la France
plt.gca().set_aspect(1.45)
plt.axis('off')

plt.show()

