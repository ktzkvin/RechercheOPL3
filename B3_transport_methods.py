import copy


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
