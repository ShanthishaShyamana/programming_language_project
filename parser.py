from ASTnode import ASTnode

class Parser:
    def __init__(self, tokens):  
        self.tokens = tokens
        self.current_token = self.tokens[0]
        self.pos = 0
        global stack
        stack = []  # Initialize the stack to hold AST nodes

    def read(self , expected=None):
        # print ("read ", expected)


        if expected in ["ID", "STR", "INT"]:
            if self.current_token.type != expected:
                raise SyntaxError(f"Expected token type '{expected}', but got '{self.current_token.type}' at position {self.pos}")

                # Check if expected token matches current token
        elif expected is not None and self.current_token.value != expected:
            raise SyntaxError(f"Expected '{expected}', but got '{self.current_token.value}' at position {self.pos}")
        
        
    
    
        if self.current_token.type in ["STR", "ID", "INT"]:
            terminalNode = ASTnode(str(self.current_token.type))
            terminalNode.value = self.current_token.value
            stack.append(terminalNode)


            # self.read_stack()
            
            # print(terminalNode)
            # return terminalNode
 
        if self.current_token.value in ['true', 'false', 'nil', 'dummy']:
            terminalNode = ASTnode(str(self.current_token.type))
            terminalNode.value = self.current_token.value
            stack.append(terminalNode)
            # self.read_stack()
            # print(terminalNode)
        #     return terminalNode
        # else:
        #     return self.current_token
        self.pos += 1
        if (self.pos < len(self.tokens)):
            self.current_token = self.tokens[self.pos]
            
        else:
            
            return None
        
       

    # def read_stack(self):
        
    #     if len(stack) > 0:
    #         node = stack.pop()
    #         print(node)


    def buildTree(self, token, numberOfChildren):
        node = ASTnode(token)
        # Create a list to store children in reverse order
        children = []
        
        # Pop children from stack and store them
        while numberOfChildren > 0:
            child = stack[-1]
            stack.pop()
            children.append(child)  # Collect children in temporary list
            numberOfChildren -= 1
            
        # Reverse children so they're in the correct order and set as node's children
        node.child = children[::-1]
        
        # Push the new node onto the stack
        stack.append(node)


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
                while(self.current_token.type == "ID" or self.current_token.value == "("):
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
        # print("Parser: parse_Ew")


    # def parse_D(self):
    #     print("Parser: parse_D")

    def parse_T(self):
        
        self.parse_Ta()
        n = 1
        while(self.current_token.value == ","):
            self.read(",")
            self.parse_Ta()
            n += 1
        if n > 1:
            self.buildTree('tau',n)

        # print("Parser: parse_T")

    def parse_Ta(self):
        self.parse_Tc()

        while(self.current_token.value == "aug"):
            self.read("aug")
            self.parse_Tc()
            self.buildTree('aug',2)

        # print("Parser: parse_Ta")

    def parse_Tc(self):
        self.parse_B()
        if(self.current_token.value == "->"):
            self.read("->")
            self.parse_Tc()
            self.read("|")
            self.parse_Tc()
            self.buildTree('->',3)

        # print("Parser: parse_Tc")

    def parse_B(self):
        self.parse_Bt()

        while(self.current_token.value == "or"):
            self.read("or")
            self.parse_Bt()
            self.buildTree('or',2)

        # print("Parser: parse_B")

    def parse_Bt(self):
        self.parse_Bs()

        while(self.current_token.value == "&"):
            self.read("&")
            self.parse_Bs()
            self.buildTree('&',2)

        # print("Parser: parse_Bt")

    def parse_Bs(self):

        if self.current_token.value == "not":
            self.read("not")
            self.parse_Bp()
            self.buildTree('not',1)
        
        else:
            self.parse_Bp()

        # print("Parser: parse_Bs")



    def parse_Bp(self):
        self.parse_A()

        if self.current_token.value == "gr" or self.current_token.value == ">":
            self.read(self.current_token.value)
            self.parse_A()
            self.buildTree('gr', 2)
        
        elif self.current_token.value == "ge" or self.current_token.value == ">=":
            self.read(self.current_token.value)
            self.parse_A()
            self.buildTree('ge', 2)

        elif self.current_token.value == "ls" or self.current_token.value == "<":
            self.read(self.current_token.value)
            self.parse_A()
            self.buildTree('ls', 2)
        
        elif self.current_token.value == "le" or self.current_token.value == "<=":
            self.read(self.current_token.value)
            self.parse_A()
            self.buildTree('le', 2)

        elif self.current_token.value == "eq" :
            self.read("eq")
            self.parse_A()
            self.buildTree('eq', 2)

        elif self.current_token.value == "ne":
            self.read("ne")
            self.parse_A()
            self.buildTree('ne', 2)



        # print("Parser: parse_Bp")

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

            
        # print("Parser: parse_A")

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
            

        # print("Parser: parse_At")

################################################################

    def parse_Af(self):

                # print('procAf')

        self.parse_Ap()
        # print('Af->Ap')
        while self.current_token.value == '**':
            self.read('**')
            self.parse_Ap()
            # print('Af->Ap ** Af')
            self.buildTree("**", 2)

        # print("Parser: parse_Af")

###############################################################

    def parse_Ap(self):

        self.parse_R()
        # print('Ap->R')
        while self.current_token.value == '@':
            self.read('@')
            self.read("ID")
            self.parse_R()
            # print('Ap->R @ R')
            self.buildTree("@", 3)

        # print("Parser: parse_Ap")

    def parse_R(self):

        self.parse_Rn()
        while self.current_token.value in ['true', 'false', 'nil', 'dummy','('] or self.current_token.type in ["ID", "STR", "INT"]:
            # print('Rn->' + str(self.current_token.value))
            if self.pos >= len(self.tokens):
                break
            self.parse_Rn()
            # print('Rn->' + str(self.current_token.value))
            # self.buildTree("id", 0)
            self.buildTree("gamma", 2)

        # print("Parser: parse_R")

    def parse_Rn(self):

        if self.current_token.value == '(':
            self.read('(')
            self.parse_E()
            self.read(')')
           

        elif self.current_token.type == "ID":
            self.read("ID")
            # print('Rn->id')
            

        elif self.current_token.type == "STR":
            self.read("STR")
            # print('Rn->string')
            

        elif self.current_token.type == "INT":
            self.read("INT")
            # print('Rn->int')
            

        elif self.current_token.value == 'true':
            self.read('true')
            # self.buildTree('true', 0)
            
        elif self.current_token.value == 'false':
            self.read('false')
            # self.buildTree('false', 0)
            
        elif self.current_token.value == 'nil':
            self.read('nil')
            # self.buildTree('nil', 0)
            
        elif self.current_token.value == 'dummy':
            self.read('dummy')
            # self.buildTree('dummy', 0)
            # print('Rn->bool')
        # print("Parser: parse_Rn")



#######################################################

    def parse_D(self):  
        self.parse_Da()
        while self.current_token.value == "within":
            self.read("within")
            self.parse_Da()
            self.buildTree('within', 2)

        # print("Parser: parse_D")

#####################################################

    def parse_Da(self):
        self.parse_Dr()
        m=1
        while self.current_token.value == "and":
            self.read("and")
            self.parse_Dr()
            m += 1
        if m>1:
            self.buildTree('and', m)
        
        # print("Parser: parse_Da")
    
    def parse_Dr(self):

        if self.current_token.value == "rec":
            self.read("rec")
            self.parse_Db()
            self.buildTree('rec', 1)

        else:
            self.parse_Db()

        # print("Parser: parse_Dr")

    def parse_Db(self):
        
        if self.current_token.value == "(":
            self.read("(")
            self.parse_D()
            self.read(")")

            ###################################################
        
        elif self.current_token.type == "ID":
           
            self.read("ID")
            p=1
            if self.current_token.value == "(" or self.current_token.type == "ID":
                vb_count = 0
                while self.current_token.value == "(" or self.current_token.type == "ID":
                    self.parse_Vb()
                    vb_count += 1
                if self.current_token.value == "=":
                    self.read("=")
                    self.parse_E()
                    self.buildTree('fcn_form', vb_count + 1+p)

            elif self.current_token.value == "=":
                # print(self.current_token.value)
                self.read("=")
                self.parse_E()
                self.buildTree('=', 2 )
            
            elif self.current_token.value == ",":
                self.read(",")
                self.read("ID")
                p+= 1
                while self.current_token.value == ",":
                    self.read(",")
                    self.read("ID")
                    p += 1
                self.buildTree(",", p )
                
        # else:
        #     self.parse_Vl()
        #     self.read("=")
        #     self.parse_E()
        #     self.buildTree('=', 2)


        # print("Parser: parse_Db")

    def parse_Vb(self):
        if self.current_token.type == "ID":
            self.read("ID")
           
        elif self.current_token.value == "(":
            self.read("(")
            if self.current_token.value == ")":
                self.read(")")
                # print('Vb->()')
                self.buildTree("()", 0)
            else:
                self.parse_Vl()
                self.read(")")
                # print('Vb->Vl)')

        # print("Parser: parse_Vb")


################################################################

    def parse_Vl(self):

        self.read("ID")
        v =1
        while self.current_token.value == ",":
            self.read(",")
            self.read("ID")
            v += 1

        self.buildTree(",", v)
        # print("Parser: parse_Vl")

# function to return stack
    def get_stack(self):
          return stack
    
    






    
    




