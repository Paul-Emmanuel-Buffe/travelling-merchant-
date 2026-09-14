# Le Marchand Ambulant — Travelling Merchant

Projet de modélisation et de résolution du **problème du voyageur de commerce (TSP — Travelling Salesperson Problem)** appliqué à une tournée de **20 villes françaises** pour le marchand ambulant Théobald.

L'objectif est de déterminer un itinéraire permettant de visiter chaque ville **une seule fois**, puis de revenir au point de départ, tout en minimisant la distance totale parcourue.

---

## Présentation du projet

Dans la France médiévale, les marchands ambulants devaient parcourir de longues distances pour vendre leurs marchandises dans différentes villes, marchés et foires.

Pour Théobald, chaque détour inutile représente un coût supplémentaire, un retard et une exposition accrue aux différents dangers liés aux voyages.

Le projet consiste donc à résoudre le **Travelling Salesperson Problem (TSP)** afin de trouver une tournée aussi courte que possible.

Le TSP consiste à trouver le circuit de longueur minimale permettant de :

* partir d'une ville de départ ;
* visiter les 20 villes ;
* visiter chaque ville une seule fois ;
* revenir à la ville de départ.

Le problème étant NP-difficile, nous comparons deux approches permettant d'obtenir efficacement des solutions proches de l'optimum :

1. **L'algorithme de Christofides**
2. **L'algorithme génétique**

---

## Objectifs

Les objectifs du projet sont les suivants :

* Modéliser les 20 villes sous forme d'un graphe.
* Récupérer leurs coordonnées géographiques.
* Calculer les distances entre les villes avec la formule de **Haversine**.
* Résoudre le TSP avec l'algorithme de **Christofides**.
* Résoudre le TSP avec un **algorithme génétique**.
* Tester différentes configurations de l'algorithme génétique.
* Comparer les deux méthodes.
* Visualiser les itinéraires obtenus sur des cartes.
* Déterminer quelle approche est la plus adaptée au problème de Théobald.

---

# 🛠️ Installation

## 1. Cloner le repository

```bash
git clone https://github.com/USERNAME/travelling-merchant.git
cd travelling-merchant
```

## 2. Créer un environnement virtuel

```bash
python3 -m venv .venv
```

## 3. Activer l'environnement virtuel

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

## 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 5. Lancer le programme

```bash
python src/main.py
```

---

# 📂 Structure du projet

```text
travelling-merchant/
│
├── data/
│   └── villes.csv
│
├── results/
│   ├── carte_christofides.html
│   └── carte_genetique.html
│
├── src/
│   ├── christofides.py
│   ├── distances.py
│   ├── figures.py
│   ├── genetique.py
│   └── main.py
│
├── README.md
└── requirements.txt
```

### Description des fichiers

| Fichier               | Description                                    |
| --------------------- | ---------------------------------------------- |
| `data/villes.csv`     | Coordonnées GPS des 20 villes françaises       |
| `src/distances.py`    | Calcul des distances avec Haversine            |
| `src/christofides.py` | Implémentation de l'algorithme de Christofides |
| `src/genetique.py`    | Implémentation de l'algorithme génétique       |
| `src/figures.py`      | Génération des visualisations et cartes        |
| `src/main.py`         | Point d'entrée principal du programme          |
| `results/`            | Cartes et résultats générés                    |
| `requirements.txt`    | Liste des dépendances Python                   |

---

# 1. Modélisation du problème

Les 20 villes françaises sont représentées sous forme d'un **graphe complet, non orienté et pondéré**.

Chaque :

* **sommet** représente une ville ;
* **arête** représente une liaison entre deux villes ;
* **poids de l'arête** représente la distance entre les deux villes.

Les coordonnées géographiques des villes sont stockées dans :

```text
data/villes.csv
```

Exemple :

```csv
ville,latitude,longitude
Paris,48.8566,2.3522
Lille,50.6292,3.0573
Lyon,45.7640,4.8357
```

Le réseau est modélisé avec la bibliothèque **NetworkX**.

---

# 2. Calcul des distances — Formule de Haversine

La distance entre deux villes est calculée à partir de leurs coordonnées GPS.

La formule de Haversine permet d'estimer la distance entre deux points situés sur une sphère.

Le rayon moyen de la Terre utilisé dans le projet est :

```text
R = 6371 km
```

La distance obtenue est exprimée en kilomètres.

Cette distance correspond à une distance géographique à vol d'oiseau et non à une distance routière.

---

# 3. Algorithme de Christofides

## Principe

L'algorithme de Christofides est une méthode heuristique permettant d'obtenir une solution au TSP avec une garantie théorique lorsque les distances respectent les conditions nécessaires.

Les principales étapes sont :

```text
Graphe complet
     ↓
Arbre couvrant minimal (MST)
     ↓
Sommets de degré impair
     ↓
Couplage parfait
     ↓
Graphe eulérien
     ↓
Circuit eulérien
     ↓
Raccourcissement
     ↓
Circuit hamiltonien
```

### Étape 1 — Arbre couvrant minimal

On commence par construire un **Minimum Spanning Tree (MST)** du graphe.

L'objectif est de relier toutes les villes avec un poids total minimal.

### Étape 2 — Sommets de degré impair

On identifie ensuite les sommets dont le degré est impair dans le MST.

### Étape 3 — Couplage parfait

Un couplage parfait est calculé sur les sommets de degré impair afin de compléter le graphe.

### Étape 4 — Graphe eulérien

Le MST et le couplage sont combinés afin d'obtenir un graphe dont les sommets possèdent un degré pair.

Un circuit eulérien peut alors être construit.

### Étape 5 — Raccourcissement

Lors du parcours du circuit eulérien, les villes déjà visitées sont ignorées afin d'obtenir une tournée passant une seule fois par chaque ville.

On obtient ainsi une solution au TSP.

## Résultat

La solution obtenue avec Christofides est d'environ :

```text
≈ 3 445 km
```

Le résultat est déterministe : pour les mêmes données et les mêmes conditions d'exécution, l'algorithme produit la même solution.

---

# 4. Algorithme génétique

L'algorithme génétique est une métaheuristique inspirée du fonctionnement de l'évolution naturelle.

Chaque individu représente une tournée possible des 20 villes.

Exemple :

```text
Paris → Lille → Rouen → Rennes → Nantes → ...
```

Une population contient plusieurs tournées différentes.

---

## Représentation d'un individu

Un individu est représenté par une **permutation des villes**.

Par exemple :

```text
[Paris, Lyon, Nice, Marseille, Toulouse, Bordeaux, ...]
```

Chaque ville apparaît une seule fois.

---

## Fonction d'évaluation

La qualité d'une solution dépend de la distance totale parcourue.

Plus la distance est faible, meilleure est la solution.

On peut donc définir la fitness à partir de la distance totale :

```text
fitness = 1 / distance
```

Une tournée courte possède ainsi une meilleure fitness.

---

## Sélection

La sélection est effectuée avec une **sélection par tournoi**.

Le paramètre utilisé est :

```text
k = 3
```

Trois individus sont sélectionnés aléatoirement et le meilleur est choisi comme parent.

---

## Croisement

Le projet utilise l'**Ordered Crossover (OX)**.

Cette méthode permet de conserver une partie de l'ordre des villes tout en évitant les doublons dans la permutation finale.

---

## Mutation

Une mutation de type **Swap** est utilisée.

Deux villes sont sélectionnées aléatoirement et leurs positions sont échangées.

Exemple :

```text
Avant :
Paris → Lyon → Nice → Marseille

Après :
Paris → Marseille → Nice → Lyon
```

La mutation permet de maintenir une diversité suffisante dans la population et d'explorer de nouvelles solutions.

---

# Paramètres de l'algorithme génétique

Plusieurs configurations ont été testées.

Les paramètres étudiés comprennent notamment :

| Paramètre             | Valeurs testées                 |
| --------------------- | ------------------------------- |
| Taille de population  | 50 à 200                        |
| Nombre de générations | 100 à 500                       |
| Sélection             | Tournoi                         |
| Taille du tournoi     | 3                               |
| Croisement            | Ordered Crossover (OX)          |
| Mutation              | Swap                            |
| Taux de mutation      | Variable selon la configuration |

Les expérimentations montrent qu'une augmentation de la taille de la population et du nombre de générations peut améliorer la qualité de la solution, au prix d'un temps d'exécution plus important.

---

# 5. Résultats

Les résultats obtenus sont approximativement les suivants :

| Critère           | Christofides | Algorithme génétique |
| ----------------- | -----------: | -------------------: |
| Distance          |   ≈ 3 445 km |           ≈ 3 386 km |
| Complexité        |        O(n³) |         O(G × P × n) |
| Temps d'exécution |     < 0,05 s |        ≈ 0,5 à 1,5 s |
| Déterminisme      |          Oui |                  Non |
| Type              |  Heuristique |      Métaheuristique |

> Les performances de l'algorithme génétique peuvent varier d'une exécution à l'autre en raison de son caractère stochastique.

---

# 6. Visualisation

Les itinéraires obtenus sont représentés sous forme de cartes interactives.

Les résultats sont enregistrés dans :

```text
results/
├── carte_christofides.html
└── carte_genetique.html
```

Ces cartes permettent de visualiser les différents parcours calculés pour Théobald.

---

# 7. Analyse comparative

## Christofides

### Avantages

* Solution obtenue rapidement.
* Résultat déterministe.
* Méthode mathématiquement encadrée.
* Bonne qualité de solution.
* Temps d'exécution très faible.

### Inconvénients

* Implémentation théorique plus complexe.
* La solution n'est pas nécessairement l'optimum absolu.
* Moins flexible qu'une approche évolutionnaire pour expérimenter différentes stratégies.

---

## Algorithme génétique

### Avantages

* Permet d'explorer un grand nombre de solutions.
* Peut obtenir une solution meilleure que Christofides sur l'instance étudiée.
* Paramètres configurables.
* Approche flexible.
* Adapté à des problèmes d'optimisation complexes.

### Inconvénients

* Résultat dépendant du hasard.
* Temps d'exécution plus important.
* Nécessite de choisir correctement les paramètres.
* Aucune garantie de trouver l'optimum global.
* Plusieurs exécutions peuvent produire des résultats différents.

---

# 8. Conclusion

Les deux approches permettent d'obtenir rapidement une solution de bonne qualité au problème du voyageur de commerce.

**Christofides** est particulièrement intéressant lorsque Théobald souhaite obtenir rapidement une solution stable et disposer d'une garantie théorique sur sa qualité.

**L'algorithme génétique** permet quant à lui d'explorer davantage l'espace des solutions et a obtenu, lors de nos expérimentations, une distance plus faible :

```text
Christofides      ≈ 3 445 km
Algorithme génétique ≈ 3 386 km
```

L'algorithme génétique reste cependant stochastique et ses performances dépendent fortement de ses paramètres.

### Recommandation

La meilleure stratégie pour Théobald est de **combiner les deux approches** :

1. utiliser Christofides pour obtenir rapidement une excellente solution de référence ;
2. utiliser ensuite l'algorithme génétique pour tenter d'améliorer cette solution ;
3. effectuer plusieurs exécutions afin de limiter l'influence du hasard ;
4. conserver la meilleure tournée obtenue.

Cette combinaison permet donc de bénéficier à la fois de la **rapidité et de la stabilité de Christofides** et de la **capacité d'exploration de l'algorithme génétique**.

---

# Technologies utilisées

Le projet est développé en **Python** et utilise notamment :

* **Python 3**
* **NetworkX** — modélisation et manipulation des graphes
* **Folium** — visualisation des itinéraires sur une carte
* **NumPy** — calcul numérique
* **Pandas** — manipulation des données

Les dépendances sont disponibles dans :

```text
requirements.txt
```

Installation :

```bash
pip install -r requirements.txt
```

---

# Organisation du projet

Le développement est organisé autour des différentes étapes du projet :

```text
1. Collecte des données
        ↓
2. Modélisation du graphe
        ↓
3. Calcul des distances
        ↓
4. Algorithme de Christofides
        ↓
5. Algorithme génétique
        ↓
6. Expérimentations
        ↓
7. Comparaison
        ↓
8. Visualisation
        ↓
9. Conclusion
```

---

# Contexte académique

Ce projet est réalisé dans le cadre d'un projet d'algorithmique portant sur le **problème du voyageur de commerce**.

Il a pour objectif de mettre en pratique :

* la modélisation par graphes ;
* les algorithmes de graphes ;
* les heuristiques d'optimisation ;
* les algorithmes génétiques ;
* l'analyse de complexité ;
* la comparaison expérimentale d'algorithmes.
