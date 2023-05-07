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

def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

def simulate_failures(graph, probability):
    updated_graph = defaultdict(list)
    broken_links = set()

    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if random.random() <= probability:
                broken_links.add(tuple(sorted((node, neighbor))))

    for node, neighbors in graph.items():
        connected_neighbors = [neighbor for neighbor in neighbors if tuple(sorted((node, neighbor))) not in broken_links]
        updated_graph[node] = connected_neighbors

    fixed_links = set()
    for link in broken_links:
        node1, node2 = link
        visited = dfs(updated_graph, node1)
        if node2 not in visited:
            updated_graph[node1].append(node2)
            updated_graph[node2].append(node1)
            fixed_links.add(link)

    broken_links -= fixed_links

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
    start_node = input("\nInput the start node: ").upper()
    while start_node not in nodes:
      print("Invalid node (Nodes go from A-N)")
      start_node = input("Input the start node: ").upper()

    end_node = input("Input the end node: ").upper()
    while end_node not in nodes:
      print("Invalid node (Nodes go from A-N)")
      end_node = input("Input the end node: ").upper()
      
    probability = input("Input the probability of a node/link breaking (0.0-1.0): ")
    while not probability.replace('.', '', 1).isdigit() or float(probability)>1 or float(probability)<0:
      print("Invalid input")
      probability = input("Input the probability of a node/link breaking (0.0-1.0): ")
      
    probability = float(probability)
    

    updated_graph, broken_links = simulate_failures(graph, probability)
    distance_table = dijkstras_unweighted(updated_graph, start_node)

    print(f"\nUpdated graph: {updated_graph}")

    distance = distance_table[end_node]
    if None not in distance:
        print(f"\nShortest path distance: {distance}")
    else:
        print("\nNo path found.")

    print(f"Broken links: {broken_links}")

if __name__ == "__main__":
  main()
