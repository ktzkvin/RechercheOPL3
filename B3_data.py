from tabulate import tabulate
from colorama import Fore, Back, Style, init


# Initialiser les couleurs pour le terminal
init(autoreset=True)

def read_file_transport(graph_number):
    """ Lit les données du problème de transport à partir d'un numéro de table.

    Retourne :
    size -- un tuple (nombre de fournisseurs, nombre de clients)
    couts -- une matrice des coûts de transport
    provisions -- une liste des provisions pour chaque fournisseur
    commandes -- une liste des commandes pour chaque client
    """
    nom_fichier = f"data/B3-table-{graph_number}.txt"
    with open(nom_fichier, 'r') as fichier:
        n, m = map(int, fichier.readline().split())
        couts = []
        provisions = []
        for _ in range(n):
            ligne = list(map(int, fichier.readline().split()))
            couts.append(ligne[:-1])  # Exclure la dernière valeur de la ligne, qui est la provision
            provisions.append(ligne[-1])  # Ajouter la provision à la liste des provisions
        commandes = list(map(int, fichier.readline().split()))

    return (n, m), couts, provisions, commandes


def load_graph_data(graph_number):
    """Charge les données pour un numéro de graphique spécifique et les stocke en mémoire."""
    try:
        taille, couts, provisions, commandes = read_file_transport(graph_number)
        return {
            "taille": taille,
            "couts": couts,
            "provisions": provisions,
            "commandes": commandes,
            "propositions": None
        }
    except FileNotFoundError:
        print("Fichier de données non trouvé. Veuillez vérifier la disponibilité du fichier.")
        return None
    except Exception as e:
        print(f"Une erreur est survenue lors du chargement des données: {e}")
        return None


def display_matrix(taille, couts, provisions, commandes, propositions, graph_number, penalites=None):
    """Affiche les données du problème de transport sous forme de tableau."""
    somme_provisions = sum(provisions)
    commandes_row = [Back.WHITE + Fore.BLACK + " Commandes " + Style.RESET_ALL] + [str(commande) for commande in commandes] + [str(somme_provisions)]

    headers = [Style.BRIGHT + f"C{i + 1}" + Style.RESET_ALL for i in range(taille[1])] + [Back.WHITE + Fore.BLACK + " Provisions " + Style.RESET_ALL]
    headers.insert(0, Fore.LIGHTGREEN_EX + str(graph_number) + Style.RESET_ALL)
    headers = [str(i) for i in headers]
    table = []

    for i in range(taille[0]):
        row = [Style.BRIGHT + f"P{i + 1}" + Style.RESET_ALL] + [Fore.LIGHTBLUE_EX + str(cout) + Style.RESET_ALL + " | " for cout in couts[i]]
        for j in range(taille[1]):
            row[j + 1] += Fore.LIGHTWHITE_EX + str(propositions[i][j]) + Style.RESET_ALL
        row.append(str(provisions[i]) + Style.RESET_ALL)
        table.append(row)
    table.append(commandes_row)

    if penalites:
        penalites_row = [Back.WHITE + Fore.BLACK + " Pénalités " + Style.RESET_ALL] + [str(p) for p in penalites]
        table.append(penalites_row)

    print(tabulate(table, headers=headers, tablefmt="rounded_grid", numalign="center", stralign="center"))


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
        print("L'arrête à ajouter pour l'obtention d'une proposition non dégénérée est P{}C{}".format(indice_minimal_i + 1, indice_minimal_j + 1))
        # retourner indice_minimal_i, indice_minimal_j
        return combinaison_minimale, indice_minimal_i, indice_minimal_j

    else:
        # Mettre à jour les coûts copiés pour exclure la proposition associée
        couts_temp[indice_minimal_i][indice_minimal_j] = float('inf')
        # Appeler récursivement la fonction en utilisant les copies modifiées
        combinaison_minimale = trouver_combinaison_minimale({'couts': couts_temp, 'propositions': graph_data['propositions']})

        return combinaison_minimale

# trouver_combinaison_minimale nous donne l'arête à ajouter pour obtenir une proposition non dégénérée si elle existe
# Fonction adjust_transport_table pour juster la table de transport : quand on doit ajouter une arête dans une cellule ligne/colonne, il faut lui donner une  delta (qui était avant à 0 car l'arête n'existait pas), il faut donc mettre à jour les autres cellules adjacentes en donnant ou en retirant delta
def adjust_transport_table(graph_data, combinaison_minimale):
    # Copie des données du graphe
    couts = [row[:] for row in graph_data['couts']]
    provisions = graph_data['provisions'][:]
    commandes = graph_data['commandes'][:]

    # Récupérer les indices de l'arête à ajouter
    i, j = combinaison_minimale

    # Trouver la valeur de l'arête à ajouter
    delta = min(provisions[i], commandes[j])

    # Mettre à jour les provisions et les commandes
    provisions[i] -= delta
    commandes[j] -= delta

    # Mettre à jour les coûts pour refléter l'ajout de l'arête
    couts[i][j] = delta

    # Mettre à jour les coûts pour les cellules adjacentes
    for k in range(len(provisions)):
        if k != i:
            couts[k][j] += delta
    for k in range(len(commandes)):
        if k != j:
            couts[i][k] += delta

    return {
        "taille": graph_data['taille'],
        "couts": couts,
        "provisions": provisions,
        "commandes": commandes,
        "propositions": graph_data['propositions'],
        "combinaison_minimale": combinaison_minimale
    }


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



