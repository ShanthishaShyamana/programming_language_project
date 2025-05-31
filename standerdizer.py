from ASTnode import ASTnode

def standardize(node):
    # Base case: if no children, return the node as-is
    if not node.child:
        return node

    # Transform based on type
    if node.type == "let":
        # let (= X E) P  => gamma (lambda X P) E
        eq_node = standardize(node.child[0])
        # print("Standardizing let node:", eq_node)
        # print(len(node.child), "children in let node")
        #print children
        # for i, child in enumerate(node.child):
            # print(f"Child {i}:", child)
        
        x = standardize(eq_node.child[0])
        # print("Standardizing let node x:", x)
        e = standardize(eq_node.child[1])
        # print("Standardizing let node e:", e)
        p = standardize(node.child[1])
        # print("Standardizing let node p:", p)

        lambda_node = ASTnode("lambda")
        lambda_node.child = [x, p]

        gamma_node = ASTnode("gamma")
        gamma_node.child = [lambda_node, e]
        return gamma_node

    elif node.type == "where":
        # where P (= X E) => gamma (lambda X P) E
        eq_node = standardize(node.child[1])
        # print("Standardizing where node:", eq_node)
        # print(len(node.child), "children in where node")
        # #print children
        # for i, child in enumerate(node.child):
        #     print(f"Child {i}:", child)
        # for i, child in enumerate(eq_node.child):
        #     print(f"Child {i} in eq_node:", child)
        x = standardize(eq_node.child[0])
        # print("Standardizing where node x:", x)
        e = standardize(eq_node.child[1])
        # print("Standardizing where node e:", e)
        p = standardize(node.child[0])
        # print("Standardizing where node p:", p)

        lambda_node = ASTnode("lambda")
        lambda_node.child = [x, p]

        gamma_node = ASTnode("gamma")
        gamma_node.child = [lambda_node, e]
        return gamma_node

    elif node.type == "within":
        # within (= X1 E1) (= X2 E2) => (= X2 (gamma (lambda X1 E2) E1))
        eq1 = standardize(node.child[0])
        eq2 = standardize(node.child[1])

        x1 = standardize(eq1.child[0])
        e1 = standardize(eq1.child[1])
        x2 = standardize(eq2.child[0])
        e2 = standardize(eq2.child[1])

        lambda_node = ASTnode("lambda")
        lambda_node.child = [x1, e2]

        gamma_node = ASTnode("gamma")
        gamma_node.child = [lambda_node, e1]

        eq_node = ASTnode("=")
        eq_node.child = [x2, gamma_node]
        return eq_node

    elif node.type == "rec":
        # rec (= X E) => (= X (gamma Ystar (lambda X E)))
        eq = standardize(node.child[0])
        x = standardize(eq.child[0])
        e = standardize(eq.child[1])

        lambda_node = ASTnode("lambda")
        lambda_node.child = [x, e]

        y_node = ASTnode("Y*>")

        gamma_node = ASTnode("gamma")
        gamma_node.child = [y_node, lambda_node]

        eq_node = ASTnode("=")
        eq_node.child = [x, gamma_node]
        return eq_node

    elif node.type == "fcn_form":
        # fcn_form P V+ E => (= P (lambda V (. E)))
        # print("Standardizing fcn_form node:", node)
        p = standardize(node.child[0])
        # print("Standardizing fcn_form node:", p)
        vs = [standardize(v) for v in node.child[1:-1]]
        # #loop tp print vs
        # for i, v in enumerate(vs):
        #     print(f"Variable {i}:", v)
        e = standardize(node.child[-1])
        # print("Standardizing fcn_form node e:", e)

        cur_lambda = ASTnode("lambda")
        cur_lambda.child = [vs[-1], e]
        for v in reversed(vs[:-1]):
            wrapper = ASTnode("lambda")
            wrapper.child = [v, cur_lambda]
            cur_lambda = wrapper

        eq_node = ASTnode("=")
        eq_node.child = [p, cur_lambda]
        return eq_node

    elif node.type == "lambda" and len(node.child) > 2:
        # lambda V++ E => lambda V (. E)
        vs = [standardize(v) for v in node.child[:-1]]
        e = standardize(node.child[-1])
        cur_lambda = ASTnode("lambda")
        cur_lambda.child = [vs[-1], e]
        for v in reversed(vs[:-1]):
            wrapper = ASTnode("lambda")
            wrapper.child = [v, cur_lambda]
            cur_lambda = wrapper
        return cur_lambda

    elif node.type == "and":
        print(f"Processing 'and' node with {len(node.child)} children")  # Debug
        xs = []
        es = []
        for i, eq in enumerate(node.child):
            print(f"Child {i} of 'and': type={eq.type}, children={len(eq.child)}")  # Debug
            standardized_eq = standardize(eq)  # Standardize 'rec' or '=' node
            print(f"After standardization, Child {i}: type={standardized_eq.type}, children={len(standardized_eq.child)}")  # Debug
            if standardized_eq.type != "=" or len(standardized_eq.child) < 2:
                raise SyntaxError(f"Expected '=' node with two children in 'and' construct, got type={standardized_eq.type}, children={len(standardized_eq.child)}")
            xs.append(standardized_eq.child[0])  # Identifier
            es.append(standardized_eq.child[1])  # Expression
            tau1 = ASTnode(",")
            tau1.child = xs
            tau2 = ASTnode("tau")
            tau2.child = es
            eq_node = ASTnode("=")
            eq_node.child = [tau1, tau2]
        return eq_node

    elif node.type == "@":
        # @ N E1 E2 => gamma (gamma N E1) E2
        n = standardize(node.child[0])
        e1 = standardize(node.child[1])
        e2 = standardize(node.child[2])

        gamma1 = ASTnode("gamma")
        gamma1.child = [n, e1]

        gamma2 = ASTnode("gamma")
        gamma2.child = [gamma1, e2]
        return gamma2

    # Recursively standardize children otherwise
    node.child = [standardize(c) for c in node.child]
    return node
