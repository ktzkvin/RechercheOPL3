from B3_data import *
from colorama import Fore, Back, Style, init

# Initialiser les couleurs pour le terminal
init(autoreset=True)


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


# Menu principal
def main_menu(graph_data, graph_number):
    print(graph_data)
    continue_running = True
    while continue_running:
        print("\n\n╠═════════════════════ " + Fore.LIGHTWHITE_EX + "Menu Principal" + Fore.RESET + " ═════════════════════╣\n")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "1." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  ...")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "2." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  ...")
        print("  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "3." + Back.RESET + Fore.RESET + Style.RESET_ALL + "  ...")

        print("\n  " + Back.WHITE + Fore.BLACK + Style.BRIGHT + "0." + Back.RESET + Style.RESET_ALL + Fore.RED + "  Quitter")

        if graph_number < 10:
            print("\n╚" + "═" * 23 + Fore.LIGHTWHITE_EX + " Table : " + str(graph_number) + Fore.RESET + " " + "═" * 24 + "╝")
        else:
            print("\n╚" + "═" * 23 + Fore.LIGHTWHITE_EX + " Table : " + str(graph_number) + Fore.RESET + " " + "═" * 23 + "╝")

        try:
            print(Fore.LIGHTBLUE_EX + "\n┌─────────────────────")
            choice = int(input(Fore.LIGHTBLUE_EX + "█ Entrez votre choix : " + Style.RESET_ALL))
        except ValueError:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 4.")
            continue

        # Quitter le programme
        if choice == 0:
            print(Fore.RED + "\n✧" + Fore.RESET + " Programme quitté. " + Fore.RED + "✧\n" + Fore.RESET)
            break


        # Choix du menu
        elif choice in [1, 2, 3, 4]:
            '''# Lire + enregistrer les données de la table de contraintes sous forme de matrice
            constraints_table = matrice_table(graph_number)

            # Stockage du tableau de contraintes dans la mémoire
            graph_data = store_constraints_in_memory(constraints_table)  # Stockage du graphe en mémoire
            graph_data = {key: graph_data[key] for key in sorted(graph_data)}  # Trier par ordre de nœud
'''
            execute_choice(choice, graph_data, graph_number)

            # Ajout de la demande pour continuer ou quitter le programme
            if not continue_prompt():
                continue_running = False
                print(Fore.RED + "\n✧" + Fore.RESET + " Programme quitté. " + Fore.RED + "✧\n" + Fore.RESET)

        # Changer la table de contraintes
        elif choice == 5:
            new_graph_number = change_table()
            if new_graph_number is not None:
                graph_number = new_graph_number
                graph_data = load_graph_data(graph_number)
                print(Fore.GREEN + f"\nTable {graph_number} chargée avec succès." + Fore.RESET)
            else:
                print(Fore.RED + "\nChangement de table annulé." + Fore.RESET)

        else:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 4.")


# Fonction d'exécution du choix de menu
def execute_choice(choice, graph_data, graph_number):

    if choice == 1:

        print("\n\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "..." + Fore.RESET + " ─────────── ✦")
        if graph_data:
            propositions = [25, 0, 0], [10, 15, 0], [0, 5, 20]
            display_matrix(graph_data['taille'], graph_data['couts'], graph_data['provisions'], graph_data['commandes'], graph_number, propositions)
        else:
            print("Aucune donnée chargée. Veuillez charger les données.")

    elif choice == 2:

        print(Fore.RESET + "\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "..." + Fore.RESET + " ─────────── ✦\n")

    elif choice == 3:

        print(Fore.RESET + "\n✦ ─────────── " + Fore.LIGHTWHITE_EX + "..." + Fore.RESET + " ─────────── ✦\n")


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
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 4.")


# Lancer le programme
if __name__ == "__main__":
    while True:
        print("\n╔═══════════════════ " + Fore.LIGHTWHITE_EX + "Projet Graphe : B3" + Fore.RESET + " ═══════════════════╗")
        try:
            graph_number = int(input("\n" + Fore.LIGHTYELLOW_EX + "  ✦" + Style.RESET_ALL + " Entrez le numéro de la table de contraintes " + Fore.YELLOW + "" + Fore.LIGHTBLUE_EX + "(1-12)" + Fore.RESET + " : "))
            if 1 <= graph_number <= 12:
                graph_data = load_graph_data(graph_number)
                main_menu(graph_data, graph_number)
                break  # Sortir de la boucle si une entrée valide est fournie
            elif graph_number == 0:
                print(Fore.RED + "\n✧" + Fore.RESET + " Programme quitté. " + Fore.RED + "✧\n" + Fore.RESET)
                break  # Sortir de la boucle
            else:
                print(Fore.RED + "\n  ⚠" + Fore.RESET + " Veuillez entrer un chiffre entre 1 et 12.\n")
        except ValueError as e:
            print(Fore.RED + "\n  ⚠" + Fore.RESET + " [ERROR] Détail de l'erreur : " + Fore.RED + str(e) + "\n" + Style.RESET_ALL)

