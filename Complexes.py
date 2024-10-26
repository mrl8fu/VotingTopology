import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import pandas as pd
import csv

def createComplex(points: dict, vote: int, filename: str) -> None:

    # Define Color
    color = 'red'
    if vote==1:
        color = 'blue'

    # Step 2: Create an empty graph to represent the simplicial complex
    G = nx.Graph()

    # Step 3: Add vertices (points)
    for point, info in points.items():
        if info['value'] == vote:
            G.add_node(point)

    # Step 4: Add edges if two points "see" each other and have the same binary value
    for point, info in points.items():
        if info['value'] == vote:
            for neighbor in info['sees']:
                if points[neighbor]['value'] == vote:
                    G.add_edge(point, neighbor)

    # Step 5: Identify cliques of vertices that all see each other and share the same binary value
    all_simplices = []  # List to store all simplices

    for clique in nx.find_cliques(G):  # find_cliques gives maximal cliques
        # Check if all nodes in the clique have the same binary value
        values = {points[node]['value'] for node in clique}
        if len(values) == 1:  # All nodes have the same value
            all_simplices.append(clique)  # Save this clique as a simplex

    # Step 6: Visualize the simplicial complex
    pos = nx.spring_layout(G)  # Layout for graph visualization
    nx.draw(G, pos, with_labels=False, node_color='Black', node_size=10, font_size=16, font_color='black')

    # Draw higher-dimensional simplices (triangles, tetrahedrons) in red
    for simplex in all_simplices:
        if len(simplex) >= 3:  # Only consider cliques with 3 or more vertices
            for edge in combinations(simplex, 2):
                nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color=color, width=2)
            if len(simplex) == 3:
                # Draw triangle
                x, y = zip(*[pos[node] for node in simplex])
                plt.fill(x, y, color, alpha=0.3)
            elif len(simplex) == 4:
                # For tetrahedron, draw each triangular face
                for face in combinations(simplex, 3):
                    x, y = zip(*[pos[node] for node in face])
                    plt.fill(x, y, color, alpha=0.4)
            elif len(simplex) == 5:
                # 5 dimensions, draw each face:
                for face in combinations(simplex, 4):
                    x, y = zip(*[pos[node] for node in face])
                    plt.fill(x, y, color, alpha=0.5)
            elif len(simplex) == 6:
                #6 dimensions, draw each face:
                for face in combinations(simplex, 5):
                    x, y = zip(*[pos[node] for node in face])
                    plt.fill(x, y, color, alpha=0.6)
            elif len(simplex) == 7:
                #7 dimensions
                for face in combinations(simplex, 6):
                    x, y = zip(*[pos[node] for node in face])
                    plt.fill(x, y, color, alpha=0.7)

            #We stop at 7, as that is the most connections we have in our dataset

    plt.gca().set_facecolor('#f8f8f8')
    plt.title("Simplicial Complex with Higher-Dimensional Simplices")
    plt.savefig("{filename}{value}.png".format(filename=filename, value=vote), dpi=300, transparent=True)
    plt.show()


def formatCSV(filename):

    result_dict = {}

    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            point = row["County"]
            binary_value = int(row["Voted (0=R, 1=D)"])
            related_points = row["Neighbors"].split("; ")

            result_dict[point] = {
                "value": binary_value,
                "sees": related_points
            }

    return result_dict


def main():
    states_dict_2020 = formatCSV("Voting Data Virginia - VA2020.csv")
    createComplex(states_dict_2020, 0, "VA2020_")
    createComplex(states_dict_2020, 1, "VA2020_")

    states_dict_2016 = formatCSV("Voting Data Virginia - VA2016.csv")
    createComplex(states_dict_2016, 0, "VA2016_")
    createComplex(states_dict_2016, 1, "VA2016_")

    states_dict_2012 = formatCSV("Voting Data Virginia - VA2012.csv")
    createComplex(states_dict_2012, 0, "VA2012_")
    createComplex(states_dict_2012, 1, "VA2012_")

if __name__ == "__main__":
    main()




