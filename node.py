nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]

class node():
    def __init__(self, node):
        self.node = node
        self.distance_table = {}
        for letter in nodes:
            self.distance_table[letter] = 100
    
    def update_distance_table(self, distance_table):
        self.distance_table = distance_table