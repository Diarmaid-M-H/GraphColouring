import networkx as nx
import random
import matplotlib.pyplot as plt


def generate_connected_random_graph(num_nodes, num_edges, colors):
    # Ensure the graph is connected using Watts-Strogatz model
    k = 4  # Number of nearest neighbors for each node in the Watts-Strogatz model
    G = nx.connected_watts_strogatz_graph(num_nodes, k, p=0.1)

    # Adding additional edges to match the desired number of edges
    if G.number_of_edges() < num_edges:
        additional_edges = num_edges - G.number_of_edges()
        for _ in range(additional_edges):
            u = random.randint(0, num_nodes - 1)
            v = random.randint(0, num_nodes - 1)
            if not G.has_edge(u, v):
                G.add_edge(u, v)

    # Assign colors to nodes
    for node in G.nodes():
        G.nodes[node]['color'] = random.choice(colors)

    return G


def detect_conflicts(G):
    conflicts = 0
    for node in G.nodes():
        node_color = G.nodes[node]['color']
        for neighbor in G.neighbors(node):
            if G.nodes[neighbor]['color'] == node_color:
                G.nodes[node]['flag'] = True
                conflicts += 1
                break
        else:
            G.nodes[node]['flag'] = False
    return conflicts


def resolve_conflicts(G, g_used_colors, reserve_colors):
    for node in G.nodes():
        if G.nodes[node]['flag']:
            node_color = G.nodes[node]['color']
            neighbor_colors = {G.nodes[neighbor]['color'] for neighbor in G.neighbors(node)}
            available_colors = [color for color in g_used_colors if color not in neighbor_colors]
            if not available_colors:  # checks if none available
                new_color = reserve_colors.pop()
                g_used_colors.append(new_color)
                G.nodes[node]['color'] = new_color
            else:
                G.nodes[node]['color'] = available_colors[0]
            G.nodes[node]['flag'] = False


def draw_graph(G, pos, iteration):
    plt.title(f"Iteration {iteration}: Graph")
    nx.draw(G, pos, with_labels=True, node_color=[G.nodes[node]['color'] for node in G.nodes()])
    plt.show()


def main():
    num_nodes = 50
    num_edges = 40
    g_used_colors = ['#fc5185', '#36486b']  # Initial list of colors
    reserve_colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#1a1a1a', '#ff0000', '#800000', '#ffff00', '#808000',
        '#00ff00', '#008000', '#00ffff', '#008080', '#0000ff',
        '#000080', '#ff00ff', '#800080', '#ff5733', '#ffc300',
        '#c70039', '#900c3f', '#581845', '#ff6f61', '#ffa07a',
        '#ffcc5c', '#ffeead', '#dcedc1', '#5e2ca5', '#a7e9af',
        '#fff200', '#00b2ff', '#4a4e4d', '#8a89a6', '#997c6c',
        '#3d4b52', '#5bc0eb', '#fde74c', '#9bc53d', '#c3423f',
        '#f7f4a3', '#36486b', '#3fc1c9'
    ]  # List of reserve colors

    random_graph = generate_connected_random_graph(num_nodes, num_edges, g_used_colors)
    conflicts = detect_conflicts(random_graph)
    iteration = 1

    # Generate node positions with spring layout once
    pos = nx.spring_layout(random_graph)

    while conflicts > 0:
        print(f"Iteration {iteration}: Number of conflicts: {conflicts}")
        draw_graph(random_graph, pos, iteration)
        resolve_conflicts(random_graph, g_used_colors, reserve_colors)
        conflicts = detect_conflicts(random_graph)
        iteration += 1

    print("Conflict resolution complete.")
    draw_graph(random_graph, pos, "Final")


if __name__ == "__main__":
    main()
