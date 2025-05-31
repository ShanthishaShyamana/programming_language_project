# This file contains the structures used in the project.
class Delta:
    def __init__(self, number):
        self.number = number
        self.body = []  # Store control structure content
        self.type = "Delta"
        
    def __str__(self):
        return f"Delta({self.number})"

class Tau:
    def __init__(self, number):
        self.number = number
        self.type = "Tau"
        
    def __str__(self):
        return f"Tau({self.number})"

class Lambda:
    def __init__(self, number):
        self.number = number
        self.bounded_variable = None
        self.environment = None
        self.body = []  # Store control structure content
        self.type = "Lambda"
        
    def __str__(self):
        return f"Lambda({self.number}, {self.bounded_variable})"

class Eta:
    def __init__(self, number):
        self.number = number
        self.bounded_variable = None
        self.environment = None
        self.type = "Eta"
        
    def __str__(self):
        return f"Eta({self.number}, {self.bounded_variable})"