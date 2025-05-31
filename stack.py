class Stack:
    def __init__(self, type):
        self.stack = []
        self.type = type
        
    # The following method is implemented for debugging purposes.
    def __repr__(self):
        return str(self.stack)
        
    # The following three methods are implemented to make the class iterable and indexable.
    def __getitem__(self, index):
        return self.stack[index]
    
    def __setitem__(self, index, value):
        self.stack[index] = value
        
    def __reversed__(self):
        return reversed(self.stack)

    # The following function lets you push an item onto the stack.
    def push(self, item):
        self.stack.append(item)

    # The following function lets you pop an item from the stack.
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            if self.type == "CSE":
                print("Stack in CSE machine has become empty unexpectedly.")
            else:
                print("Stack used for AST generation has become empty unexpectedly.")
            exit(1)

    # The following function lets you check whether the stack is empty.
    def is_empty(self):
        return len(self.stack) == 0