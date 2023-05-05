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
"N": ["K", "L", "M"]}

start_node = input("\nInput the start node.")
end_node = input("Input the end node")
probability = float(input("Input the probability of a node/link breaking."))

def dijkstras_unweighted(graph, start_node):
    unvisited = []
    for node in graph:
        unvisited.append(node)
    unvisited.remove(start_node)

    #Just initializing all the distances
    table = {}
    for node in graph:
        table[node] = 999999
    table[start_node] = 0
    current_node = start_node

    #Running through dijkstras now
    while len(unvisited) > 0:

        #This makes a list of adjacent nodes that are also unvisited
        adjacent_nodes = [node for node in graph[current_node] if node in unvisited]

        #This adds the nodes' distances into the table
        for node in adjacent_nodes:
            table[node] = min(table[current_node] + 1, table[node])
        
        #This makes current_node the minimum unvisited node
        current_node = unvisited[0]
        for node in unvisited:
            if table[current_node] > table[node]:
              current_node = node

        #This removes the current_node from the unvisited list
        unvisited.remove(current_node)
    
    return table
            
print(dijkstras_unweighted(graph, "D"))
