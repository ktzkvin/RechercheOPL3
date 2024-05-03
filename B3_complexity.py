# Fonction pour créer une matrice de données aléatoires
import random


def create_random_matrix(n, m):
    """
    Crée une matrice de données aléatoires pour le problème de transport.
    :param n: Nombre de fournisseurs
    :param m: Nombre de clients
    :return: Dictionnaire contenant les données du problème de transport
    """
    matrice = {'taille': (n, m), 'couts': [], 'provisions': [], 'commandes': [], 'propositions': []}
    couts = []
    provisions = []
    commandes = []
    for i in range(n):
        couts.append([])
        for j in range(m):
            couts[i].append(random.randint(0, 100))

    for i in range(n):
        provisions.append(random.randint(0, 300))

    for i in range(m):
        commandes.append(random.randint(0, 300))

    # Ajouter les valeurs dans la matrice
    matrice['taille'] = (n, m)
    matrice['couts'] = couts
    matrice['provisions'] = provisions
    matrice['commandes'] = commandes
    for i in range(n):
        matrice['propositions'].append([0] * m)

    return matrice
