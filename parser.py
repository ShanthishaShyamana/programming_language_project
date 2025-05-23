from ASTnode import ASTnode

class Parser:
    def __init__(self, tokens):  
        self.tokens = tokens
        self.current_token = None
        self.pos = 0

    def read(self , expected=None):
        global stack
        stack = []

        if (self.pos < len(self.tokens)):
            self.current_token = self.tokens[self.pos]
            
        else:
            
            return None
        if expected in ["<IDENTIFIER>", "<STRING>", "<INTEGER>"]:
            if self.current_token.type != expected:
                raise SyntaxError(f"Expected token type '{expected}', but got '{self.current_token.type}' at position {self.pos}")

                # Check if expected token matches current token
        elif expected is not None and self.current_token.value != expected:
            raise SyntaxError(f"Expected '{expected}', but got '{self.current_token.value}' at position {self.pos}")
        
        
    
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
         match self.current_token.value:

            case 'let':
                self.read("let")
                self.parse_D()  
                self.read("in")
                self.parse_E()

                self.buildTree('let',2)

            case 'fn':
                self.read("fn")

                n = 1 # Vb can run until it gets Identifier or a Open Bracket
                self.parse_Vb()
                while(self.current_token.type == "IDENTIFIER" or self.current_token.value == "("):
                    self.parse_Vb()
                    n += 1
                   
                self.read(".")
                self.parse_E()
                self.buildTree('lambda',n+1)
                
            case  _:
                self.parse_Ew()

        #print("Parser: parse_E")


    def parse_Ew(self):
        self.parse_T()
        if(self.current_token.value == "where"):
            self.read("where")
            self.parse_Dr()
            self.buildTree('where',2)
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

        if self.current_token.value == '+':
            self.read('+')
            self.parse_At()

        elif self.current_token.value == '-':
            self.read('-')
            self.parse_At()
            self.buildTree("neg", 1)


        else:
            self.parse_At()
       
    
        while self.current_token.value == '+' or self.current_token.value == '-':

            if self.current_token.value=='-':
                self.read('-')
                self.parse_At()
                self.buildTree("-", 2)

            elif self.current_token.value=='+':
                self.read('+')
                self.parse_At()
                self.buildTree("+", 2)

            
        print("Parser: parse_A")

    def parse_At(self):

        
        self.parse_Af()
        # print('At->Af')
        while self.current_token.value == '*' or self.current_token.value == '/':
            
            if self.current_token.value == '/':
                self.read('/')
                self.parse_Af()
                self.buildTree("/", 2)

            elif self.current_token.value == '*':   
                self.read('*')
                self.parse_Af()
                self.buildTree("*", 2)
            

        print("Parser: parse_At")

    def parse_Af(self):

                # print('procAf')

        self.parse_Ap()
        # print('Af->Ap')
        while self.current_token.value == '**':
            self.read('**')
            self.parse_Ap()
            # print('Af->Ap ** Af')
            self.buildTree("**", 2)

        print("Parser: parse_Af")

    def parse_Ap(self):

        self.parse_R()
        # print('Ap->R')
        while self.current_token.value == '@':
            self.read('@')
            self.read("<IDENTIFIER>")
            self.parse_R()
            # print('Ap->R @ R')
            self.buildTree("@", 3)

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

    
    






    
    




