import networkx as nx

def generate_layout(concept_map):
    G = nx.Graph()
    for concept1, relation, concept2 in concept_map:
        G.add_node(concept1)
        G.add_node(concept2)
        G.add_edge(concept1, concept2)

    pos = nx.spring_layout(G, scale=1000)
    
    nodes = []
    for node, (x, y) in pos.items():
        nodes.append({
            'id': node,
            'data': {'label' : node},
            'position': {'x': x, 'y': y}
        })

    edges = []
    for concept1, concept2 in G.edges:
        edges.append({
            'id': f'{concept1}-{concept2}',
            'source': concept1,
            'target': concept2,
            'label': next(relation for c1, relation, c2 in concept_map if (c1 == concept1 and c2 == concept2) or (c1 == concept2 and c2 == concept1)),
            'animated': 'true'
        })
    
    return {'nodes': nodes, 'edges': edges}