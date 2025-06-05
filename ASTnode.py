class ASTnode:
        
    def __init__(self, type):
        self.type = type
        self.value = None
        self.child = []

    
    def __str__(self):
        return f"ASTnode(type={self.type}, value={self.value})"