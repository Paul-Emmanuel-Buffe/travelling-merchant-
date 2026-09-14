import random
import math
import matplotlib.pyplot as plt
import csv
from math import radians, sin, cos, asin, sqrt
"""
Algorithme génétique — résolution du TSP de Théobald (20 villes)
==================================================================

Représentation :
    Un individu est une permutation des indices des 20 villes, représentant
    l'ordre de visite du parcours (le retour à la ville de départ est
    implicite et ajouté lors du calcul de la distance).

Fonction d'évaluation :
    La distance totale d'un individu est la somme des distances de Haversine
    entre villes consécutives, plus la distance de retour au point de départ.
    Le fitness est l'inverse de cette distance (1 / distance_totale) :
    plus le parcours est court, plus le fitness est élevé.

Population initiale :
    Générée aléatoirement — un ensemble de permutations tirées au hasard.

Sélection :
    Par tournoi (k individus tirés au hasard, le meilleur des k est retenu),
    pour équilibrer pression de sélection et diversité de la population.

Croisement :
    Croisement par ordre (OX, Order Crossover) : un segment est copié tel
    quel depuis le premier parent, le reste est complété avec les villes du
    second parent dans leur ordre d'apparition — garantit que chaque enfant
    reste une permutation valide (chaque ville visitée une seule fois).

Mutation :
    Échange (swap) de deux villes tirées au hasard dans le parcours, appliqué
    avec un faible taux de mutation, pour maintenir la diversité génétique
    sans détruire les bonnes solutions déjà trouvées.

Élitisme :
    Les meilleurs individus d'une génération sont copiés tels quels dans la
    génération suivante, garantissant que la meilleure solution trouvée
    n'est jamais perdue.

Critère d'arrêt :
    Nombre fixe de générations atteint, ou absence d'amélioration du meilleur
    individu pendant un nombre défini de générations consécutives.

Paramètres réglables :
    taille de la population, taux de mutation, taille du tournoi de
    sélection, taille de l'élite, nombre de générations.
"""

def charger_villes(fichier_csv):
    noms = []
    coord=[]
    with open(fichier_csv, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            noms.append(row["Ville"])
            coord.append((float(row["Latitude"]), float(row["Longitude"])))
    return noms, coord
# 1. Definition d'un individu: une permutation des villes
def creer_individu(villes):
    individu = list(range(len(villes)))
    random.shuffle(individu)
    return individu


# 2. Definition de lapopulation : un ensemble d'individus(de parcours)
def creer_population(villes, taille_population):
    return [creer_individu(villes) for _ in range(taille_population)]
# 3. Definition de la fonction de fitness : la distance totale du parcours



RAYON_TERRE_KM = 6371

def distance_haversine(lat1, lon1, lat2, lon2):
    """Distance à vol d'oiseau (km) entre deux points, coordonnées en degrés."""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    return 2 * RAYON_TERRE_KM * asin(sqrt(a))

def construire_matrice_distances(villes):
    """villes : liste de tuples (latitude, longitude).
    Retourne une matrice n x n des distances de Haversine (km)."""
    n = len(villes)
    matrice = [[0.0] * n for _ in range(n)]

    for i in range(n):
        lat1, lon1 = villes[i]
        for j in range(i + 1, n):          # symétrie : on ne calcule qu'une fois par paire
            lat2, lon2 = villes[j]
            d = distance_haversine(lat1, lon1, lat2, lon2)
            matrice[i][j] = d
            matrice[j][i] = d               # on recopie en miroir
    return matrice


def distance_totale(individu, matrice_distances):
    """individu : liste d'indices de villes (une permutation)."""
    n = len(individu)
    somme = 0.0
    for i in range(n - 1):
        somme += matrice_distances[individu[i]][individu[i + 1]]
    somme += matrice_distances[individu[-1]][individu[0]]   # retour au point de départ
    return somme


def fitness(individu, matrice_distances):
    return 1 / distance_totale(individu, matrice_distances)

# 4. Definition de la fonction de selection : selectionner les meilleurs individus pour la reproduction

def selection_tournoi(population, matrice_distances, k=5):
    """Sélectionne un individu par tournoi : k candidats tirés au hasard,
    on retourne celui de plus petite distance totale."""
    candidats = random.sample(population, k=5)
    return min(candidats, key=lambda individu: distance_totale(individu, matrice_distances))

# 5. Definition de la fonction de croisement : combiner deux individus pour créer un nouvel individu

def croisement_ox(parent1, parent2):
    """Croisement par ordre (OX) : copie un segment du parent1,
    complète le reste avec les villes du parent2 dans leur ordre d'apparition."""
    n = len(parent1)
    i, j = sorted(random.sample(range(n), 2))   # deux points de coupe, i < j

    enfant = [None] * n
    enfant[i:j] = parent1[i:j]                   # segment copié tel quel

    position = j
    for k in range(n):
        ville = parent2[(j + k) % n]
        if ville not in enfant:
            enfant[position % n] = ville
            position += 1

    return enfant

# 6. Definition de la fonction de mutation : modifier un individu pour introduire de la diversité
def mutation_swap(individu, taux_mutation):
    """Échange deux villes au hasard avec une probabilité de mutation."""
    if random.random() < taux_mutation:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu

# 7. Definition de la fonction d'algorithme genetique : iterer sur plusieurs generations pour trouver le meilleur individu
def algorithme_genetique(villes, matrice_distances, taille_population=100, generations=1000, taux_mutation=0.1):
    population = creer_population(villes, taille_population)
    meilleur_individu = min(population, key=lambda ind: distance_totale(ind, matrice_distances))
    meilleure_distance = distance_totale(meilleur_individu, matrice_distances)
    historique_distances = [meilleure_distance]  # AJOUT : suivi de la meilleure distance à chaque génération (pour la courbe de convergence)

    for generation in range(generations):
        nouvelle_population = []

        # Élitisme : on garde le meilleur individu
        nouvelle_population.append(meilleur_individu)

        while len(nouvelle_population) < taille_population:
            parent1 = selection_tournoi(population, matrice_distances)
            parent2 = selection_tournoi(population, matrice_distances)
            enfant = croisement_ox(parent1, parent2)
            enfant = mutation_swap(enfant, taux_mutation)
            nouvelle_population.append(enfant)

        population = nouvelle_population

        # AJOUT : mise à jour du meilleur individu trouvé jusqu'ici + suivi pour la courbe de convergence
        meilleur_de_la_generation = min(population, key=lambda ind: distance_totale(ind, matrice_distances))
        distance_de_la_generation = distance_totale(meilleur_de_la_generation, matrice_distances)
        if distance_de_la_generation < meilleure_distance:
            meilleur_individu = meilleur_de_la_generation
            meilleure_distance = distance_de_la_generation
        historique_distances.append(meilleure_distance)

    return meilleur_individu, meilleure_distance, historique_distances

# 8. AJOUT — Affichage du parcours sous forme de carte
def tracer_parcours(individu, noms_villes, coord_villes, titre="Meilleur parcours trouvé", afficher=True):
    """Affiche les villes reliées entre elles dans l'ordre de visite du parcours
    (longitude en abscisse, latitude en ordonnée), avec retour à la ville de départ."""
    lats = [coord_villes[i][0] for i in individu] + [coord_villes[individu[0]][0]]
    lons = [coord_villes[i][1] for i in individu] + [coord_villes[individu[0]][1]]

    plt.figure(figsize=(10, 8))
    plt.plot(lons, lats, 'o-', color='tab:blue', markersize=8, linewidth=1.5, zorder=1)

    # Numéroter l'ordre de visite et afficher le nom de chaque ville
    for ordre, i in enumerate(individu):
        lat, lon = coord_villes[i]
        plt.annotate(f"{ordre + 1}. {noms_villes[i]}", (lon, lat),
                     textcoords="offset points", xytext=(6, 6), fontsize=8)

    # Marquer le point de départ / arrivée
    lat_depart, lon_depart = coord_villes[individu[0]]
    plt.plot(lon_depart, lat_depart, 'o', color='tab:red', markersize=12, zorder=2, label="Départ / arrivée")

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(titre)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("parcours.png", dpi=150)
    if afficher:
        plt.show()


# 9. AJOUT — Affichage de la courbe de convergence
def generation_convergence(historique_distances):
    """Retourne le numéro de la génération à partir de laquelle la meilleure
    distance finale est atteinte (= la dernière génération où le parcours
    s'est encore amélioré)."""
    distance_finale = historique_distances[-1]
    for generation, distance in enumerate(historique_distances):
        if distance == distance_finale:
            return generation
    return len(historique_distances) - 1


def tracer_convergence(historique_distances, titre="Courbe de convergence", afficher=True):
    """Affiche l'évolution de la meilleure distance trouvée au fil des générations,
    et indique la génération à partir de laquelle l'algorithme a convergé
    (ligne rouge + numéro affiché directement sur l'axe des générations)."""
    gen_convergence = generation_convergence(historique_distances)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(historique_distances, color='tab:green', linewidth=1.5)
    ax.axvline(gen_convergence, color='tab:red', linestyle='--', linewidth=1,
               label=f"Convergence à la génération {gen_convergence}")

    # Ajoute le numéro de la génération de convergence comme graduation sur l'axe des x
    ticks = sorted(set(list(ax.get_xticks()) + [gen_convergence]))
    ticks = [t for t in ticks if 0 <= t <= len(historique_distances) - 1]
    ax.set_xticks(ticks)
    for tick, label in zip(ticks, ax.get_xticklabels()):
        if tick == gen_convergence:
            label.set_color('tab:red')
            label.set_fontweight('bold')

    ax.set_xlabel("Génération")
    ax.set_ylabel("Meilleure distance (km)")
    ax.set_title(titre)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("convergence.png", dpi=150)
    if afficher:
        plt.show()

    print(f"Convergence atteinte à la génération {gen_convergence} "
          f"(sur {len(historique_distances) - 1} générations), "
          f"distance finale : {historique_distances[-1]:.2f} km")

    return gen_convergence


if __name__ == "__main__":
    # Exemple d'utilisation avec un fichier CSV contenant les villes et leurs coordonnées
    noms_villes, coord_villes = charger_villes("villes_france_lat_long.csv")
    matrice_distances = construire_matrice_distances(coord_villes)

    meilleur_individu, meilleure_distance, historique_distances = algorithme_genetique(coord_villes, matrice_distances)
    print(f"Meilleur parcours trouvé : {meilleur_individu} avec une distance totale de {meilleure_distance:.2f} km")
    print("Ordre des villes :", [noms_villes[i] for i in meilleur_individu])

    # AJOUT : génération des deux graphiques, enregistrés en PNG dans le dossier courant
    # (parcours.png, convergence.png) SANS les afficher dans une fenêtre — plt.show() est
    # bloquant (le script attend que tu fermes la fenêtre à la main pour continuer), donc on
    # l'évite complètement ici : ouvre simplement les fichiers PNG depuis l'explorateur de
    # fichiers une fois le script terminé.
    tracer_parcours(meilleur_individu, noms_villes, coord_villes, afficher=False)
    tracer_convergence(historique_distances, afficher=False)
    print("Graphiques enregistrés dans le dossier courant : parcours.png, convergence.png")
