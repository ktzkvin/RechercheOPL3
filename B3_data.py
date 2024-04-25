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


def display_matrix(taille, couts, provisions, commandes, graph_number, propositions):
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