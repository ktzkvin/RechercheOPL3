# B3_data.py

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
        n, m = map(int, fichier.readline().split())
        couts = [list(map(int, fichier.readline().split())) for _ in range(n)]
        provisions = list(map(int, fichier.readline().split()))
        commandes = list(map(int, fichier.readline().split()))

    return (n, m), couts, provisions, commandes


def display_matrix(taille, couts, provisions, commandes):
    """Affiche la matrice des coûts ainsi que les vecteurs de provisions et de commandes."""
    n, m = taille
    print("Matrice des coûts:")
    for i, ligne in enumerate(couts):
        print("P{}: {}".format(i + 1, '  '.join(map(str, ligne))))
    print("Provisions:", '  '.join(map(str, provisions)))
    print("Commandes:", '  '.join(map(str, commandes)))


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