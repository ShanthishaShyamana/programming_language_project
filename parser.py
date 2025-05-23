from ASTnode import ASTnode

class Parser:
    def __init__(self, tokens):  
        self.tokens = tokens
        self.current_token = None
        self.pos = 0

    def read(self):
        global stack
        stack = []

        if (self.pos < len(self.tokens)):
            self.current_token = self.tokens[self.pos]
            
            
        else:
            
            return None
        
    
        self.pos += 1
        if self.current_token.type in ["STRING", "IDENTIFIER", "INTEGER", "OPERATOR"]:
            terminalNode = ASTnode(str(self.current_token.type))
            terminalNode.value = self.current_token.value
            stack.append(terminalNode)

            # self.read_stack()
            
            # print(terminalNode)
            return terminalNode
 
        if self.current_token.value in ['true', 'false', 'nil', 'dummy']:
            terminalNode = ASTnode(str(self.current_token.type))
            terminalNode.value = self.current_token.value
            stack.append(terminalNode)
            # self.read_stack()
            # print(terminalNode)
            return terminalNode
        else:
            return self.current_token
        
       

    def read_stack(self):
        
        if len(stack) > 0:
            node = stack.pop()
            print(node)


    def buildTree(self , token, numberOfChildren):

        node = ASTnode(token)

        while numberOfChildren > 0:
            # #print("error in while loop")
            child = stack[-1]
            stack.pop()
            # Assuming pop() is a function that returns an ASTNode
            # if node.child is not None:
            #     child.sibling = node.child
            #     node.child.previous = child
                # node.previous = child
            node.child.append(child)

            # node.sourceLineNumber = child.sourceLineNumber
            numberOfChildren -= 1
        # node.print_tree()

        stack.append(node)  # Assuming push() is a function that pushes a node onto a stack
        # #print("stack content after")
        # for node in stack:
        #     pass
            # #print(node.type)


    def parse_E(self):
        print("Parser: parse_E")

    def parse_Ew(self):
        print("Parser: parse_Ew")

    def parse_D(self):
        print("Parser: parse_D")

    def parse_T(self):
        print("Parser: parse_T")

    def parse_Ta(self):
        print("Parser: parse_Ta")

    def parse_Tc(self):
        print("Parser: parse_Tc")

    def parse_B(self):
        print("Parser: parse_B")

    def parse_Bt(self):
        print("Parser: parse_Bt")

    def parse_Bs(self):
        print("Parser: parse_Bs")

    def parse_Bp(self):
        print("Parser: parse_Bp")

    def parse_A(self):
        print("Parser: parse_A")

    def parse_At(self):
        print("Parser: parse_At")

    def parse_Af(self):
        print("Parser: parse_Af")

    def parse_Ap(self):
        print("Parser: parse_Ap")

    def parse_R(self):
        print("Parser: parse_R")

    def parse_Rn(self):
        print("Parser: parse_Rn")

    def parse_D(self):
        print("Parser: parse_D")

    def parse_Da(self):
        print("Parser: parse_Da")
    
    def parse_Dr(self):
        print("Parser: parse_Dr")

    def parse_Db(self):
        print("Parser: parse_Db")

    def parse_Vb(self):
        print("Parser: parse_Vb")

    def parse_Vl(self):
        print("Parser: parse_Vl")

    
    






    
    




