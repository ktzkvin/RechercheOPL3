import copy
from collections import deque


def nord_ouest_method(graph_data):
    # Récupérer les dimensions du tableau
    n = len(graph_data['provisions'])
    m = len(graph_data['commandes'])

    # Créer des copies des listes de provisions et de commandes
    provisions_copie = graph_data['provisions'][:]
    commandes_copie = graph_data['commandes'][:]

    # Initialiser la matrice d'allocation avec des zéros
    allocation = [[0 for _ in range(m)] for _ in range(n)]

    # Indices pour parcourir les lignes et les colonnes
    i = 0
    j = 0

    # Tant qu'il reste des fournisseurs et des clients à servir
    while i < n and j < m:
        # Allouer autant que possible en partant du coin nord-ouest
        quantity = min(provisions_copie[i], commandes_copie[j])
        allocation[i][j] = quantity

        # Mettre à jour les provisions et les commandes restantes dans les copies
        provisions_copie[i] -= quantity
        commandes_copie[j] -= quantity

        # Passer au fournisseur suivant s'il n'a plus de provision
        if provisions_copie[i] == 0:
            i += 1

        # Passer au client suivant s'il n'a plus de commande
        if commandes_copie[j] == 0:
            j += 1

    return allocation


def balas_hammer_method(graph_data):

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


def bfs_connexity(graph_data):
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


def is_acyclic_bfs(graph_data):
    num_fournisseurs, num_clients = graph_data['taille']
    total_vertices = num_fournisseurs + num_clients
    visited = [False] * total_vertices
    parent = [-1] * total_vertices
    queue = deque()

    # Envisagez chaque fournisseur et chaque client comme un point de départ potentiel
    for start in range(total_vertices):
        if not visited[start]:
            queue.append(start)
            visited[start] = True

            while queue:
                current = queue.popleft()

                # Déterminer les voisins en fonction du type de sommet
                if current < num_fournisseurs:  # Sommet actuel est un fournisseur
                    for j in range(num_clients):
                        neighbor = num_fournisseurs + j
                        if graph_data['propositions'][current][j] > 0:
                            if visited[neighbor] and parent[current] != neighbor:
                                return False  # Un cycle a été trouvé
                            if not visited[neighbor]:
                                visited[neighbor] = True
                                parent[neighbor] = current
                                queue.append(neighbor)
                else:  # Sommet actuel est un client
                    client_index = current - num_fournisseurs
                    for i in range(num_fournisseurs):
                        neighbor = i
                        if graph_data['propositions'][i][client_index] > 0:
                            if visited[neighbor] and parent[current] != neighbor:
                                return False  # Un cycle a été trouvé
                            if not visited[neighbor]:
                                visited[neighbor] = True
                                parent[neighbor] = current
                                queue.append(neighbor)

    return True  # Aucun cycle détecté
