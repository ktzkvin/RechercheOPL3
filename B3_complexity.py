# Fonction pour créer une matrice de données aléatoires
import random
import time
import matplotlib.pyplot as plt
from B3_transport_methods import *
from tqdm import tqdm



def create_random_matrix(n, m):
    """
    Crée une matrice de données aléatoires pour le problème de transport.
    :param n: Nombre de fournisseurs
    :param m: Nombre de clients
    :return: Dictionnaire contenant les données du problème de transport
    """
    matrice = {'taille': (n, m), 'couts': [], 'provisions': [], 'commandes': [], 'propositions': []}
    couts = [[random.randint(1, 100) for _ in range(m)] for _ in range(n)]  # Doit être n x m
    provisions = [random.randint(1, 100) for _ in range(n)]
    total_provisions = sum(provisions)
    commandes = [random.randint(1, total_provisions) for _ in range(m - 1)]
    commandes.append(total_provisions - sum(commandes))  # Équilibrer la dernière commande

    # Ajouter les valeurs dans la matrice
    matrice['couts'] = couts
    matrice['provisions'] = provisions
    matrice['commandes'] = commandes
    matrice['propositions'] = [[0] * m for _ in range(n)]  # Doit être n x m

    return matrice


def mesure_temps_execution(algo, graph_data):
    start_time = time.perf_counter()
    algo(graph_data)
    end_time = time.perf_counter()
    return end_time - start_time


def complex_analys():
    # Tailles de problème à tester
    sizes = [10, 30, 100]
    repetitions = 100  # Nombre de répétitions pour chaque taille

    # Dictionnaires pour stocker les temps d'exécution
    execution_times = {
        'nord_ouest': {size: [] for size in sizes},
        'balas_hammer': {size: [] for size in sizes},
    }

    # Boucle sur chaque taille de problème
    for size in sizes:
        for _ in tqdm(range(repetitions), desc=f"Running experiments for size {Fore.LIGHTWHITE_EX}{Back.RED} {size} {Style.RESET_ALL}"):
            graph_data = create_random_matrix(size, size)

            # Mesure du temps pour Nord-Ouest
            t_nord_ouest = mesure_temps_execution(nord_ouest_method, graph_data)
            execution_times['nord_ouest'][size].append(t_nord_ouest)

            # Mesure du temps pour Balas-Hammer
            t_balas_hammer = mesure_temps_execution(balas_hammer_method, graph_data)
            execution_times['balas_hammer'][size].append(t_balas_hammer)

    # print les résultats
    for algorithm, times in execution_times.items():
        print(f"Results for {algorithm}:")
        for size, times_list in times.items():
            print(f"Size {size}: {max(times_list)} seconds")

    # Tracé des résultats
    for algorithm, times in execution_times.items():
        max_times = [max(times[size]) for size in sizes]
        print(f"Max times for {algorithm}: {max_times}")  # Imprime les temps d'exécution max
        plt.plot(sizes, max_times, label=f'Max time {algorithm}')

    print(f"Sizes for x-axis: {sizes}")  # Imprime les tailles du problème pour l'axe des abscisses

    plt.xlabel('Size of problem n')
    plt.ylabel('Execution time (seconds)')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Complexity Analysis in the Worst Case')
    plt.legend()
    plt.grid(True)
    plt.show()
