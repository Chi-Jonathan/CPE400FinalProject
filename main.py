# The team will simulate a mesh network where nodes and links may fail (Figure 5). Nodes and links may fail intermittently, as an input to the simulation, each node and link will have a certain probability to fail. When such failure occurs, the network must adapt and re-route to avoid the faulty link/node.

from ast import literal_eval
from collections import defaultdict
import random

#Gets a network from a file
def get_network(filename):
  f = open(filename, "r")
  network = []
  connection = ("", "")
  line = f.readline()[:-1]
  while line:
    connection = tuple(line.split(":"))
    network.append(connection)
    line = f.readline()[:-1]
  f.close()
  return network

#Builds the network into a graph/adjacency list
def build_network(network):
  graph = {}
  for connection in network:
    graph[connection[0]] = literal_eval(connection[1])
  return graph
  

def dfs(graph, start, visited=None):
    # If visited set is not provided, initialize an empty set
    if visited is None:
        visited = set()
        
    # Add the current start node to the visited set
    visited.add(start)
    # Iterate through neighbors of the start node
    for neighbor in graph[start]:
        # If the neighbor node has not been visited yet, perform DFS recursively
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    # visited set contains all nodes reachable from the start node
    return visited

def simulate_failures(graph, probability):
    # Initialize the updated graph as a defaultdict with lists as default values
    updated_graph = defaultdict(list)
    # Initialize a set to store broken links
    broken_links = set()

    # Iterate through nodes and their neighbors in the original graph
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            # If a random value is less than or equal to the input probability, add the link as broken
            if random.random() <= probability:
                broken_links.add(tuple(sorted((node, neighbor))))
    # Iterate through nodes and their neighbors in the original graph again
    for node, neighbors in graph.items():
        # Create a list of connected neighbors, filtering out the broken links
        connected_neighbors = [neighbor for neighbor in neighbors if tuple(sorted((node, neighbor))) not in broken_links]
        # Assign the connected neighbors to the corresponding node in the updated graph
        updated_graph[node] = connected_neighbors
    # Initialize a set to store fixed links
    fixed_links = set()
    # Iterate through the broken links
    for link in broken_links:
        node1, node2 = link
        # Use DFS to find the nodes reachable from node1 in the updated graph
        visited = dfs(updated_graph, node1)
        # If node2 is not reachable, fix the link by adding it back to the updated graph
        if node2 not in visited:
            updated_graph[node1].append(node2)
            updated_graph[node2].append(node1)
            fixed_links.add(link)
    # Remove the fixed links from the broken_links set
    broken_links -= fixed_links
    # Return the updated graph and the final set of broken links
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


######################



def main():

    network = input("\nInput which graph you want to use (options: graph1.txt, graph2.txt, graph3.txt): ")
    while network != "graph1.txt" and network!="graph2.txt" and network!="graph3.txt":
      network = input("Input which graph you want to use (options: graph1.txt, graph2.txt, graph3.txt): ")

    graph = build_network(get_network(network))
    nodes = []
    for node in graph:
      nodes.append(node)
      
    start_node = input("\nInput the start node: ").upper()
    while start_node not in nodes:
      print(f"Invalid node (Nodes go from A-{nodes[-1]})")
      start_node = input("Input the start node: ").upper()

    end_node = input("\nInput the end node: ").upper()
    while end_node not in nodes:
      print(f"Invalid node (Nodes go from A-{nodes[-1]})")
      end_node = input("Input the end node: ").upper()
      
    probability = input("\nInput the probability of a node/link breaking (0.0-1.0): ")
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