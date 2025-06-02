import mysql.connector
import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.cluster import KMeans
import folium
import tkinter as tk
from tkinter import messagebox

# Fonction pour exécuter le code principal
def execute_code():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="mini_projet"
        )
        
        cursor = conn.cursor()
        
        # Récupérer les informations des clients
        cursor.execute("SELECT id, nom, telephone, ville, x, y FROM clients")
        clients_data = cursor.fetchall()
        
        # Convertir les données des clients en une structure adaptée
        clients = [
            {
                "id": row[0],
                "nom": row[1],
                "telephone": row[2],
                "ville": row[3],
                "location": [row[4], row[5]]
            }
            for row in clients_data
        ]
        
        # Récupérer les informations des véhicules disponibles
        cursor.execute("SELECT id_vehicule FROM vehicules WHERE disponibilite = 1")
        vehicules_data = cursor.fetchall()
        
        # Créer un dictionnaire des véhicules disponibles
        vehicules = {row[0] - 1: {"clients": []} for row in vehicules_data}
        
        # Vérifier le nombre de véhicules disponibles et ajuster le nombre de clusters
        nombre_vehicules = len(vehicules)
        nombre_clients = len(clients)
        if nombre_vehicules > nombre_clients:
            nombre_vehicules = nombre_clients
        
        # Coordonnées des villes des clients
        coords_villes = np.array([client["location"] for client in clients])
        
        # Clustering des clients
        nombre_clusters = min(nombre_vehicules, nombre_clients)
        kmeans = KMeans(n_clusters=nombre_clusters, random_state=0)
        kmeans.fit(coords_villes)
        clusters = kmeans.predict(coords_villes)
        
        # Répartir les clients entre les véhicules en fonction des clusters
        vehicules_villes = {i: [] for i in range(nombre_clusters)}
        for client, cluster in zip(clients, clusters):
            vehicules_villes[cluster].append(client)
        
        # Fonction d'optimisation TSP
        def calculate_distance(route, locations):
            return sum(
                euclidean(locations[route[i]], locations[route[i + 1]]) for i in range(len(route) - 1)
            )
        
        def swap_algorithm(route, i, k):
            return np.concatenate((route[:i], route[k:i-1:-1], route[k+1:]))
        
        def optimize_tsp(locations):
            n = len(locations)
            route = np.arange(n)
            route = np.append(route, route[0])  # Retour au point de départ
            best_distance = calculate_distance(route, locations)
            improved = True
        
            while improved:
                improved = False
                for i in range(1, n - 1):
                    for k in range(i + 1, n):
                        new_route = swap_algorithm(route, i, k)
                        new_distance = calculate_distance(new_route, locations)
                        if new_distance < best_distance:
                            route = new_route
                            best_distance = new_distance
                            improved = True
            return route, best_distance
        
        # Coordonnées de l'entrepôt (Sfax)
        entrepot = [34.7407, 10.7605]
        
        # Couleurs pour distinguer les groupes
        colors = ["red", "blue", "green", "purple", "orange", "darkred", "darkblue", "darkgreen", "pink", "cadetblue"]
        
        # Créer une carte principale
        carte_principale = folium.Map(location=entrepot, zoom_start=7)
        
        # Ajouter l'entrepôt sur la carte
        folium.Marker(entrepot, popup="Entrepôt (Sfax)", icon=folium.Icon(color='black')).add_to(carte_principale)
        
        # Parcourir chaque véhicule et ses clients
        for vehicule, villes_cluster in vehicules_villes.items():
            cluster_locations = [entrepot] + [client["location"] for client in villes_cluster]
        
            # Optimiser le chemin TSP
            route, distance = optimize_tsp(cluster_locations)
        
            # Afficher les indices de la route pour le débogage
            print(f"Optimized route for vehicle {vehicule + 1}: {route}")
            print(f"Optimized distance for vehicle {vehicule + 1}: {distance}")
        
            # Tracer le chemin optimisé
            route_coords = [cluster_locations[i] for i in route]
            color = colors[vehicule % len(colors)]  # Attribuer une couleur unique au groupe
            for i in range(1, len(route_coords)):
                folium.PolyLine(
                    locations=[route_coords[i-1], route_coords[i]],
                    color=color, weight=2.5, opacity=1
                ).add_to(carte_principale)
        
            # Ajouter les marqueurs des villes avec numéros
            for i, index in enumerate(route[1:-1]):  # Ignorer l'entrepôt (index 0 et le retour)
                client = villes_cluster[index - 1]  # Récupérer le client correspondant au chemin
                client_number = i + 1  # Numérotation basée sur l'ordre de la route
        
                folium.Marker(
                    client["location"],
                    popup=f"Client {client_number}: {client['nom']} ({client['ville']})",
                    icon=folium.Icon(color=color, icon="info-sign")
                ).add_to(carte_principale)
        
                # Ajouter un texte avec le numéro directement sur le marqueur
                folium.Marker(
                    client["location"],
                    icon=folium.DivIcon(
                        html=f'''
                            <div style="font-size: 16px; font-weight: bold; 
                                        color: black; background-color: {color}; 
                                        border-radius: 50%; text-align: center; 
                                        width: 20px; height: 20px; line-height: 20px;">
                                {client_number}
                            </div>
                        '''
                    )
                ).add_to(carte_principale)
        
        # Sauvegarder la carte principale dans un fichier HTML
        output_path = "carte_vehicule.html"
        carte_principale.save(output_path)

        # Fermer la connexion à la base de données
        cursor.close()
        conn.close()

        print("Map generated:", output_path)


        print("Map generated: carte_vehicule.html")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    execute_code()
