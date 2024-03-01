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
    # At start of iteration create copy graph to ensure synchronicity
    copy = G.copy()
    colour_introduction_chance = 0.001
    colour_change_chance = 0.5
    for node in G.nodes():
        if G.nodes[node]['flag']:
            neighbor_colors = [copy.nodes[neighbor]['color'] for neighbor in copy.neighbors(node)]
            available_colors = [color for color in g_used_colors if color not in neighbor_colors]
            if not available_colors and random.random() < colour_introduction_chance:  #COLOUR INTRODUCTION CHANCE # if empty
                new_color = reserve_colors.pop()
                g_used_colors.append(new_color)
                G.nodes[node]['color'] = new_color  # only G, not copy is written to
            elif random.random() < colour_change_chance:  # COLOUR CHANGE CHANCE # this was changed to be random
                if len(available_colors) > 0:
                    G.nodes[node]['color'] = random.choice(available_colors)
                else:
                    G.nodes[node]['color'] = random.choice(neighbor_colors)

            # Because the alg is synchronous and detect conflicts will be called not sure if this is necessary
            G.nodes[node]['flag'] = False
            copy.nodes[node]['flag'] = False

def draw_graph(G, pos, iteration):
    plt.title(f"Iteration {iteration}: Graph")
    nx.draw(G, pos, with_labels=True, node_color=[G.nodes[node]['color'] for node in G.nodes()])
    plt.show()

def main():
    num_nodes = 50
    num_edges = 20
    num_graphs = 20

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
    estimates = []
    used_colors_lengths = []
    iterations = []

    for _ in range(num_graphs):
        random_graph = generate_connected_random_graph(num_nodes, num_edges, g_used_colors)
        conflicts = detect_conflicts(random_graph)
        iteration = 1

        # Generate node positions with spring layout once
        pos = nx.spring_layout(random_graph)

        # Figure to compare against:
        estimate = max(nx.greedy_color(random_graph).values()) + 1
        #print('Minimum Colors: ' + str(estimate))

        while conflicts > 0:
            #draw_graph(random_graph, pos, iteration)  # edit here to start drawing graphs ******
            resolve_conflicts(random_graph, g_used_colors, reserve_colors)
            conflicts = detect_conflicts(random_graph)
            iteration += 1

        draw_graph(random_graph, pos, iteration)
        used_colors_lengths.append(len(g_used_colors))
        estimates.append(estimate)
        iterations.append(iteration)

    #print('Estimates:   ', estimates)
    #print('Used Colors: ', used_colors_lengths)
    #print('Iterations:  ', iterations)

    # Calculate averages
    avg_estimate = sum(estimates) / num_graphs
    avg_used_colors_length = sum(used_colors_lengths) / num_graphs
    avg_iterations = sum(iterations) / num_graphs
    print('Average Minimum Colors:     ', avg_estimate)
    print('Average Number Used Colors: ', avg_used_colors_length)
    print('Average Iterations:         ', avg_iterations)


if __name__ == "__main__":
    main()
