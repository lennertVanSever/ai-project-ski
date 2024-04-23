import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(graph, path=None):
    pos = nx.spring_layout(graph)  # positions for all nodes

    # Draw the nodes
    nx.draw_networkx_nodes(graph, pos, node_size=700)

    # Draw the edges
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), width=2)

    # Draw labels
    nx.draw_networkx_labels(graph, pos, font_size=12, font_family='sans-serif')

    # Draw edge labels to show weights and times
    edge_labels = {(u, v): f"{d['weight']:.2f}, {d['time']}min" for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    # Highlight the path if it is provided
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='r', width=3)
        nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='r', node_size=700)

    plt.axis('off')  # Turn off the axis
    plt.show()

# Usage example
if __name__ == '__main__':
    from initialize_graph import create_ski_resort
    ski_resort = create_ski_resort()
    draw_graph(ski_resort)
