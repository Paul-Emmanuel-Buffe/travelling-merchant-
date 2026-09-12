import time
import matplotlib.pyplot as plt

# 1. On passe nb_tests à 100 par défaut
def evaluer_complexite(df_positions, main_func, tailles=[4, 6, 8, 10, 12, 14, 16, 18, 20], nb_tests=100):
    # Lancement à blanc pour chauffer le processeur et charger la mémoire
    main_func(df_positions.head(tailles[0]))

    temps_execution = []

    for n in tailles:
        df_sub = df_positions.head(n)
        
        durees = []
        for _ in range(nb_tests):
            debut = time.perf_counter()
            main_func(df_sub)
            durees.append(time.perf_counter() - debut)

        # 2. On prend le temps minimum absolu au lieu de la moyenne
        temps_retenu = min(durees)
        temps_execution.append(temps_retenu)
        print(f"N = {n} villes : {temps_retenu:.4f} s")

    plt.figure(figsize=(8, 5))
    plt.plot(tailles, temps_execution, marker='o', color='purple', linewidth=2)
    plt.xlabel("Nombre de villes (N)")
    plt.ylabel("Temps d'exécution optimal (secondes)")
    plt.title("Courbe expérimentale de complexité (N <= 20)")
    plt.grid(True)
    plt.show()