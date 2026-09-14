import time
import matplotlib.pyplot as plt

# Réutilise le code de base (chargement des villes, matrice de distances,
# algorithme génétique) défini dans algo_genetique_tsp.py — ce fichier ne
# contient que la partie "complexité théorique" et "comparaison des paramètres".
from algo_genetique_tsp import charger_villes, construire_matrice_distances, algorithme_genetique


# 10. AJOUT — Courbe de complexité théorique : Christofides vs Algorithme génétique
def tracer_courbe_complexite(n_max=1000, n_projet=20,
                              combos_ga=((50, 100), (150, 500), (400, 2000)),
                              titre="Complexité théorique : Christofides vs Algorithme génétique",
                              afficher=True):
    """Compare le nombre d'opérations théoriques de Christofides (O(n^3)) à celui de
    l'algorithme génétique (O(g x p x n)) en fonction du nombre de villes n, pour
    plusieurs combinaisons (taille de population p, nombre de générations g) issues
    de la table des paramètres à tester. Échelle log-log pour rendre lisible le point
    de croisement entre les deux courbes (Christofides finit toujours par dépasser le
    GA puisqu'il croît en n^3 contre n pour le GA, mais pour un n aussi petit que celui
    du projet, c'est le GA qui reste le plus coûteux à cause du facteur g x p)."""
    n_valeurs = list(range(2, n_max + 1))

    fig, ax = plt.subplots(figsize=(10, 7))

    # Christofides : O(n^3)
    christofides = [n ** 3 for n in n_valeurs]
    ax.plot(n_valeurs, christofides, color='tab:blue', linewidth=2, label="Christofides — O(n³)")

    # Algorithme génétique : O(g x p x n), pour chaque combinaison de paramètres à tester
    couleurs = ['tab:orange', 'tab:green', 'tab:red']
    for (p, g), couleur in zip(combos_ga, couleurs):
        ga = [g * p * n for n in n_valeurs]
        ax.plot(n_valeurs, ga, color=couleur, linewidth=1.5, linestyle='--',
                label=f"Algo génétique — O(g×p×n), p={p}, g={g}")

        # Croisement théorique n³ = g×p×n  =>  n = √(g×p)
        n_croisement = (g * p) ** 0.5
        if n_croisement <= n_max:
            ax.axvline(n_croisement, color=couleur, linestyle=':', linewidth=1, alpha=0.5)

    # Repère : le nombre de villes du projet
    ax.axvline(n_projet, color='black', linewidth=1.2, label=f"Projet — n = {n_projet} villes")

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel("Nombre de villes (n)")
    ax.set_ylabel("Nombre d'opérations théoriques")
    ax.set_title(titre)
    ax.legend(fontsize=8)
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig("complexite.png", dpi=150)
    if afficher:
        plt.show()

    print(f"À n = {n_projet} villes (taille du projet) :")
    print(f"  Christofides (n³)                 : {n_projet ** 3:,} opérations".replace(",", " "))
    for p, g in combos_ga:
        n_croisement = round((g * p) ** 0.5)
        print(f"  Algo génétique (p={p}, g={g})".ljust(37) +
              f": {g * p * n_projet:,} opérations".replace(",", " ") +
              f"  (rejoint Christofides vers n ≈ {n_croisement})")


# 11. AJOUT — Comparaison des meilleurs parcours obtenus selon les paramètres du GA
def comparer_parametres(coord_villes, matrice_distances,
                         combos_ga=((50, 100), (150, 500), (400, 2000)),
                         taux_mutation=0.1, repetitions=3,
                         titre="Comparaison des meilleurs parcours selon les paramètres"):
    """Exécute l'algorithme génétique plusieurs fois pour chaque combinaison de paramètres
    (taille de population p, nombre de générations g), pour comparer la distance moyenne,
    l'écart-type et le temps d'exécution moyen obtenus par combinaison — reprend la méthode :
    changer un seul paramètre à la fois et répéter chaque configuration plusieurs fois pour
    ne pas comparer sur la base d'un seul tirage aléatoire.

    ATTENTION : chaque combinaison est exécutée `repetitions` fois. Les grandes combinaisons
    (population et générations élevées, ex. p=400, g=2000) peuvent prendre plusieurs dizaines
    de secondes par répétition — le script affiche sa progression pour que tu voies qu'il
    tourne toujours (pas besoin d'interrompre s'il n'y a pas d'affichage pendant un moment)."""
    resultats = []

    for p, g in combos_ga:
        distances, temps = [], []
        for rep in range(repetitions):
            print(f"  → p={p}, g={g} — répétition {rep + 1}/{repetitions}...", end=" ", flush=True)
            debut = time.perf_counter()
            _, distance, _ = algorithme_genetique(coord_villes, matrice_distances,
                                                    taille_population=p, generations=g,
                                                    taux_mutation=taux_mutation)
            duree = time.perf_counter() - debut
            distances.append(distance)
            temps.append(duree)
            print(f"{distance:.2f} km en {duree:.1f} s")

        moyenne = sum(distances) / len(distances)
        ecart_type = (sum((d - moyenne) ** 2 for d in distances) / len(distances)) ** 0.5
        temps_moyen = sum(temps) / len(temps)
        resultats.append({"p": p, "g": g, "distances": distances, "moyenne": moyenne,
                           "ecart_type": ecart_type, "meilleure": min(distances),
                           "temps_moyen": temps_moyen})
        print(f"  Résumé p={p}, g={g} : moyenne = {moyenne:.2f} km (écart-type {ecart_type:.2f}), "
              f"meilleure = {min(distances):.2f} km, temps moyen = {temps_moyen:.1f} s\n")

    # Graphique : distance moyenne (+/- écart-type) et temps moyen, par combinaison
    labels = [f"p={r['p']}, g={r['g']}" for r in resultats]
    couleurs = ['tab:green', 'tab:orange', 'tab:red', 'tab:purple', 'tab:brown'][:len(resultats)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    barres1 = ax1.bar(labels, [r["moyenne"] for r in resultats],
                       yerr=[r["ecart_type"] for r in resultats], capsize=6, color=couleurs)
    for barre, r in zip(barres1, resultats):
        ax1.text(barre.get_x() + barre.get_width() / 2, barre.get_height() + r["ecart_type"] + 0.5,
                  f"{r['moyenne']:.1f} km", ha='center', fontsize=9)
    ax1.set_ylabel("Distance moyenne du meilleur parcours (km)")
    ax1.set_title("Distance obtenue (moyenne ± écart-type)")
    ax1.grid(True, axis='y', alpha=0.3)
    ax1.tick_params(axis='x', rotation=15)

    barres2 = ax2.bar(labels, [r["temps_moyen"] for r in resultats], color=couleurs)
    for barre, r in zip(barres2, resultats):
        ax2.text(barre.get_x() + barre.get_width() / 2, barre.get_height(),
                  f"{r['temps_moyen']:.1f} s", ha='center', va='bottom', fontsize=9)
    ax2.set_ylabel("Temps d'exécution moyen (s)")
    ax2.set_title("Temps d'exécution")
    ax2.grid(True, axis='y', alpha=0.3)
    ax2.tick_params(axis='x', rotation=15)

    fig.suptitle(titre)
    plt.tight_layout()
    plt.savefig("comparaison_parametres.png", dpi=150)
    plt.close()

    meilleure_combo = min(resultats, key=lambda r: r["moyenne"])
    print(f"Meilleure combinaison en moyenne : p={meilleure_combo['p']}, g={meilleure_combo['g']} "
          f"({meilleure_combo['moyenne']:.2f} km)")

    return resultats


if __name__ == "__main__":
    # Charge les mêmes villes que le fichier de base, via ses fonctions importées
    noms_villes, coord_villes = charger_villes("villes_france_lat_long.csv")
    matrice_distances = construire_matrice_distances(coord_villes)

    # AJOUT : courbe de complexité théorique, enregistrée en PNG (complexite.png)
    tracer_courbe_complexite(n_projet=len(noms_villes), afficher=False)
    print("Graphique enregistré : complexite.png")

    # AJOUT : comparaison des meilleurs parcours obtenus pour différentes combinaisons de
    # paramètres (population, générations) — chaque combinaison est répétée plusieurs fois
    # pour comparer une distance moyenne fiable plutôt qu'un seul tirage aléatoire.
    print("\nComparaison des paramètres du GA (peut prendre un moment pour les grandes combinaisons) :")
    comparer_parametres(coord_villes, matrice_distances, repetitions=3)
    print("Graphique enregistré : comparaison_parametres.png")
