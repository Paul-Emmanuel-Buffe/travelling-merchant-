import time
import matplotlib.pyplot as plt

def evaluer_complexite(df_positions, main_func, tailles=[4, 6, 8, 10, 12, 14, 16, 18, 20], nb_tests=10):
    temps_execution = []

    for n in tailles:
        df_sub = df_positions.head(n)
        
        # Moyenne sur plusieurs passages pour éliminer le bruit processeur
        durees = []
        for _ in range(nb_tests):
            debut = time.perf_counter()
            main_func(df_sub)
            durees.append(time.perf_counter() - debut)

        temps_moyen = sum(durees) / len(durees)
        temps_execution.append(temps_moyen)
        print(f"N = {n} villes : {temps_moyen:.4f} s")

    plt.figure(figsize=(8, 5))
    plt.plot(tailles, temps_execution, marker='o', color='purple', linewidth=2)
    plt.xlabel("Nombre de villes (N)")
    plt.ylabel("Temps moyen d'exécution (secondes)")
    plt.title("Courbe expérimentale de complexité (N <= 20)")
    plt.grid(True)
    plt.show()