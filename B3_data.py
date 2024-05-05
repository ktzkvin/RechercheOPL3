from tabulate import tabulate
from colorama import Fore, Back, Style, init


# Initialiser les couleurs pour le terminal
init(autoreset=True)

# Fonction pour mettre en pause (demande pour continuer ou non)
def read_file_transport(graph_number):
    """
    Lit les données du problème de transport à partir d'un fichier texte.
    :param graph_number: Numéro de la table de contraintes
    :return: Tuple contenant les données du problème de transport
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


# Fonction pour charger les données du problème de transport
def load_graph_data(graph_number):
    """
    Charge les données du problème de transport à partir d'un numéro de table.
    :param graph_number: Numéro de la table de contraintes
    :return: Dictionnaire contenant les données du problème de transport
    """
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


# Fonction pour afficher les données du problème de transport sous forme de tableau
def display_matrix_transport(graph_data, graph_number):
    """
    Affiche les données du problème de transport sous forme de tableau.
    :param taille: Tuple (nombre de fournisseurs, nombre de clients)
    :param couts: Matrice des coûts de transport
    :param provisions: Liste des provisions pour chaque fournisseur
    :param commandes: Liste des commandes pour chaque client
    :param propositions: Matrice des propositions de transport
    :param graph_number: Numéro de la table de contraintes
    :return: None
    """
    # Initialisation
    taille = graph_data["taille"]
    couts = graph_data["couts"]
    provisions = graph_data["provisions"]
    commandes = graph_data["commandes"]
    propositions = graph_data["propositions"]

    # Calculer la somme des valeurs de provisions
    somme_provisions = sum(provisions)

    # Ajouter la somme des provisions à la dernière ligne des commandes
    commandes_row = [Back.WHITE + Fore.BLACK + " Commandes " + Style.RESET_ALL] + [str(commande) for commande in commandes] + [str(somme_provisions)]

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
    table.append(commandes_row)

    print(tabulate(table, headers=headers, tablefmt="grid", numalign="center", stralign="center"))



# Fonction pour afficher les données du problème de transport sous forme de tableau
def display_matrix_cost_only(taille, couts, provisions, commandes, graph_number):
    """
    Affiche les données du problème de transport sous forme de tableau.
    :param taille: Tuple (nombre de fournisseurs, nombre de clients)
    :param couts: Matrice des coûts de transport
    :param provisions: Liste des provisions pour chaque fournisseur
    :param commandes: Liste des commandes pour chaque client
    :param graph_number: Numéro de la table de contraintes
    :return: None
    """
    # Calculer la somme des valeurs de provisions
    somme_provisions = sum(provisions)

    # Ajouter la somme des provisions à la dernière ligne des commandes
    commandes_row = [Back.WHITE + Fore.BLACK + " Commandes " + Style.RESET_ALL] + [str(commande) for commande in commandes] + [str(somme_provisions)]

    headers = [Style.BRIGHT + f"C{i + 1}" + Style.RESET_ALL for i in range(taille[1])] + [Back.WHITE + Fore.BLACK + " Provisions " + Style.RESET_ALL]
    headers.insert(0, Fore.LIGHTGREEN_EX + str(graph_number) + Style.RESET_ALL)
    headers = [str(i) for i in headers]
    table = []

    # Ajouter les lignes des fournisseurs avec les coûts et les provisions
    for i in range(taille[0]):
        row = [Style.BRIGHT + f"P{i + 1}" + Style.RESET_ALL] + [Fore.LIGHTBLUE_EX + str(cout) + Style.RESET_ALL for cout in couts[i]]

        row.append(str(provisions[i]) + Style.RESET_ALL)
        table.append(row)

    # Ajouter la ligne des commandes
    table.append(commandes_row)

    print(tabulate(table, headers=headers, tablefmt="grid", numalign="center", stralign="center"))


def display_matrix_2d(tableau, graph_number, type_tab):
    """
    Affiche les coûts et les potentiels sous forme de tableau.
    :param tableau: Tableau contenant les coûts et les potentiels
    :return: None
    """

    headers = [Style.BRIGHT + f"C{i + 1}" + Style.RESET_ALL for i in range(len(tableau[0]))]
    headers.insert(0, Fore.LIGHTGREEN_EX + str(graph_number) + Style.RESET_ALL)
    headers = [str(i) for i in headers]
    table = []

    for i in range(len(tableau)):
        row = [Style.BRIGHT + f"P{i + 1}" + Style.RESET_ALL] + [Fore.LIGHTBLUE_EX + str(cout) + Style.RESET_ALL for cout in tableau[i]]
        table.append(row)

    print(f"\n Table des coûts {type_tab}:")
    print(tabulate(table, headers=headers, tablefmt="grid", numalign="center", stralign="center"))

