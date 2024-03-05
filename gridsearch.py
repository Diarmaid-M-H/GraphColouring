import networkx as nx
import random
import matplotlib.pyplot as plt

def generate_connected_random_graph(num_nodes, colors):
    # Ensure the graph is connected using Watts-Strogatz model
    k = 4  # Number of nearest neighbors for each node in the Watts-Strogatz model
    G = nx.connected_watts_strogatz_graph(num_nodes, k, p=0.1)

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

def resolve_conflicts(G, g_used_colors, reserve_colors, colour_introduction_chance, colour_change_chance):
    copy = G.copy()
    for node in G.nodes():
        if G.nodes[node]['flag']:
            neighbor_colors = [copy.nodes[neighbor]['color'] for neighbor in copy.neighbors(node)]
            available_colors = [color for color in g_used_colors if color not in neighbor_colors]
            if not available_colors and random.random() < colour_introduction_chance:
                new_color = reserve_colors.pop()
                g_used_colors.append(new_color)
                G.nodes[node]['color'] = new_color
            elif random.random() < colour_change_chance:
                if len(available_colors) > 0:
                    G.nodes[node]['color'] = random.choice(available_colors)
                else:
                    G.nodes[node]['color'] = random.choice(neighbor_colors)

            G.nodes[node]['flag'] = False
            copy.nodes[node]['flag'] = False

def draw_graph(G, pos, iteration):
    plt.title(f"Iteration {iteration}: Graph")
    nx.draw(G, pos, with_labels=True, node_color=[G.nodes[node]['color'] for node in G.nodes()])
    plt.show()

def main():
    num_nodes = 200
    num_graphs = 1

    g_used_colors = ['#fc5185', '#36486b']
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
    ]

    # Pre-generate graphs
    graphs = [generate_connected_random_graph(num_nodes, g_used_colors) for _ in range(num_graphs)]

    # Define parameters to search
    param_grid = {
        'colour_introduction_chance': [0.001, 0.005, 0.01],
        'colour_change_chance': [0.1, 0.3, 0.5]
    }

    best_params = None
    best_used_colors_length = float('inf') # starts with high number

    for intro_chance in param_grid['colour_introduction_chance']:
        for change_chance in param_grid['colour_change_chance']:
            used_colors_lengths = []
            for graph in graphs:
                conflicts = detect_conflicts(graph)
                iteration = 1
                pos = nx.spring_layout(graph)

                while conflicts > 0:
                    resolve_conflicts(graph, g_used_colors, reserve_colors, intro_chance, change_chance)
                    conflicts = detect_conflicts(graph)
                    iteration += 1

                used_colors_lengths.append(len(g_used_colors))

            avg_used_colors_length = sum(used_colors_lengths) / num_graphs
            if avg_used_colors_length < best_used_colors_length:
                best_used_colors_length = avg_used_colors_length
                best_params = (intro_chance, change_chance)

    print('Best intro_chance:', best_params[0])
    print('Best change_chance:', best_params[1])
    print('Best used colors length:', best_used_colors_length)

if __name__ == "__main__":
    main()
