import os
from colorama import Back, Fore, Style
from graphviz import Digraph


# Fonction pour dessiner le graphe de transport
def draw_transport_graph(graph_data, graph_number, added_edges):
    """
    Dessiner le graphe de transport avec les propositions de transport
    :param graph_data: informations sur le graphe
    :param graph_number: numéro du graphe
    :param added_edges: arêtes ajoutées pour rendre le graphe connexe
    :return: affiche le graphe de transport
    """
    try:

        dot = Digraph()
        dot.attr(rankdir='LR', size='8,5')
        dot.node_attr.update(shape='circle', style='filled')

        # Ajouter les nœuds des fournisseurs et des clients avec des couleurs spécifiques.
        for i in range(graph_data['taille'][0]):
            dot.node(f'F{i+1}', f'P{i+1}', color='lightblue')
        for j in range(graph_data['taille'][1]):
            dot.node(f'C{j+1}', f'C{j+1}', color='peachpuff')

        # Traitement et ajout des arêtes au graphique.
        for i, row in enumerate(graph_data['couts']):
            for j, cost in enumerate(row):
                proposition = graph_data["propositions"][i][j]
                edge_color = 'black'
                label = f'<{proposition} <FONT COLOR="blue">({cost})</FONT>>'

                # Gestion des arêtes ajoutées pour la connexité
                if added_edges and (i, j) in added_edges:
                    label = f'<0 <FONT COLOR="red">({cost})</FONT>>'  # Mettre en rouge avec la proposition à zéro
                    edge_color = 'red'

                if proposition > 0 or (added_edges and (i, j) in added_edges):
                    dot.edge(f'F{i+1}', f'C{j+1}', label=label, fontcolor=edge_color, color=edge_color, dir="none")

        # Configuration du label du graphe avec une indication si des modifications non dégénératives ont été apportées
        if added_edges:
            dot.attr(label=f"Graphe {graph_number} - Non Dégénéré", fontsize='20')
        else:
            dot.attr(label=f"Graphe {graph_number}", fontsize='20')

        # Enregistrer le fichier DOT et ouvrir la visualisation
        dot.render(f'data/graph/transport_graph_{graph_number}', format='pdf', view=False)

        file_path = f'data/graph/transport_graph_{graph_number}.pdf'

        file_uri = f"file:///{os.path.abspath(file_path).replace(os.sep, '/')}"
        print(f"\n{Back.BLUE}{Fore.LIGHTWHITE_EX}Graphe généré :{Style.RESET_ALL} {file_uri}")
        print("Cliquez sur le lien ci-dessus pour ouvrir le graphe.")

        try:
            from IPython.display import display, HTML
            display(HTML(f"<a href='{file_uri}' target='_blank'>Open Graph PDF</a>"))
        except ImportError:
            pass

    except RuntimeError as e:
        print(Fore.RED + "Erreur lors de la génération du graphe : assurez-vous d'avoir ajouté Graphviz au PATH.")
        print("Pour installer Graphviz sur Windows : " + Fore.LIGHTBLUE_EX + "https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/10.0.1/windows_10_cmake_Release_graphviz-install-10.0.1-win64.exe.sha256" + Style.RESET_ALL)
        print("Lors de l'installation, bien cocher la case " + Fore.LIGHTRED_EX + "'Add Graphviz to the system PATH for all users'." + Style.RESET_ALL)
        print("\nPour tout autre système d'exploitation, visiter : https://gitlab.com/graphviz/graphviz/-/releases")
        print(Fore.RED + str(e))

# Fonction pour dessiner le graphe de transport avec les composants connexes
def draw_transport_graph_with_components(graph_data, graph_number, components):
    """
    Dessiner le graphe de transport avec les composants connexes identifiés
    :param graph_data: informations sur le graphe
    :param graph_number: numéro du graphe
    :param components: composants connexes identifiés
    :return: affiche le graphe de transport avec les composants connexes
    """
    try:
        dot = Digraph()
        dot.attr(rankdir='LR', size='8,5')
        dot.node_attr.update(shape='circle', style='filled')
        dot.attr(label=f"Graphe {graph_number} - Sous Graphes", fontsize='20')


        # Dictionnaire pour stocker les couleurs des composants
        component_colors = ["hotpink", "lightgreen", "lightslateblue", "lightyellow", "violet", "lightcyan", "brown", "grey", "peachpuff", "pink"]
        color_map = {}

        num_fournisseurs, num_clients = graph_data['taille']

        # Assigner une couleur à chaque composant
        for index, component in enumerate(components):
            color = component_colors[index % len(component_colors)]
            for vertex in component:
                if vertex < num_fournisseurs:
                    node_id = f'F{vertex+1}'
                    node_label = f'P{vertex+1}'
                else:
                    node_id = f'C{vertex - num_fournisseurs + 1}'
                    node_label = f'C{vertex - num_fournisseurs + 1}'
                dot.node(node_id, node_label, style='filled', color=color)
                color_map[vertex] = color

        # Ajouter les arcs
        for i in range(num_fournisseurs):
            for j in range(num_clients):
                if graph_data['propositions'][i][j] > 0:
                    dot.edge(f'F{i+1}', f'C{j+1}', label=str(graph_data['propositions'][i][j]))

        dot.render(f'data/graph/transport_graph_{graph_number}_components', format='pdf', view=False)
        file_path = f'data/graph/transport_graph_{graph_number}_components.pdf'

        file_uri = f"file:///{os.path.abspath(file_path).replace(os.sep, '/')}"
        print(f"\n{Back.BLUE}{Fore.LIGHTWHITE_EX}Sous graphes générés :{Style.RESET_ALL} {file_uri}")
        print("Cliquez sur le lien ci-dessus pour ouvrir le graphe.")

    except RuntimeError as e:
        print(Fore.RED + "Erreur lors de la génération du graphe : assurez-vous d'avoir ajouté Graphviz au PATH.")
        print("Pour installer Graphviz sur Windows : " + Fore.LIGHTBLUE_EX + "https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/10.0.1/windows_10_cmake_Release_graphviz-install-10.0.1-win64.exe.sha256" + Style.RESET_ALL)
        print("Lors de l'installation, bien cocher la case " + Fore.LIGHTRED_EX + "'Add Graphviz to the system PATH for all users'." + Style.RESET_ALL)
        print("\nPour tout autre système d'exploitation, visiter : https://gitlab.com/graphviz/graphviz/-/releases")
        print(Fore.RED + str(e))
