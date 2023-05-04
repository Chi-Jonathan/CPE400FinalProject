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