class ASTnode:
        
    def __init__(self, type):
        self.type = type
        self.value = None
        self.sourceLineNumber = -1
        self.child = []
        # self.sibling = None
        self.previous = None
        self.indentation = 0
    
    def __str__(self):
        return f"ASTnode(type={self.type}, value={self.value}, sourceLineNumber={self.sourceLineNumber})"