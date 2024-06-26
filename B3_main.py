from B3_data import *
from B3_draw import *
from B3_complexity import *
from B3_transport_methods import *
from colorama import Fore, Back, Style, init

# Initialiser les couleurs pour le terminal
init(autoreset=True)


def is_connex(graph_data, graph_number):
    """
    Vérifie si le graphe est connexe et propose des arêtes pour le rendre connexe.
    :param graph_data:
    :param graph_number:
    :return:
    """
    print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Proposition de transport" + Fore.RESET + " ─────────── ✦")
    display_matrix_transport(graph_data, graph_number)
    print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Connexité du graphe" + Fore.RESET + " ─────────── ✦")

    added_edges = []
    ignored_edges = set()

    if bfs_connexity(graph_data):
        print(f"\nLe réseau de transport est {Back.GREEN}{Fore.LIGHTWHITE_EX} déjà connexe {Style.RESET_ALL}.")
    else:
        print(f"\nLe réseau de transport {Back.RED}{Fore.LIGHTWHITE_EX} n'est pas connexe {Style.RESET_ALL}.")

        # Identifier et afficher les sous-graphes connexes
        components = find_connected_components(graph_data)

        draw_transport_graph_with_components(graph_data, graph_number, components)

        # Trouver les arêtes minimales pour rendre le graphe connexe
        while not bfs_connexity(graph_data):
            combinaison_minimale = trouver_combinaison_minimale(graph_data, ignored_edges)
            if combinaison_minimale is None:
                print("Aucune autre arête ne peut être ajoutée sans créer de cycle.")
                break
            i, j = combinaison_minimale

            is_cycle, path = detect_cycle_with_edge(graph_data, (i, j), added_edges)
            if not is_cycle:
                graph_data['propositions'][i][j] += 1
                added_edges.append((i, j))
                print(f"L'arête {Fore.LIGHTBLUE_EX}P{i + 1}{Style.RESET_ALL}-{Fore.LIGHTMAGENTA_EX}C{j + 1}{Style.RESET_ALL} a été ajoutée pour améliorer la connexité.")

            else:
                # Associer chaque tuple de path à un sommet
                print(f"Impossible d'ajouter l'arête P{i + 1}-C{j + 1} car cela créerait un cycle : {path}")
                ignored_edges.add((i, j))

        print(f"\nLe réseau de transport est maintenant {Back.GREEN}{Fore.LIGHTWHITE_EX} connexe {Style.RESET_ALL}.")

    # remettre toutes les propositions de added_edges à 0
    for edge in added_edges:
        graph_data['propositions'][edge[0]][edge[1]] = 0

    draw_transport_graph(graph_data, graph_number, added_edges)
    return added_edges


# Fonction pour mettre en pause (demande pour continuer ou non)
def continue_prompt():
    while True:  # Boucle jusqu'à ce que l'utilisateur donne une réponse valide
        user_input = input("\n" + Fore.LIGHTBLUE_EX + "Souhaitez-vous continuer ? [" + Fore.GREEN + "y" + Fore.LIGHTBLUE_EX + "/" + Fore.RED + "n" + Fore.LIGHTBLUE_EX + "] " + Style.RESET_ALL).lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print(Fore.RED + "Choix invalide, veuillez entrer 'y' pour oui ou 'n' pour non." + Fore.RESET)


# Fonction pour mettre en pause pour les coûts marginaux (demande pour continuer ou non)
def continue_prompt_marg():
    while True:  # Boucle jusqu'à ce que l'utilisateur donne une réponse valide
        user_input = input("\n" + Fore.RED + "Une valeur des coûts marginaux a de nouveau été détectée négative, refaire une itération ? "+ Fore.BLUE + "[" + Fore.GREEN + "y" + Fore.LIGHTBLUE_EX + "/" + Fore.RED + "n" + Fore.LIGHTBLUE_EX + "] " + Style.RESET_ALL).lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print(Fore.RED + "Choix invalide, veuillez entrer 'y' pour oui ou 'n' pour non." + Fore.RESET)



# Menu principal
def main_menu(graph_data, graph_number):
    continue_running = True
    added_edges = []
    while continue_running:
        print("\n\n╠═════════════════════ " + Fore.LIGHTWHITE_EX + "Menu Principal" + Fore.RESET + " ═════════════════════╣\n")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "1." + Back.RESET + Fore.RESET + Style.RESET_ALL + " Matrice des coûts")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "2." + Back.RESET + Fore.RESET + Style.RESET_ALL + " Proposition de transport (NO/BH)")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "3." + Back.RESET + Fore.RESET + Style.RESET_ALL + " Connexité du graphe")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "4." + Back.RESET + Fore.RESET + Style.RESET_ALL + " Calcul des coûts potentiels")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "5." + Back.RESET + Fore.RESET + Style.RESET_ALL + " Calcul des coûts marginaux")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "6." + Back.RESET + Fore.RESET + Style.RESET_ALL + " Coûts Totaux")

        print("\n  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "8. BONUS " + Back.RESET + Fore.RESET + Style.RESET_ALL + " Dessiner le graphe")

        print("\n  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "9." + Back.RESET + Fore.RESET + Style.RESET_ALL + " Changer le tableau de contraintes")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "0." + Back.RESET + Style.RESET_ALL + Fore.RED + "  Quitter")

        if graph_number < 10:
            print("\n╚" + "═" * 23 + Fore.LIGHTWHITE_EX + " Table : " + str(graph_number) + Fore.RESET + " " + "═" * 24 + "╝")
        else:
            print("\n╚" + "═" * 23 + Fore.LIGHTWHITE_EX + " Table : " + str(graph_number) + Fore.RESET + " " + "═" * 23 + "╝")

        try:
            print(Fore.LIGHTBLUE_EX + "\n┌─────────────────────")
            choice = int(input(Fore.LIGHTBLUE_EX + "█ Entrez votre choix : " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 9.")
            continue

        # Quitter le programme
        if choice == 0:
            print(Fore.RED + "\n✧" + Fore.RESET + " Programme quitté. " + Fore.RED + "✧\n" + Fore.RESET)
            break


        # Choix du menu
        elif choice in [1, 2, 3, 4, 5, 6, 7, 8]:

            added_edges = execute_choice(choice, graph_data, graph_number, added_edges)

            # Ajout de la demande pour continuer ou quitter le programme
            if not continue_prompt():
                continue_running = False
                print(Fore.RED + "\n✧" + Fore.RESET + " Programme quitté. " + Fore.RED + "✧\n" + Fore.RESET)

        # Changer la table de contraintes
        elif choice == 9:
            new_graph_number = change_table()
            if new_graph_number is not None:
                graph_number = new_graph_number
                graph_data = load_graph_data(graph_number)
                print(Fore.GREEN + f"\nTable {graph_number} chargée avec succès." + Fore.RESET)
            else:
                print(Fore.RED + "\nChangement de table annulé." + Fore.RESET)

        else:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 9.")


# Fonction d'exécution du choix de menu
def execute_choice(choice, graph_data, graph_number, added_edges):
    if choice == 1:

        print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Matrice des coûts" + Fore.RESET + " ─────────── ✦")
        display_matrix_cost_only(graph_data['taille'], graph_data['couts'], graph_data['provisions'], graph_data['commandes'], graph_number)

    elif choice == 2:
        print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Proposition de Transport" + Fore.RESET + " ─────────── ✦")

        # Demander à l'utilisateur de choisir l'algorithme
        print("\nChoisissez l'algorithme à utiliser :")
        print("1. Algorithme de "+ Fore.LIGHTWHITE_EX + Back.GREEN + " Nord-Ouest " + Style.RESET_ALL)
        print("2. Algorithme de "+ Fore.LIGHTWHITE_EX + Back.BLUE + " Balas-Hammer " + Style.RESET_ALL)

        print(Fore.LIGHTBLUE_EX + "\n┌─────────────────────")
        algo_choice = int(input(Fore.LIGHTBLUE_EX + "█ Entrez votre choix : " + Style.RESET_ALL))

        # Méthode de Nord-Ouest
        if algo_choice == 1:
            graph_data['propositions'] = nord_ouest_method(graph_data)

        # Méthode de Balas-Hammer
        elif algo_choice == 2:
            graph_data['propositions'] = balas_hammer_method(graph_data, True)

        else:
            print("Choix invalide. Veuillez entrer 1 ou 2 pour sélectionner l'algorithme.")

        print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Proposition de transport" + Fore.RESET + " ─────────── ✦")
        display_matrix_transport(graph_data, graph_number)

    elif choice == 3:

        # Demander à l'utilisateur de choisir l'algorithme
        print("\nChoisissez l'algorithme à utiliser :")
        print("1. Algorithme de " + Fore.LIGHTWHITE_EX + Back.GREEN + " Nord-Ouest " + Style.RESET_ALL)
        print("2. Algorithme de " + Fore.LIGHTWHITE_EX + Back.BLUE + " Balas-Hammer " + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "\n┌─────────────────────")
        algo_choice = int(input(Fore.LIGHTBLUE_EX + "█ Entrez votre choix : " + Style.RESET_ALL))

        # Méthode de Nord-Ouest
        if algo_choice == 1:
            graph_data['propositions'] = nord_ouest_method(graph_data)

        # Méthode de Balas-Hammer
        elif algo_choice == 2:
            graph_data['propositions'] = balas_hammer_method(graph_data, True)

        added_edges = is_connex(graph_data, graph_number)
        return added_edges

    elif choice == 4:

        # Demander à l'utilisateur de choisir l'algorithme
        print("\nChoisissez l'algorithme à utiliser :")
        print("1. Algorithme de " + Fore.LIGHTWHITE_EX + Back.GREEN + " Nord-Ouest " + Style.RESET_ALL)
        print("2. Algorithme de " + Fore.LIGHTWHITE_EX + Back.BLUE + " Balas-Hammer " + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "\n┌─────────────────────")
        algo_choice = int(input(Fore.LIGHTBLUE_EX + "█ Entrez votre choix : " + Style.RESET_ALL))

        # Méthode de Nord-Ouest
        if algo_choice == 1:
            graph_data['propositions'] = nord_ouest_method(graph_data)

        # Méthode de Balas-Hammer
        elif algo_choice == 2:
            graph_data['propositions'] = balas_hammer_method(graph_data, True)

        added_edges = is_connex(graph_data, graph_number)

        print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Calcul des coûts potentiels" + Fore.RESET + " ─────────── ✦")

        print("\nCalcul des potentiels :")
        potentiel = calcul_potentiels(graph_data, added_edges)
        couts_potentiel_tab = calcul_couts_potentiels(graph_data, potentiel)
        display_matrix_2d(couts_potentiel_tab, graph_number,"potentiels")

        return added_edges

    elif choice == 5:

        # Demander à l'utilisateur de choisir l'algorithme
        print("\nChoisissez l'algorithme à utiliser :")
        print("1. Algorithme de " + Fore.LIGHTWHITE_EX + Back.GREEN + " Nord-Ouest " + Style.RESET_ALL)
        print("2. Algorithme de " + Fore.LIGHTWHITE_EX + Back.BLUE + " Balas-Hammer " + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "\n┌─────────────────────")
        algo_choice = int(input(Fore.LIGHTBLUE_EX + "█ Entrez votre choix : " + Style.RESET_ALL))

        # Méthode de Nord-Ouest
        if algo_choice == 1:
            graph_data['propositions'] = nord_ouest_method(graph_data)

        # Méthode de Balas-Hammer
        elif algo_choice == 2:
            graph_data['propositions'] = balas_hammer_method(graph_data, True)

        added_edges = is_connex(graph_data, graph_number)

        print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Calcul des coûts marginaux" + Fore.RESET + " ─────────── ✦")
        new_potentiels = None
        potentiel = calcul_potentiels(graph_data, added_edges)
        couts_potentiel_tab = calcul_couts_potentiels(graph_data, potentiel)
        couts_marginaux_tab = calcul_couts_marginaux(graph_data, couts_potentiel_tab)

        display_matrix_2d(couts_potentiel_tab, graph_number,"potentiels")
        display_matrix_2d(couts_marginaux_tab, graph_number,"marginaux")

        # vérification technique marchepied : vérifier si les coûts marginaux sont négatifs
        i, j = is_marginal_negative(couts_marginaux_tab)
        k = 0
        while i is not None:
            print(f" --------------------------------- Itération : {k} --------------------------------- ")
            print(f"Le coût marginal de l'arête {Fore.LIGHTBLUE_EX}P{i + 1}{Style.RESET_ALL}-{Fore.LIGHTMAGENTA_EX}C{j+1}{Style.RESET_ALL} est négatif.")
            graph_data['propositions'] = stepping_stone_method(graph_data, i, j, added_edges)

            # Afficher le tableau de nouvelle proposition de transport
            print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Nouvelle proposition de transport" + Fore.RESET + " ─────────── ✦")
            display_matrix_transport(graph_data, graph_number)

            new_potentiel = calcul_potentiels(graph_data, added_edges)
            couts_potentiel_tab = calcul_couts_potentiels(graph_data, potentiel)
            couts_marginaux_tab = calcul_couts_marginaux(graph_data, couts_potentiel_tab)

            display_matrix_2d(couts_potentiel_tab, graph_number, "potentiels")
            display_matrix_2d(couts_marginaux_tab, graph_number, "marginaux")

            i, j = is_marginal_negative(couts_marginaux_tab)

            # pause pour continuer ou non
            if (i is not None and not continue_prompt_marg()) or new_potentiel == potentiel:
                break
            k += 1

            potentiel = new_potentiel
        return added_edges

    elif choice == 6:

        # Demander à l'utilisateur de choisir l'algorithme
        print("\nChoisissez l'algorithme à utiliser :")
        print("1. Algorithme de " + Fore.LIGHTWHITE_EX + Back.GREEN + " Nord-Ouest " + Style.RESET_ALL)
        print("2. Algorithme de " + Fore.LIGHTWHITE_EX + Back.BLUE + " Balas-Hammer " + Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "\n┌─────────────────────")
        algo_choice = int(input(Fore.LIGHTBLUE_EX + "█ Entrez votre choix : " + Style.RESET_ALL))

        # Méthode de Nord-Ouest
        if algo_choice == 1:
            graph_data['propositions'] = nord_ouest_method(graph_data)

        # Méthode de Balas-Hammer
        elif algo_choice == 2:
            graph_data['propositions'] = balas_hammer_method(graph_data, True)

        added_edges = is_connex(graph_data, graph_number)

        k = 0
        print(f"\n --------------------------------- Itération : {k} --------------------------------- ")

        print("\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Calcul des coûts marginaux" + Fore.RESET + " ─────────── ✦")

        new_potentiel = None
        potentiel = calcul_potentiels(graph_data, added_edges)
        couts_potentiel_tab = calcul_couts_potentiels(graph_data, potentiel)
        couts_marginaux_tab = calcul_couts_marginaux(graph_data, couts_potentiel_tab)

        display_matrix_2d(couts_potentiel_tab, graph_number,"potentiels")
        display_matrix_2d(couts_marginaux_tab, graph_number,"marginaux")

        # vérification technique marchepied : vérifier si les coûts marginaux sont négatifs
        i, j = is_marginal_negative(couts_marginaux_tab)

        while i is not None:
            k += 1
            print(f"\n --------------------------------- Itération : {k} --------------------------------- \n")
            print(f"Le coût marginal de l'arête {Fore.LIGHTBLUE_EX}P{i + 1}{Style.RESET_ALL}-{Fore.LIGHTMAGENTA_EX}C{j + 1}{Style.RESET_ALL} est négatif.")

            # revérifier si connexe, si c'est non, relancer is_connex
            if not bfs_connexity(graph_data):
                added_edges = is_connex(graph_data, graph_number)

            graph_data['propositions'] = stepping_stone_method(graph_data, i, j, added_edges)

            # Afficher le tableau de nouvelle proposition de transport
            print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Nouvelle proposition de transport" + Fore.RESET + " ─────────── ✦")
            display_matrix_transport(graph_data, graph_number)

            new_potentiel = calcul_potentiels(graph_data, added_edges)
            couts_potentiel_tab = calcul_couts_potentiels(graph_data, new_potentiel)
            couts_marginaux_tab = calcul_couts_marginaux(graph_data, couts_potentiel_tab)

            display_matrix_2d(couts_potentiel_tab, graph_number, "potentiels")
            display_matrix_2d(couts_marginaux_tab, graph_number, "marginaux")

            i, j = is_marginal_negative(couts_marginaux_tab)

            # pause pour continuer ou non
            if (i is not None and not continue_prompt_marg()) or new_potentiel == potentiel:
                break
            potentiel = new_potentiel
        print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Coûts totaux" + Fore.RESET + " ─────────── ✦")

        cout_totaux(graph_data)
        return added_edges

    elif choice == 8:

        print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Représentation du graphe" + Fore.RESET + " ─────────── ✦")
        draw_transport_graph(graph_data, graph_number, added_edges)



# Fonction pour changer la table de contraintes
def change_table():

    print("\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "Changement de la table de contraintes" + Fore.RESET + " ─────────── ✦\n")

    while True:
        try:
            new_graph_number = int(input(Fore.LIGHTYELLOW_EX + "  ✦" + Style.RESET_ALL + " Entrez le nouveau numéro de la table de contraintes " + Fore.YELLOW + "" + Fore.LIGHTBLUE_EX + "(1-12)" + Fore.RESET + " : "))
            if 1 <= new_graph_number <= 12:
                print("\nTable de contraintes changée.\n")
                return new_graph_number
            else:
                print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 12.\n")
        except ValueError:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 9.")


# Lancer le programme
if __name__ == "__main__":
    while True:
        print("\n╔═══════════════════ " + Fore.LIGHTWHITE_EX + "Projet Graphe : B3" + Fore.RESET + " ═══════════════════╗")
        graph_number = int(input("\n" + Fore.LIGHTYELLOW_EX + "  ✦" + Style.RESET_ALL + " Entrez le numéro de la table de contraintes " + Fore.YELLOW + "" + Fore.LIGHTBLUE_EX + "(1-12)" + Fore.RESET + " : " +
                                 "\n" + Fore.LIGHTYELLOW_EX + "  ✦" + Style.RESET_ALL + " Ou bien entrez " + Fore.YELLOW + "" + Fore.LIGHTYELLOW_EX + "0" + Fore.RESET + " pour lancer la simulation de complexité : "))
        if 1 <= graph_number <= 12:
            graph_data = load_graph_data(graph_number)

            # Initialiser propositions avec des zéros en fonction de graph_data['taille']
            propositions = [[0] * graph_data['taille'][1] for _ in range(graph_data['taille'][0])]

            # Assigner propositions à graph_data['propositions']
            graph_data['propositions'] = propositions

            main_menu(graph_data, graph_number)
            break  # Sortir de la boucle si une entrée valide est fournie
        elif graph_number == 0:
            complex_analys()
        else:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 12.\n")
