from graphviz import Digraph

def draw_transport_graph(graph_data, graph_number, arete_ameliorante=None):
    dot = Digraph()
    dot.attr(rankdir='LR', size='8,5')
    dot.node_attr.update(shape='circle', style='filled')

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
                # Utilisation de HTML pour le label
                label = f'<{proposition} <FONT COLOR="blue">({cost})</FONT>>'
                dot.edge(f'F{i+1}', f'C{j+1}', label=label, fontcolor='black', dir='none')

    # Ajouter les arêtes améliorantes si elles sont fournies
    if arete_ameliorante:
        i, j = arete_ameliorante
        dot.edge(f'F{i+1}', f'C{j+1}', color='red', style='bold', dir='none')

    dot.render(f'data/graph/transport_graph_{graph_number}', format='pdf', view=True)