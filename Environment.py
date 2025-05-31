class Environment():
    def __init__(self, number, parent):
        self.number = number  # Store environment index
        self.name = "e_" + str(number)
        self.variables = {}
        self.children = []
        self.parent = parent
    
    def add_child(self, child):
        self.children.append(child)
        # Remove copying of parent variables
    
    def add_variable(self, key, value):
        self.variables[key] = value