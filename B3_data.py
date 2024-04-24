from tabulate import tabulate
from colorama import Fore, Back, Style, init

# Initialiser les couleurs pour le terminal
init(autoreset=True)

def read_file_transport(graph_number):
    """ Lit les données du problème de transport à partir d'un numéro de table.

    Arguments :
    graph_number -- le numéro de la table de transport à lire

    Retourne :
    taille -- un tuple (nombre de fournisseurs, nombre de clients)
    couts -- une matrice des coûts de transport
    provisions -- une liste des provisions pour chaque fournisseur
    commandes -- une liste des commandes pour chaque client
    """
    nom_fichier = f"data/B3-table-{graph_number}.txt"
    with open(nom_fichier, 'r') as fichier:
        ''' exemple fichier txt : 
        4 2
        50 20 100
        10 50 200
        50 40 100
        45 35 200
        300 300
        
        4 = nombre de fournisseurs
        2 = nombre de clients
        donc la matrice des couts est de taille 4x2
        ensuite la dernière ligne est les commandes des clients (300 300)
        et tout ce qui est avant est les provisions des fournisseurs, sans compter la dernière colonne qui est les provisions
        ex ici : 
        50 20 100 => 50 et 20 donc de la ligne P1 pour les colonnes respectives C1 et C2, alors que 100 sont les provisions de P1
        10 50 200 => 10 et 50 donc de la ligne P2 pour les colonnes respectives C1 et C2, alors que 200 sont les provisions de P2
        50 40 100 => 50 et 40 donc de la ligne P3 pour les colonnes respectives C1 et C2, alors que 100 sont les provisions de P3
        45 35 200 => 45 et 35 donc de la ligne P4 pour les colonnes respectives C1 et C2, alors que 200 sont les provisions de P4
        300 300 => 300 et 300 donc les commandes des clients C1 et C2
   

        n, m = map(int, fichier.readline().split())
        couts = [list(map(int, fichier.readline().split())) for _ in range(n)]
        provisions = list(map(int, fichier.readline().split()))
        commandes = list(map(int, fichier.readline().split()))
        me donnent :
        n, m = (4, 2)
        couts = [[5, 7, 8, 25], [6, 8, 5, 25], [6, 7, 7, 25]]
        provisions = [35, 20, 20]
        commandes = []
        
        donc ne marche pas hormis pour n et m
        moi je veux:
        
        n, m = (4, 2)
        couts = [[50, 20], [10, 50], [50, 40], [45, 35]]
        provisions = [100, 200, 100, 200]
        commandes = [300, 300]
        '''
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
            "commandes": commandes
        }
    except FileNotFoundError:
        print("Fichier de données non trouvé. Veuillez vérifier la disponibilité du fichier.")
        return None
    except Exception as e:
        print(f"Une erreur est survenue lors du chargement des données: {e}")
        return None


def display_matrix(taille, couts, provisions, commandes, graph_number):
    headers = [Style.BRIGHT + f"C{i + 1}" + Style.RESET_ALL for i in range(taille[1])] + [Back.WHITE + Fore.BLACK + " Provisions " + Style.RESET_ALL]
    headers.insert(0, Fore.LIGHTGREEN_EX + str(graph_number) + Style.RESET_ALL)
    headers = [str(i) for i in headers]
    table = []

    # Ajouter les lignes des fournisseurs avec les coûts et les provisions
    for i in range(taille[0]):
        row = [Style.BRIGHT + f"P{i + 1}" + Style.RESET_ALL] + [Fore.LIGHTBLUE_EX + str(cout) + Style.RESET_ALL for cout in couts[i]] + [str(provisions[i])]
        table.append(row)

    # Ajouter la ligne des commandes
    commandes_row = [Back.WHITE + Fore.BLACK + " Commandes " + Style.RESET_ALL] + [str(commande) for commande in commandes]
    table.append(commandes_row)

    print(tabulate(table, headers=headers, tablefmt="rounded_grid", numalign="center", stralign="center"))