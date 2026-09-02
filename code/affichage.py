import matplotlib.pyplot as plt

# Affichage des points sur une carte
plt.figure(figsize=(8, 8))

# Affiche uniquement les points (visibles)
plt.scatter(df_positions['Longitude'], df_positions['Latitude'], color='blue', s=30)

# Ratio 1.45 pour préserver les proportions de la France
plt.gca().set_aspect(1.45)
plt.axis('off')

plt.show()