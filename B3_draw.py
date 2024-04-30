from graphviz import Digraph

# Fonction pour dessiner le graphe de transport
def draw_transport_graph(graph_data, graph_number, added_edges=None):
    """
    Dessiner le graphe de transport avec les propositions de transport
    :param graph_data: informations sur le graphe
    :param graph_number: numéro du graphe
    :param added_edges: arêtes ajoutées pour rendre le graphe connexe
    :return: affiche le graphe de transport
    """

    dot = Digraph()
    dot.attr(rankdir='LR', size='8,5')
    dot.node_attr.update(shape='circle', style='filled')

    is_connex = ""

    # Ajouter les nœuds des fournisseurs avec une couleur spécifique
    for i in range(graph_data['taille'][0]):
        dot.node(f'F{i+1}', f'P{i+1}', color='lightblue')

    # Ajouter les nœuds des clients avec une autre couleur spécifique
    for j in range(graph_data['taille'][1]):
        dot.node(f'C{j+1}', f'C{j+1}', color='peachpuff')

    # Ajouter les arcs avec les propositions de transport seulement si elles sont non nulles
    for i, row in enumerate(graph_data['couts']):
        for j, cost in enumerate(row):
            proposition = graph_data["propositions"][i][j]
            if proposition > 0:  # Vérifier si la proposition est non nulle
                # Utilisation de HTML pour la couleur du texte
                label = f'<{proposition} <FONT COLOR="blue">({cost})</FONT>>'
                edge_color = 'black'
                # Si l'arête est une des arêtes ajoutées et added_edges n'est pas None, la colorier en rouge
                if added_edges and (i, j) in added_edges:
                    edge_color = 'red'
                    is_connex = "non dégénéré"

                dot.attr(label=f"Graphe {graph_number} {is_connex}", fontsize='20')
                dot.edge(f'F{i+1}', f'C{j+1}', label=label, fontcolor=edge_color, color=edge_color, dir="none")

    dot.render(f'data/graph/transport_graph_{graph_number}', format='pdf', view=True)

# Fonction pour dessiner le graphe de transport avec les composants connexes
def draw_transport_graph_with_components(graph_data, graph_number, components):
    """
    Dessiner le graphe de transport avec les composants connexes identifiés
    :param graph_data: informations sur le graphe
    :param graph_number: numéro du graphe
    :param components: composants connexes identifiés
    :return: affiche le graphe de transport avec les composants connexes
    """
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

    dot.render(f'data/graph/transport_graph_{graph_number}_components', format='pdf', view=True)
