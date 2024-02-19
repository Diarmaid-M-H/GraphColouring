import networkx as nx
import random
import matplotlib.pyplot as plt

def main():
    def generate_connected_random_graph(num_nodes, num_edges, k):
        # Ensure the graph is connected using Watts-Strogatz model
        G = nx.connected_watts_strogatz_graph(num_nodes, k, p=0.1)
        # Adding additional edges to match the desired number of edges
        if G.number_of_edges() < num_edges:
            additional_edges = num_edges - G.number_of_edges()
            for _ in range(additional_edges):
                u = random.randint(0, num_nodes-1)
                v = random.randint(0, num_nodes-1)
                if not G.has_edge(u, v):
                    G.add_edge(u, v)
        return G

    def assign_random_colors(G, colors):
        color_mapping = {}
        for node in G.nodes():
            color_mapping[node] = random.choice(colors)
        nx.set_node_attributes(G, color_mapping, 'color')

        return G

    num_nodes = 50
    num_edges = 40
    k = 4  # Number of nearest neighbors for each node in the Watts-Strogatz model
    colors = ['red', 'green', 'blue', 'yellow', 'orange']  # Define your list of colors here

    random_graph = generate_connected_random_graph(num_nodes, num_edges, k)
    colored_graph = assign_random_colors(random_graph, colors)

    # Print node colors
    # for node, data in colored_graph.nodes(data=True):
    #     print(f"Node {node} has color: {data['color']}")

    # Draw the graph
    nx.draw(colored_graph, with_labels=True, node_color=[data['color'] for node, data in colored_graph.nodes(data=True)])
    plt.show()

if __name__ == "__main__":
    main()
