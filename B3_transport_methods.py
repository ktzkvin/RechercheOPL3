import copy
from collections import deque


# Fonction pour appliquer la méthode de Nord-Ouest
def nord_ouest_method(graph_data):
    """
    Applique la méthode de Nord-Ouest pour résoudre le problème de transport.
    :param graph_data: Dictionnaire contenant les données du problème de transport
    :return: Matrice des propositions de transport
    """
    # Récupérer les dimensions du tableau
    n = len(graph_data['provisions'])
    m = len(graph_data['commandes'])

    # Créer des copies des listes de provisions et de commandes
    provisions_copie = graph_data['provisions'][:]
    commandes_copie = graph_data['commandes'][:]

    # Initialiser la matrice des propositions avec des zéros
    propositions = [[0 for _ in range(m)] for _ in range(n)]

    # Indices pour parcourir les lignes et les colonnes
    i = 0
    j = 0

    # Tant qu'il reste des fournisseurs et des clients à servir
    while i < n and j < m:
        # Allouer autant que possible en partant du coin nord-ouest
        quantity = min(provisions_copie[i], commandes_copie[j])
        propositions[i][j] = quantity

        # Mettre à jour les provisions et les commandes restantes dans les copies
        provisions_copie[i] -= quantity
        commandes_copie[j] -= quantity

        # Passer au fournisseur suivant s'il n'a plus de provision
        if provisions_copie[i] == 0:
            i += 1

        # Passer au client suivant s'il n'a plus de commande
        if commandes_copie[j] == 0:
            j += 1

    return propositions


# Fonction pour appliquer la méthode de Balas-Hammer
def balas_hammer_method(graph_data):
    """
    Applique la méthode de Balas-Hammer pour résoudre le problème de transport.
    :param graph_data: Dictionnaire contenant les données du problème de transport
    :return: Matrice des propositions de transport
    """
    # Initialisation
    provisions = graph_data['provisions'].copy()
    commandes = graph_data['commandes'].copy()
    costs = copy.deepcopy(graph_data['couts'])  # Copie des coûts pour éviter les modifications sur graph_data
    taille = graph_data['taille']
    fournisseurs, clients = taille

    # Tableau initial de toutes les attributions à zéro
    propositions = [[0 for _ in range(clients)] for _ in range(fournisseurs)]


    while sum(provisions) > 0 and sum(commandes) > 0:
        
        # Calcul des pénalités...
        
        # ...pour chaque ligne
        delta_rows = []        
        for row in costs:
            valid_costs = [cost for cost in row if cost != float('inf')]  # Coûts valides (non infinis)
            if valid_costs:
                delta_rows.append(max(valid_costs) - min(valid_costs))
            else:
                delta_rows.append(-float('inf'))

        # ...pour chaque colonne
        delta_cols = []
        for j in range(clients):
            valid_costs = [costs[i][j] for i in range(fournisseurs) if costs[i][j] != float('inf')]  # Coûts valides (non infinis)
            if valid_costs:
                delta_cols.append(max(valid_costs) - min(valid_costs))
            else:
                delta_cols.append(-float('inf'))

        # Sélectionner la ligne ou la colonne avec la plus grande pénalité
        max_delta_row = max(delta_rows)
        max_delta_col = max(delta_cols)

        # Si toutes les lignes et colonnes sont infinies, arrêter le processus
        if max_delta_row == -float('inf') and max_delta_col == -float('inf'):
            break

        # Récupération de la cellule avec le coût minimum dans la ligne/colonne sélectionnée
        if max_delta_row >= max_delta_col:
            i = delta_rows.index(max_delta_row)  # Indice de la ligne sélectionnée
            filtered_row = [costs[i][j] for j in range(clients) if costs[i][j] != float('inf')]
            min_cost = min(filtered_row)  # Coût minimum dans la ligne sélectionnée
            j = costs[i].index(min_cost)  # Indice de la colonne sélectionnée
        else:
            j = delta_cols.index(max_delta_col)  # Indice de la colonne sélectionnée
            filtered_col = [costs[i][j] for i in range(fournisseurs) if costs[i][j] != float('inf')]
            min_cost = min(filtered_col)  # Coût minimum dans la colonne sélectionnée
            i = next(i for i in range(fournisseurs) if costs[i][j] == min_cost)  # Indice de la ligne sélectionnée

        # Maximiser la cellule sélectionnée en fonction des provisions et des commandes
        quantity = min(provisions[i], commandes[j])  # Quantité maximale entre les provisions et les commandes
        propositions[i][j] += quantity   # Ajout de la quantité à la cellule sélectionnée
        provisions[i] -= quantity  # Mise à jour des provisions
        commandes[j] -= quantity  # Mise à jour des commandes

        # Marquage de la cellule comme utilisée en fixant son coût à infini
        costs[i][j] = float('inf')

    return propositions


# Fonction pour vérifier la connexité du graphe en utilisant un parcours en largeur (Breadth-First Search)
def bfs_connexity(graph_data):
    """
    Vérifie si le graphe est connexe en utilisant un parcours en largeur (BFS).
    :param graph_data: Données du graphe
    :return: True si le graphe est connexe, False sinon
    """
    # Initialisation : extraire les dimensions du graphe
    num_fournisseurs, num_clients = graph_data['taille']

    # Total de sommets (fournisseurs + clients)
    total_vertices = num_fournisseurs + num_clients
    visited = [False] * total_vertices  # Initialiser tous les sommets comme non visités
    queue = deque([0])  # Commencer par le premier fournisseur

    # Parcours en largeur (BFS) pour trouver les connexions
    while queue:
        vertex = queue.popleft()  # Extraire le sommet de la file
        if not visited[vertex]:  # Si le sommet n'a pas été visité
            visited[vertex] = True  # Marquer le sommet comme visité

            # Ajouter les sommets adjacents à la file :
            if vertex < num_fournisseurs:  # Ce sommet est un fournisseur

                # Parcourir les propositions pour trouver les clients connectés
                for j in range(num_clients):
                    # Si proposition de la cellule > 0 et le client n'a pas été visité
                    if graph_data['propositions'][vertex][j] > 0 and not visited[num_fournisseurs + j]:
                        queue.append(num_fournisseurs + j)  # Ajouter le client à la file

            else:  # Ce sommet est un client
                client_index = vertex - num_fournisseurs  # Indice du client dans les propositions
                for i in range(num_fournisseurs):
                    # Si proposition de la cellule > 0 et le fournisseur n'a pas été visité
                    if graph_data['propositions'][i][client_index] > 0 and not visited[i]:
                        queue.append(i)  # Ajouter le fournisseur à la file

    return all(visited)  # Le graphe est connexe si tous les sommets ont été visités


# Fonction pour vérifier si un chemin existe entre deux sommets dans le graphe
def path_exists(graph_data, start, end, visited):
    """
    Vérifie s'il existe un chemin entre deux sommets dans le graphe.
    :param graph_data: Dictionnaire contenant les données du graphe
    :param start: Sommet de départ
    :param end: Sommet d'arrivée
    :param visited: Liste des sommets visités
    :return: True si un chemin existe, False sinon
    """
    # Parcours en largeur (BFS) pour trouver s'il existe un chemin de start à end
    queue = deque([start])
    visited[start] = True
    while queue:
        current = queue.popleft()
        if current == end:
            return True  # Chemin trouvé
        # Parcourir les propositions pour trouver les sommets adjacents
        if current < len(graph_data['propositions']):  #
            for j in range(len(graph_data['propositions'][current])):
                if graph_data['propositions'][current][j] > 0:
                    neighbor = j + len(graph_data['propositions'])  # Indice du client
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
        else:  # C'est un client
            client_index = current - len(graph_data['propositions'])
            # Parcourir les propositions pour trouver les sommets adjacents
            for i in range(len(graph_data['propositions'])):
                if graph_data['propositions'][i][client_index] > 0:
                    if not visited[i]:
                        visited[i] = True
                        queue.append(i)
    return False  # Pas de chemin trouvé


# Fonction pour trouver les composants connexes du graphe
def find_connected_components(graph_data):
    """
    Trouve les composants connexes du graphe en utilisant un parcours en largeur (BFS).
    :param graph_data: Dictionnaire contenant les données du graphe
    :return: Liste des composants connexes
    """
    num_fournisseurs, num_clients = graph_data['taille']
    total_vertices = num_fournisseurs + num_clients
    visited = [False] * total_vertices
    components = []

    def bfs(start_vertex):
        """
        Parcours en largeur (BFS) pour trouver les composants connexes.
        :param start_vertex: Sommet de départ
        :return: Liste des sommets du composant connexe
        """
        queue = deque([start_vertex])
        component = []
        visited[start_vertex] = True
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            # Déterminer les connexions en fonction de si c'est un fournisseur ou un client
            if vertex < num_fournisseurs:
                for j in range(num_clients):
                    if graph_data['propositions'][vertex][j] > 0 and not visited[num_fournisseurs + j]:
                        visited[num_fournisseurs + j] = True
                        queue.append(num_fournisseurs + j)
            else:  # C'est un client
                client_index = vertex - num_fournisseurs
                for i in range(num_fournisseurs):
                    if graph_data['propositions'][i][client_index] > 0 and not visited[i]:
                        visited[i] = True
                        queue.append(i)
        return component

    for v in range(total_vertices):
        if not visited[v]:
            components.append(bfs(v))

    return components


def calcul_potentiels(graph_data):
    # Initialiser les potentiels
    potentiels = {'P1': 0}

    # Parcourir les coûts et les propositions pour trouver les arêtes avec une proposition non nulle
    for i, row in enumerate(graph_data['couts']):
        for j, cout in enumerate(row):
            proposition = graph_data['propositions'][i][j]
            if proposition != 0 or (i, j) == graph_data.get('combinaison_minimale', (-1, -1)):
                Pi = 'P{}'.format(i + 1)
                Cj = 'C{}'.format(j + 1)
                if Pi in potentiels and Cj not in potentiels:
                    # Mettre à jour E(Cj) si Pi est connu et Cj est inconnu
                    potentiels[Cj] = potentiels[Pi] - cout
                    print("E({}) - E({}) = {}".format(Pi, Cj, cout))
                elif Cj in potentiels and Pi not in potentiels:
                    # Stocker temporairement le calcul pour une utilisation ultérieure
                    potentiels[Pi] = cout + potentiels[Cj]
                    print("E({}) - E({}) = {}".format(Pi, Cj, cout))

    # Afficher les résultats
    print('\nRésultats des potentiels :')
    for key, value in potentiels.items():
        print("E({}) = {}".format(key, value))

    return potentiels.items()


def calcul_potentiels_not_connexe(graph_data):
    # Initialiser les potentiels
    potentiels = {'P1': 0}

    # Trouver la combinaison minimale
    combinaison_minimale = trouver_combinaison_minimale(graph_data)

    # Créer une copie de graph_data
    graph_data_copy = graph_data.copy()

    print('\nCalculs potentiels par sommets :')

    # Modifier la copie pour prendre en compte la nouvelle proposition
    if combinaison_minimale:
        i, j = combinaison_minimale
        graph_data_copy['propositions'][i][j] = -1  # Initialiser la valeur à -1

    # Répéter les calculs jusqu'à la convergence
    while len(potentiels) < graph_data['taille'][0] + graph_data['taille'][1]:
        updated = False  # Variable pour suivre si des mises à jour ont été effectuées

        # Parcourir les propositions de la copie pour mettre à jour les potentiels
        for i, row in enumerate(graph_data_copy['couts']):
            for j, cout in enumerate(row):
                proposition = graph_data_copy['propositions'][i][j]
                if proposition != 0 or (i, j) == combinaison_minimale:
                    Pi = 'P{}'.format(i + 1)
                    Cj = 'C{}'.format(j + 1)
                    if Pi not in potentiels and Cj in potentiels:
                        potentiels[Pi] = cout + potentiels[Cj]
                        print("E({}) - E({}) = {}".format(Pi, Cj, cout))
                        updated = True
                    elif Cj not in potentiels and Pi in potentiels:
                        potentiels[Cj] = potentiels[Pi] - cout
                        print("E({}) - E({}) = {}".format(Pi, Cj, cout))
                        updated = True

        # Vérifier si des mises à jour ont été effectuées, sinon sortir de la boucle
        if not updated:
            break

    # Afficher les résultats
    print('\nRésultats des potentiels :')
    for key, value in potentiels.items():
        print("E({}) = {}".format(key, value))

    return potentiels.items()



def trouver_combinaison_minimale(graph_data):
    # Créer une copie temporaire des coûts
    couts_temp = [row[:] for row in graph_data['couts']]

    # Trouver la valeur minimale dans les coûts
    couts_minimaux = min(min(row) for row in couts_temp)

    # Parcourir les coûts copiés pour trouver l'indice de la valeur minimale
    for i, row in enumerate(couts_temp):
        for j, cout in enumerate(row):
            if cout == couts_minimaux:
                indice_minimal_i = i
                indice_minimal_j = j
                break

    # Vérifier si la proposition associée a une valeur nulle
    if graph_data['propositions'][indice_minimal_i][indice_minimal_j] == 0:
        combinaison_minimale = (indice_minimal_i, indice_minimal_j)
        print("L'arrête à ajouter pour l'obtention d'une proposition non dégénérée est P{}-C{}".format(indice_minimal_i + 1, indice_minimal_j + 1))

    else:
        # Mettre à jour les coûts copiés pour exclure la proposition associée
        couts_temp[indice_minimal_i][indice_minimal_j] = float('inf')
        # Appeler récursivement la fonction en utilisant les copies modifiées
        combinaison_minimale = trouver_combinaison_minimale({'couts': couts_temp, 'propositions': graph_data['propositions']})

    return combinaison_minimale


# Fonction pour vérifier la connexité du graphe
def rendre_graphe_connexe(graph_data):
    """
    Rendre le graphe connexe en ajoutant des arêtes.
    :param graph_data: Dictionnaire contenant les données du graphe
    :return: None
    """
    # Vérifier si le graphe est déjà connexe
    if graph_data['propositions'] is None:
        graph_data['propositions'] = [[0] * graph_data['taille'][1] for _ in range(graph_data['taille'][0])]

    # Tant que le graphe n'est pas connexe, ajouter des arêtes
    while not bfs_connexity(graph_data):
        # Trouver une arête minimale à ajouter qui n'introduit pas de cycle
        combinaison_minimale = trouver_combinaison_minimale(graph_data)
        i, j = combinaison_minimale
        # Ajouter cette arête au graphe
        graph_data['propositions'][i][j] += 1  # Incrémenter la proposition
        print(f"Ajout de l'arête P{i + 1}C{j + 1} pour améliorer la connexité.")

    print("Le graphe est maintenant connexe.")
