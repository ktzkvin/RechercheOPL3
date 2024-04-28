import copy


def balas_hammer_method(graph_data):

    # Initialisation
    provisions = graph_data['provisions'].copy()
    commandes = graph_data['commandes'].copy()
    costs = copy.deepcopy(graph_data['costs'])  # Copie des coûts pour éviter les modifications sur graph_data
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


def connexe(graph_data):
    row_column = graph_data['taille'][0] + graph_data['taille'][1]

    notzero = 0
    for proposition in graph_data['propositions']:
        for valeur in proposition:
            if valeur != 0:
                notzero += 1
    if notzero + 1 == row_column:
        print('Le diagramme est connexe')
        return 0
    elif notzero + 2 == row_column:
        print("Le diagramme est non connexe")
        return 1
    else:
        print("Le diagramme est non connexe et doit trouver plusieurs arrêtes")
        return 2


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
        print("L'arrête à ajouté pour l'obtention d'une proposition non dégénérée est P{}C{}".format(indice_minimal_i + 1, indice_minimal_j + 1))

    else:
        # Mettre à jour les coûts copiés pour exclure la proposition associée
        couts_temp[indice_minimal_i][indice_minimal_j] = float('inf')
        # Appeler récursivement la fonction en utilisant les copies modifiées
        combinaison_minimale = trouver_combinaison_minimale({'couts': couts_temp, 'propositions': graph_data['propositions']})

    return combinaison_minimale


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


def nord_ouest(graph_data):
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

