# 🚚 Delivery Route Optimization Model

## 📘 Description du projet  
Ce projet vise à **optimiser les itinéraires de livraison** des véhicules en fonction des positions géographiques des clients.  
Il utilise des techniques de **clustering (K-Means)** pour regrouper les clients par zones, puis applique un **algorithme d’optimisation du voyageur de commerce (TSP)** pour minimiser les distances de trajet pour chaque véhicule.  

Le résultat est une **carte interactive générée avec Folium**, affichant :  
- Les itinéraires optimisés pour chaque véhicule  
- Les clients numérotés selon l’ordre de livraison  
- L’emplacement de l’entrepôt central (Sfax)

---

## 🧠 Fonctionnalités principales  
- Connexion automatique à une base de données MySQL  
- Récupération des coordonnées géographiques des clients  
- Identification des véhicules disponibles  
- Clustering des clients par véhicule (K-Means)  
- Optimisation du trajet (algorithme 2-opt du TSP)  
- Visualisation interactive via **Folium** (carte HTML)  
- Marqueurs colorés et numérotés pour chaque client  

---

## 🗂️ Structure du projet  

Delivery-Route-Optimization-Model/
│
├── main.py # Code principal du projet
├── carte_vehicule.html # Carte générée avec les itinéraires
├── README.md # Ce fichier de documentation
└── requirements.txt # Liste des dépendances Python


---

## 🛠️ Technologies utilisées  
- **Python 3.x**  
- **MySQL Connector** – pour interagir avec la base de données  
- **NumPy** – pour les opérations numériques  
- **SciPy** – pour le calcul des distances euclidiennes  
- **Scikit-learn (KMeans)** – pour le clustering des clients  
- **Folium** – pour la visualisation des trajets sur carte  
- **Tkinter** – pour l’interface utilisateur (exécution du script)  

---

## 🗄️ Base de données MySQL  

### 🔹 Table `clients`
| id | nom | telephone | ville | x (latitude) | y (longitude) |
|----|-----|------------|-------|---------------|----------------|

### 🔹 Table `vehicules`
| id_vehicule | disponibilite |
|--------------|----------------|
| 1            | 1              |
| 2            | 0              |

> ⚠️ Seuls les véhicules avec `disponibilite = 1` sont pris en compte dans l’optimisation.



🧩 Exemple de résultat
## 🗺️ Aperçu du résultat  

Voici un aperçu de la carte générée après exécution du programme :  

![Aperçu de la carte](carte%20véhicule.png)

### 🔗 Voir la carte interactive
👉 [Ouvrir la carte interactive `carte_vehicule.html`](carte_vehicule.html)

Les clients sont représentés par des marqueurs colorés selon le véhicule.

L’ordre des visites est numéroté.

Les trajets sont reliés par des polylignes de couleurs différentes.

L’entrepôt est ville (Sfax) .

## 📈 Améliorations possibles
Intégrer des contraintes supplémentaires (capacité véhicule, temps de livraison, etc.)

Déployer une interface web Flask/Django pour la visualisation dynamique

Utiliser des algorithmes plus avancés (Ant Colony, Genetic Algorithm, etc.)

Ajouter une interface graphique complète (Tkinter ou PyQt5)

## 👩‍💻 Auteur
Nada Cherni
Étudiante ingénieure en Data & Systèmes Décisionnels
Passionnée par la Data Science, l’optimisation et l’analyse de données géospatiales.
