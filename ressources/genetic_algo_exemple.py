import random
import math
import matplotlib.pyplot as plt

def fitness(tour, distances):
    # 1. Trajet classique + Retour au point de départ
    total = sum(distances[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    total += distances[tour[-1]][tour[0]]
    return total 

def selection(population, distances, k=3):
    # 2. Vrai système de tournoi : on tire k individus au hasard
    competiteurs = random.sample(population, k)
    return min(competiteurs, key=lambda tour: fitness(tour, distances))

def order_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    child[start:end] = parent1[start:end]
    p2_filtered = [x for x in parent2 if x not in child]
    child[:start] = p2_filtered[:start]
    child[end:] = p2_filtered[start:]
    return child

def mutate(child):
    idx1, idx2 = random.sample(range(len(child)), 2)
    child[idx1], child[idx2] = child[idx2], child[idx1]
    return child

def genetic_algorithm(villes, distances, population_size=100, generations=500):
    # 3. Uniformisation du mot "population"
    population = [random.sample(range(len(villes)), len(villes)) for _ in range(population_size)]
    
    for generation in range(generations):
        new_population = []
        for _ in range(population_size):
            parent1 = selection(population, distances)
            parent2 = selection(population, distances)
            child = order_crossover(parent1, parent2)
            
            if random.random() < 0.05:
                child = mutate(child)
                
            new_population.append(child)
        population = new_population
    
    best_tour = min(population, key=lambda tour: fitness(tour, distances))
    return best_tour, fitness(best_tour, distances)

villes = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(15)]

distances = []

for i in range(len(villes)):
    row = []
    for j in range(len(villes)):
        dist = math.hypot((villes[i][0] - villes[j][0]), (villes[i][1] - villes[j][1]))
        row.append(dist)
    distances.append(row)

meilleurs_parcours = genetic_algorithm(villes, distances, population_size=100, generations=300)
meilleure_distance = fitness(meilleurs_parcours[0], distances)
