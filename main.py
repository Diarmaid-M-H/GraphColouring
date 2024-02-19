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

    def detect_conflicts(G):
        conflicts = 0
        for node in G.nodes():
            node_color = G.nodes[node]['color']
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]['color'] == node_color:
                    G.nodes[node]['flag'] = True
                    conflicts += 1
                    break  # No need to check further neighbors if already found a conflict
            else:
                G.nodes[node]['flag'] = False
        return conflicts

    def resolve_conflicts(G, colors):
        for node in G.nodes():
            if G.nodes[node]['flag']:
                node_color = G.nodes[node]['color']
                neighbor_colors = {G.nodes[neighbor]['color'] for neighbor in G.neighbors(node)}
                available_colors = [color for color in colors if color not in neighbor_colors]
                new_color = random.choice(available_colors)
                G.nodes[node]['color'] = new_color
                G.nodes[node]['flag'] = False  # Reset flag after resolving conflict

    num_nodes = 40
    num_edges = 20
    k = 4  # Number of nearest neighbors for each node in the Watts-Strogatz model
    colors = ['red', 'green', 'blue', 'yellow', 'orange']  # Define your list of colors here

    random_graph = generate_connected_random_graph(num_nodes, num_edges, k)
    colored_graph = assign_random_colors(random_graph, colors)

    # Compute layout only once
    pos = nx.spring_layout(colored_graph)

    iteration = 1
    while True:
        # Detect conflicts sets a "conflict" flag to true so that resolve conflicts can fix
        # Also returns the no. of conflicts
        conflicts = detect_conflicts(colored_graph)
        print(f"Iteration {iteration}: Number of conflicts: {conflicts}")

        # Plot the graph
        plt.title(f"Iteration {iteration}: Graph")
        nx.draw(colored_graph, pos=pos, with_labels=True, node_color=[data['color'] for node, data in colored_graph.nodes(data=True)])
        plt.show()

        if conflicts == 0:
            break  # No conflicts remaining, exit the loop

        # Resolve conflicts
        resolve_conflicts(colored_graph, colors)

        iteration += 1

    # Plot the final graph
    plt.title('Final Graph')
    nx.draw(colored_graph, pos=pos, with_labels=True, node_color=[data['color'] for node, data in colored_graph.nodes(data=True)])
    plt.show()

if __name__ == "__main__":
    main()
