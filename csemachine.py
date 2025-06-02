from standerdizer import standardize
from ASTnode import ASTnode
from Environment import Environment
from stack import Stack
from structure import Delta, Tau, Lambda, Eta

control_structures = []
count = 0
control = []
stack = Stack("CSE")
environments = [Environment(0, None)]
current_environment = 0
builtInFunctions = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction", "ItoS","neg"]
print_present = False

def generate_control_structure(root, i, current_env=0):
    global count
    
    while len(control_structures) <= i:
        control_structures.append([])

    # print(f"Generating control structure for node {root.type}, index {i}, env e_{current_env}")  # Debug
    
    if root.type == "lambda":
        count += 1
        temp = Lambda(count)
        left_child = root.child[0]
        if left_child.type == ",":
            temp.bounded_variable = [child.value for child in left_child.child]
            # print(f"Lambda {count} bounded variables: {temp.bounded_variable}")
        else:
            temp.bounded_variable = left_child.value
        temp.environment = current_env  # Set environment at definition
        temp.body = []
        control_structures[i].append(temp)
        # Process lambda body with new index
        body_index = count
        generate_control_structure(root.child[1], body_index, current_env)
        temp.body = control_structures[body_index]
        # print(f"Lambda {count} body: {temp.body}, env e_{current_env}")  # Debug

    elif root.type == "->":
        count += 1
        then_delta = Delta(count)
        control_structures[i].append(then_delta)
        generate_control_structure(root.child[1], count, current_env)
        then_delta.body = control_structures[count]
        
        count += 1
        else_delta = Delta(count)
        control_structures[i].append(else_delta)
        generate_control_structure(root.child[2], count, current_env)
        else_delta.body = control_structures[count]
        
        control_structures[i].append("beta")
        generate_control_structure(root.child[0], i, current_env)

    elif root.type == "tau":
        temp = Tau(len(root.child))
        control_structures[i].append(temp)
        for child in root.child:
            generate_control_structure(child, i, current_env)

    elif root.type in ["gamma", ",", "=", "Y*"]:
        control_structures[i].append(root.type)
        for child in root.child:
            generate_control_structure(child, i, current_env)

    elif root.type in ["IDENTIFIER", "INTEGER", "STRING", "KEYWORD"]:
        control_structures[i].append(f"<{root.type}:{root.value}>")
    
    elif root.type:  # Handle operators like +, -, etc.
        control_structures[i].append(root.type)
        for child in root.child:
            generate_control_structure(child, i, current_env)

def lookup(name):
    if not name.startswith("<") or not name.endswith(">"):
        return name
    name = name[1:-1]
    info = name.split(":", 1)
    
    if len(info) == 1:
        value = info[0]
    else:
        data_type, value = info
        if data_type == "INTEGER":
            return int(value)
        elif data_type == "STRING":
            return value.strip("'")
        elif data_type == "IDENTIFIER":
            if value in builtInFunctions:
                return value
            
            elif value in ["neg", "not"]:
                return value
            try:
                env = environments[current_environment]
                while env:
                    if value in env.variables:
                        # print(f"Found {value} = {env.variables[value]} in environment e_{env.number}")  # Debug
                        return env.variables[value]
                    # print(f"Variable {value} not found in environment e_{env.number}, checking parent...")  # Debug
                    env = env.parent
                
                print(f"Undeclared Identifier: {value}")
                exit(1)
            except KeyError:
                print(f"Undeclared Identifier: {value}")
                exit(1)
        elif data_type == "KEYWORD":
            if value == "nil":
                return ()
            elif value == "true":
                return True
            elif value == "false":
                return False
            elif value == "Y*":
                return "Y*"
    return value

def built_in(function, argument):
    global print_present
    if function == "Order":
        stack.push(len(argument))
    elif function in ["Print", "print"]:
        print_present = True
        if isinstance(argument, str):
            argument = argument.replace("\\n", "\n").replace("\\t", "\t")
        stack.push(argument)
    elif function == "Conc":
        if stack.is_empty():
            print("Error: Stack empty for Conc")
            exit(1)
        stack_symbol = stack.pop()
        control.pop()
        stack.push(argument + stack_symbol)
    elif function == "Stern":
        stack.push(argument[1:])
    elif function == "Stem":
        stack.push(argument[0])
    elif function == "Isinteger":
        stack.push(isinstance(argument, int))
    elif function == "Istruthvalue":
        stack.push(isinstance(argument, bool))
    elif function == "Isstring":
        stack.push(isinstance(argument, str))
    elif function == "Istuple":
        stack.push(isinstance(argument, tuple))
    elif function == "Isfunction":
        stack.push(function in builtInFunctions)
    elif function == 'neg':
        # print(f"Applying negation to in built {argument}")  # Debug
        if isinstance(argument, int):
            stack.push(-argument)
        else:
            print("Error: neg function can only accept integers.")
            exit()
    elif function == "ItoS":
        if isinstance(argument, int):
            stack.push(str(argument))
        else:
            print("Error: ItoS function can only accept integers.")
            exit()


def apply_rules():
    op = ["+", "-", "*", "/", "**", "gr", "ge", "ls", "le", "eq", "ne", "or", "&", "aug"]
    uop = ["neg", "not"]
    global control, current_environment, count

    def extract_current_env_from_control():
        """Extract the latest environment number from control stack"""
        for item in reversed(control):
            if isinstance(item, str) and item.startswith("e_"):
                return int(item[2:])
        return current_environment

    # Set the initial current environment
    current_environment = extract_current_env_from_control() if control else 0

    while control:
        if stack.is_empty() and control:
            print(f"Warning: Stack empty, control: {control}")
        symbol = control.pop()
        # print(f"Applying rule for symbol: {symbol}, Stack: {stack.stack}, Control: {control}")  # Debug

        # Rule 1: Identifiers, literals
        if isinstance(symbol, str) and symbol.startswith("<") and symbol.endswith(">"):
            stack.push(lookup(symbol))

        # Rule 2: Lambda
        elif isinstance(symbol, Lambda):
            stack.push(symbol)  # Push lambda as-is, environment already set
            #update environment in lambda
            symbol.environment = current_environment
            # print(f"Lambda {symbol.number} pushed with environment e_{symbol.environment}")  # Debug

        # Rule 4: Gamma (function application)
        elif symbol == "gamma":
            if len(stack.stack) < 2:
                print(f"Error: Stack has {len(stack.stack)} items, need 2 for gamma")
                exit(1)
            stack_symbol_1 = stack.pop()
            stack_symbol_2 = stack.pop()
            # print(f"Gamma: Applying {stack_symbol_1} to {stack_symbol_2}")  # Debug

            if isinstance(stack_symbol_1, Lambda):
                if isinstance(stack_symbol_2, str) and stack_symbol_2.startswith("e_"):
                    print(f"Error: Invalid argument {stack_symbol_2} for lambda application")
                    exit(1)
                current_environment = len(environments)
                lambda_number = stack_symbol_1.number
                bounded_variable = stack_symbol_1.bounded_variable
                parent_environment_number = stack_symbol_1.environment

                if parent_environment_number is None:
                    print(f"Error: Lambda {lambda_number} has no environment")
                    exit(1)
                parent = environments[parent_environment_number]
                child = Environment(current_environment, parent)
                parent.add_child(child)
                environments.append(child)
                if isinstance(bounded_variable, str):
                    # Single variable - normal application
                    child.add_variable(bounded_variable, stack_symbol_2)
                    stack.push(child.name)
                    control.append(child.name)
                    control.extend(stack_symbol_1.body)

                # Handle multiple variables (e.g., from 'and' or multi-arg functions)
                elif isinstance(bounded_variable, list):
                    # print('list of bounded variables:', bounded_variable)  # Debug
                    
                    if len(bounded_variable) == 1:
                        # Single variable in a list - treat as normal single variable
                        child.add_variable(bounded_variable[0], stack_symbol_2)
                        stack.push(child.name)
                        control.append(child.name)
                        control.extend(stack_symbol_1.body)
                        
                    elif isinstance(stack_symbol_2, tuple) and len(stack_symbol_2) == len(bounded_variable):
                        # Multiple variables with matching tuple of values
                        # print(f"Applying lambda with multiple variables: {bounded_variable}")  # Debug
                        for var, val in zip(bounded_variable, stack_symbol_2):
                            child.add_variable(var, val)
                        stack.push(child.name)
                        control.append(child.name)
                        control.extend(stack_symbol_1.body)
                        
                    elif len(bounded_variable) > 1 and not isinstance(stack_symbol_2, tuple):
                        # Partial application for currying - bind first variable, return new lambda
                        # print(f"Partial application: binding {bounded_variable[0]} to {stack_symbol_2}")  # Debug
                        
                        # Bind the first variable
                        child.add_variable(bounded_variable[0], stack_symbol_2)
                        
                        # Create new lambda for remaining variables
                        new_lambda = Lambda(count + 1)
                        count += 1
                        new_lambda.bounded_variable = bounded_variable[1:]  # Remaining variables
                        new_lambda.environment = current_environment  # Current environment (with first var bound)
                        new_lambda.body = stack_symbol_1.body  # Same body
                        
                        # Push the new lambda (no environment marker needed for partial application)
                        # current_environment = child.number
                        # stack.push(child.name)
                        # control.append(child.name)
                        
                        stack.push(new_lambda)
                        
                    else:
                        print(f"Error: Expected tuple of length {len(bounded_variable)} for variables {bounded_variable}, got {stack_symbol_2}")
                        exit(1)
                else:
                    child.add_variable(bounded_variable, stack_symbol_2)
                    stack.push(child.name)
                    control.append(child.name)
                    control.extend(stack_symbol_1.body)

            elif isinstance(stack_symbol_1, tuple):
                if isinstance(stack_symbol_2, int) and 1 <= stack_symbol_2 <= len(stack_symbol_1):
                    stack.push(stack_symbol_1[stack_symbol_2 - 1])
                else:
                    print(f"Error: Invalid tuple index {stack_symbol_2}")
                    exit(1)

            elif stack_symbol_1 == "Y*":
                temp = Eta(stack_symbol_2.number)
                temp.bounded_variable = stack_symbol_2.bounded_variable
                temp.environment = stack_symbol_2.environment
                temp.body = stack_symbol_2.body
                stack.push(temp)

            elif isinstance(stack_symbol_1, Eta):
                temp = Lambda(stack_symbol_1.number)
                temp.bounded_variable = stack_symbol_1.bounded_variable
                temp.environment = stack_symbol_1.environment
                temp.body = stack_symbol_1.body
                control.append("gamma")
                control.append("gamma")
                stack.push(stack_symbol_2)
                stack.push(stack_symbol_1)
                stack.push(temp)

            elif stack_symbol_1 in builtInFunctions:
                built_in(stack_symbol_1, stack_symbol_2)
                # print(f"Built-in function {stack_symbol_1} applied to {stack_symbol_2}")  # Debug

        # Rule 5: Environment
        elif isinstance(symbol, str) and symbol.startswith("e_"):
            if len(stack.stack) < 1:
                print(f"Error: Stack has {len(stack.stack)} items, need at least 1 for environment")
                exit(1)
            if len(stack.stack) == 1:
                print(f"Warning: Only environment {symbol} on stack, skipping result pop")
                current_environment = int(symbol[2:])
            else:
                stack_symbol = stack.pop()
                stack.pop()  # Remove environment
                current_environment = int(symbol[2:])
                stack.push(stack_symbol)

        # Rule 6: Binary operators
        elif symbol in op:
            if len(stack.stack) < 2:
                print(f"Error: Stack has {len(stack.stack)} items, need 2 for operator {symbol}")
                exit(1)
            rand_1 = stack.pop()
            rand_2 = stack.pop()
            # print(f"Applying {symbol} to {rand_1} and {rand_2}")  # Debug
            try:
                if symbol == "+":
                    stack.push(rand_1 + rand_2)
                elif symbol == "-":
                    stack.push(rand_1 - rand_2)
                elif symbol == "*":
                    stack.push(rand_1 * rand_2)
                elif symbol == "/":
                    stack.push(rand_1 // rand_2)
                elif symbol == "**":
                    stack.push(rand_1 ** rand_2)
                elif symbol == "gr":
                    stack.push(rand_1 > rand_2)
                elif symbol == "ge":
                    stack.push(rand_1 >= rand_2)
                elif symbol == "ls":
                    stack.push(rand_1 < rand_2)
                elif symbol == "le":
                    stack.push(rand_1 <= rand_2)
                elif symbol == "eq":
                    stack.push(rand_1 == rand_2)
                elif symbol == "ne":
                    stack.push(rand_1 != rand_2)
                elif symbol == "or":
                    stack.push(rand_1 or rand_2)
                elif symbol == "&":
                    stack.push(rand_1 and rand_2)
                elif symbol == "aug":
                    if isinstance(rand_1, tuple):
                        stack.push(rand_1 + (rand_2,))
                    else:
                        stack.push((rand_1, rand_2))
            except Exception as e:
                print(f"Error in operator {symbol}: {e}")
                exit(1)

        # Rule 7: Unary operators
        elif symbol in uop:
            if len(stack.stack) < 1:
                print(f"Error: Stack has {len(stack.stack)} items, need 1 for unary operator {symbol}")
                exit(1)
            rand = stack.pop()
            if symbol == "not":
                stack.push(not rand)
            elif symbol == "neg":
                # print(f"Applying negation to {rand}")  # Debug
                # print(f"Stack before negation: {stack.stack}")  # Debug
                stack.push(-rand)
                # print(f"Result after negation: ")  # Debug


        # Rule 8: Beta (conditional)
        elif symbol == "beta":
            if len(stack.stack) < 1:
                print(f"Error: Stack has {len(stack.stack)} items, need 1 for beta")
                exit(1)
            B = stack.pop()
            else_part = control.pop()
            then_part = control.pop()
            if B:
                control.extend(then_part.body)
            else:
                control.extend(else_part.body)

        # Rule 9: Tau
        elif isinstance(symbol, Tau):
            n = symbol.number
            if len(stack.stack) < n:
                print(f"Error: Stack has {len(stack.stack)} items, need {n} for tau")
                exit(1)
            tau_list = []
            for _ in range(n):
                tau_list.append(stack.pop())
            stack.push(tuple((tau_list)))

        # Rule 12: Y*
        elif symbol == "Y*":
            stack.push(symbol)

    # Format output
    if len(stack.stack) == 0:
        print("Error: Stack is empty at end of evaluation")
        exit(1)
    result = stack[0]
    if isinstance(result, Lambda):
        result = f"[lambda closure: {result.bounded_variable}: {result.number}]"
    elif isinstance(result, tuple):
        result = list(result)
        for i in range(len(result)):
            if isinstance(result[i], bool):
                result[i] = str(result[i]).lower()
        result = tuple(result)
        if len(result) == 1:
            result = f"({result[0]})"
        else:
            result = f"({', '.join(str(x).replace("'", "") for x in result)})"
    elif isinstance(result, bool):
        result = str(result).lower()
    elif isinstance(result, str):
        result = result.replace("'", "")
    return result

def run_cse_machine(ast):
    global control, control_structures, environments, current_environment, count, print_present
    # Reset state
    control_structures = [[]]
    count = 0
    control = []
    stack.stack = []
    environments = [Environment(0, None)]
    current_environment = 0
    print_present = False

    # print("Generating control structures...")  # Debug
    generate_control_structure(ast, 0, current_environment)
    # print(f"Control structure 0: {control_structures[0]}")  # Debug
    # print(f"Total control structures generated: {len(control_structures)}")  # Debug
    #print control structures
    # Uncomment the following lines if you want to see the control structures
    # for i, cs in enumerate(control_structures):
    #     print(f"Control structure {i}: {cs}")

    control.append(environments[0].name)
    control.extend(control_structures[0])
    stack.push(environments[0].name)
    
    # print("Starting CSE evaluation...")  # Debug
    result = apply_rules()
    # if print_present:
    #     print(result)
    return result