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


def display_matrix(taille, couts, provisions, commandes, propositions, graph_number):
    """Affiche les données du problème de transport sous forme de tableau."""
    headers = [Style.BRIGHT + f"C{i + 1}" + Style.RESET_ALL for i in range(taille[1])] + [Back.WHITE + Fore.BLACK + " Provisions " + Style.RESET_ALL]
    headers.insert(0, Fore.LIGHTGREEN_EX + str(graph_number) + Style.RESET_ALL)
    headers = [str(i) for i in headers]
    table = []

    # Ajouter les lignes des fournisseurs avec les coûts et les provisions
    for i in range(taille[0]):
        row = [Style.BRIGHT + f"P{i + 1}" + Style.RESET_ALL] + [Fore.LIGHTBLUE_EX + str(cout) + Style.RESET_ALL + " | " for cout in couts[i]]
        for j in range(taille[1]):
            row[j + 1] += Fore.LIGHTWHITE_EX + str(propositions[i][j]) + Style.RESET_ALL

        row.append(str(provisions[i]) + Style.RESET_ALL)
        table.append(row)

    # Ajouter la ligne des commandes
    commandes_row = [Back.WHITE + Fore.BLACK + " Commandes " + Style.RESET_ALL] + [str(commande) for commande in commandes]
    table.append(commandes_row)

    print(tabulate(table, headers=headers, tablefmt="rounded_grid", numalign="center", stralign="center"))

def connexe(graph_data):
        row_column=graph_data['taille'][0] + graph_data['taille'][1]

        notzero = 0
        for proposition in graph_data['propositions']:
            for valeur in proposition:
                if valeur != 0:
                    notzero += 1
        print("test")
        if notzero+1 == row_column:
            print('Diagramme connexe')
        else:
            print('Diagramme non connexe')

        print(trouver_combinaison_minimale(graph_data))


def trouver_combinaison_minimale(graph_data):
    # Trouver la valeur minimale dans les coûts
    couts_minimaux = min(min(row) for row in graph_data['couts'])
    #print(couts_minimaux)

    # Parcourir les coûts pour trouver l'indice de la valeur minimale
    for i, row in enumerate(graph_data['couts']):
        for j, cout in enumerate(row):
            if cout == couts_minimaux:
                indice_minimal_i = i
                indice_minimal_j = j
                break
    #print(indice_minimal_i, indice_minimal_j)

    # Vérifier si la proposition associée a une valeur nulle
    if graph_data['propositions'][indice_minimal_i][indice_minimal_j] == 0:
        print("La combinaison minimale est S{}C{}".format(indice_minimal_i + 1, indice_minimal_j + 1))

    else:
        # Mettre à jour les coûts pour exclure la proposition associée
        graph_data['couts'][indice_minimal_i][indice_minimal_j] = float('inf')
        #print("La combinaison est pas égale à 0")
        trouver_combinaison_minimale(graph_data)


def nord_ouest(graph_data):
    d=1
