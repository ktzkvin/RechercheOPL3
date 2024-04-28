from graphviz import Digraph

def draw_transport_graph(graph_data):
    dot = Digraph()
    dot.attr(rankdir='LR', size='8,5')
    dot.node_attr.update(shape='circle')

    # Ajouter les nœuds des fournisseurs avec une couleur spécifique
    for i in range(graph_data['taille'][0]):
        dot.node(f'F{i+1}', f'S{i+1}', style='filled', color='lightblue')

    # Ajouter les nœuds des clients avec une autre couleur spécifique
    for j in range(graph_data['taille'][1]):
        dot.node(f'C{j+1}', f'L{j+1}', style='filled', color='peachpuff')

    # Ajouter les arcs avec les coûts et les propositions de transport
    for i, row in enumerate(graph_data['couts']):
        for j, cost in enumerate(row):
            # Utilisation de HTML pour le label
            label = f'{cost} <FONT COLOR="blue">({graph_data["propositions"][i][j]})</FONT>'
            dot.edge(f'F{i+1}', f'C{j+1}', label=f'<{label}>', fontcolor='black')

    dot.render('transport_graph', view=True)
