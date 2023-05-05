# The team will simulate a mesh network where nodes and links may fail (Figure 5). Nodes and links may fail intermittently, as an input to the simulation, each node and link will have a certain probability to fail. When such failure occurs, the network must adapt and re-route to avoid the faulty link/node.

from collections import defaultdict
import random

# Node names (represents vertices in the graph)
nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]

# Graph (keys = node, value = connected nodes)
graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C", "E", "F"],
    "E": ["D", "G"],
    "F": ["D", "G", "H"],
    "G": ["E", "F"],
    "H": ["F", "I"],
    "I": ["H", "J", "K"],
    "J": ["I", "K", "L"],
    "K": ["I", "J", "L", "M", "N"],
    "L": ["J", "K", "N"],
    "M": ["K", "N"],
    "N": ["K", "L", "M"]
}

def simulate_failures(graph, probability):
    """ Simulate link failures in the graph """

    # New graph with empty connections (will fill this later)
    updated_graph = defaultdict(list)

    # Set to store broken links as tuples (node1, node2)
    broken_links = set()

    # Go through the nodes and its neighbors in graph
    for node, neighbors in graph.items():
        connected_neighbors = []
        for neighbor in neighbors:
            # Generate random number and if it is greater than probability, keep the connection
            if random.random() > probability:
                connected_neighbors.append(neighbor)
            else:
                # If the link is broken, add it to the broken_links set
                # Use sorted() to ensure (node1, node2) and (node2, node1) are treated as the same link
                broken_links.add(tuple(sorted((node, neighbor))))

        # Ensure at least one connection
        if not connected_neighbors:
            connected_neighbors.append(random.choice(neighbors))

        # Update new graph with the connections
        updated_graph[node] = connected_neighbors
        # Update reverse connections
        for connected_neighbor in connected_neighbors:
            updated_graph[connected_neighbor].append(node)

    return updated_graph, broken_links



def dijkstras_unweighted(graph, start_node):
    unvisited = []
    for node in graph:
        unvisited.append(node)
    unvisited.remove(start_node)

    #Just initializing all the paths
    table = {}
    for node in graph:
        table[node] = [None, None, None, None, None, None, None, None, None, None]
    table[start_node] = []
    current_node = start_node

    #Running through dijkstras now
    while len(unvisited) > 0:
        #This makes a list of adjacent nodes that are also unvisited
        adjacent_nodes = [node for node in graph[current_node] if node in unvisited]

        #This adds the node into the table
        for node in adjacent_nodes:
            if None in table[node] or len(table[current_node])+1 < len(table[node]):
              table[node] = table[current_node].copy()
              table[node].append(node)
        
        #This makes current_node the minimum unvisited node
        current_node = unvisited[0]
        for node in unvisited:
            if len(table[current_node]) > len(table[node]):
              current_node = node

        #This removes the current_node from the unvisited list
        unvisited.remove(current_node)
    
    return table

def main():
    start_node = input("\nInput the start node: ")
    end_node = input("Input the end node: ")
    probability = float(input("Input the probability of a node/link breaking: "))

    updated_graph, broken_links = simulate_failures(graph, probability)
    distance_table = dijkstras_unweighted(updated_graph, start_node)

    distance = distance_table[end_node]
    if distance != 999999:
        print(f"\nShortest path distance: {distance}")
    else:
        print("\nNo path found.")

    print(f"Broken links: {broken_links}")

if __name__ == "__main__":
    main()

