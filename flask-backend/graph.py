# For graph creation and layout generation
import networkx as nx

def generate_layout(concept_map):
    """
    Generate a graph layout from a concept map.

    Args:
        concept_map (list): A list of tuples representing the concept map, 
                            where each tuple is (concept1, relation, concept2).

    Returns:
        dict: A dictionary containing nodes and edges with their positions and labels.
    """
    # Create an empty undirected graph
    G = nx.Graph()

    # Add nodes and edges to the graph based on the concept map
    for concept1, relation, concept2 in concept_map:
        G.add_node(concept1)
        G.add_node(concept2)
        G.add_edge(concept1, concept2)

    # Generate positions for the nodes using a spring layout algorithm
    # The scale parameter controls the spacing of the layout
    pos = nx.spring_layout(G, scale=1000)
    
    # Prepare the nodes for the output
    nodes = []
    for node, (x, y) in pos.items():
        nodes.append({
            'id': node,
            'data': {'label' : node},
            'position': {'x': x, 'y': y}
        })

    # Prepare the edges for the output
    edges = []
    for concept1, concept2 in G.edges:
        edges.append({
            'id': f'{concept1}-{concept2}',
            'source': concept1,
            'target': concept2,
            'label': next(relation for c1, relation, c2 in concept_map if (c1 == concept1 and c2 == concept2) or (c1 == concept2 and c2 == concept1)),
            'animated': 'true'
        })
    
    # Return the graph as a dictionary containing nodes and edges
    return {'nodes': nodes, 'edges': edges}