# travelling-merchant-
Résolution du problème du voyageur de commerce (TSP) via l'implémentation de l'algorithme de Christofides et d'un algorithme génétique. Projet axé sur l'optimisation combinatoire, la théorie des graphes, la modélisation géospatiale (Haversine) et le benchmarking de performance (complexité, temps d'exécution, convergence).

## Géométrie et Distances
Pour pouvoir s'approcher au plus près de la distance minimale à parcourir, nous devons tout d'abord aborder le calcul de la distance entre deux points. Nous utiliserons ici la formule de Haversine.

### 1. Le problème des degrés GPS
En mathématiques, les formules géométriques ne comprennent pas les coordonnées exprimées en degrés, elles utilisent des **radians**. Il nous faut donc convertir nos coordonnées en radians. La formule de conversion est simple : **Radians = Degrés X pi/180**.

### 2. La formule de Haversine
La Terre est une sphère (d'un Rayon = 6371 Km), on ne peut pas tracer une ligne droite à travers le sol. On utilise la distance de Haversine pour calculer la courbe à la surface.

**Formule de Haversine :**
d = 2 × R × arcsin( √ [ sin²(Δφ / 2) + cos(φ₁) × cos(φ₂) × sin²(Δλ / 2) ] )