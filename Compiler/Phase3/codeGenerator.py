class TACGenerator:
    """
    Three-Address Code (TAC) Generator for grammar G.
    
    This class generates TAC quadruples from an Abstract Syntax Tree (AST) representation
    produced by the parser. It supports expressions, assignments, control flow structures,
    and function returns.
    """
    def __init__(self):
        """
        Initializes the TAC generator.
        - `quadruples`: Stores the list of generated TAC instructions.
        - `temp_var_counter`: Counter for generating unique temporary variables.
        - `label_counter`: Counter for generating unique labels for control flow.
        """
        self.quadruples = []
        self.temp_var_counter = 0
        self.label_counter = 0

    def generate_temp_var(self):
        """Generates a new temporary variable for storing intermediate results."""
        self.temp_var_counter += 1
        return f"t{self.temp_var_counter}"

    def generate_label(self):
        """Generates a new label for control flow (e.g. loops, conditionals)."""
        self.label_counter += 1
        return f"L{self.label_counter}"

    def reset_counters(self):
        """Resets counters for temporary variables and labels when generating a new program."""
        self.temp_var_counter = 0
        self.label_counter = 0
        self.quadruples = []

    def get_tac_code(self):
        """
        Converts the generated TAC quadruples into readable TAC instructions.
        
        Returns:
            str: Formatted TAC code as a string.
        """
        tac_code = ""
        for quad in self.quadruples:
            op, arg1, arg2, result = quad
            if op == ':=':
                tac_code += f"{result} = {arg1}\n"
            elif op in ['+', '-', '*', '/', 'and', 'or']:
                tac_code += f"{result} = {arg1} {op} {arg2}\n"
            elif op in ['<', '<=', '=', '<>', '>=', '>']:
                tac_code += f"{result} = {arg1} {op} {arg2}\n"
            elif op == 'ifgoto':
                tac_code += f"if {arg1} goto {arg2}\n"
            elif op == 'goto':
                tac_code += f"goto {result}\n"
            elif op == 'label':
                tac_code += f"{result}:\n"
            elif op == 'return':
                tac_code += f"return {arg1}\n"
            else:
                raise ValueError(f"Unknown TAC operation: {op}")
        return tac_code

    def generate_program_tac(self, program_node):
        """Generates TAC for the entire program, including declarations and the main block."""
        self.reset_counters()
        self.generate_decList_tac(program_node['decList'])
        self.generate_block_tac(program_node['block'])

        return self.get_tac_code()


    def generate_decList_tac(self, decList_node):
        """Processes the list of declarations, if present."""
        if not decList_node or decList_node['type'] == 'funcList' and decList_node.get('empty', False):
            return
        if decList_node['type'] == 'decList' and 'decs' in decList_node:
            self.generate_decs_tac(decList_node['decs'])
            self.generate_decList_tac(decList_node['decList'])


    def generate_decs_tac(self, decs_node):
        """Processes individual variable declarations."""
        if decs_node['type'] == 'decs' and decs_node.get('empty', False):
            return
        if decs_node['type'] == 'decs':
            self.generate_varList_tac(decs_node['varList'])


    def generate_varList_tac(self, varList_node):
        """Processes a list of declared variables (no TAC needed for declarations)."""
        if varList_node['type'] == 'varList':
            if varList_node['varList']:
                self.generate_varList_tac(varList_node['varList'])
            pass # No TAC for declarations


    def generate_block_tac(self, block_node):
        """Processes a block of statements."""
        if block_node['type'] == 'block':
            self.generate_stmtList_tac(block_node['stmtList'])


    def generate_stmtList_tac(self, stmtList_node):
        """Processes a list of statements recursively."""
        if stmtList_node['type'] == 'stmtList':
            if stmtList_node['stmtList']:
                self.generate_stmtList_tac(stmtList_node['stmtList'])
            self.generate_stmt_tac(stmtList_node['stmt'])

    def generate_stmt_tac(self, stmt_node):
        """Processes an individual statement and generates the corresponding TAC instruction."""
        if stmt_node['type'] == 'stmt':
            stmt_type = stmt_node['stmtType']

            # Assignment statement
            if stmt_type == 'assign':
                expr_result = self.generate_expr_tac(stmt_node['expr'])
                var_name = stmt_node['id'][0]
                self.quadruples.append((':=', expr_result, '_', var_name))

            # If-then statement
            elif stmt_type == 'if_then':
                expr_result = self.generate_expr_tac(stmt_node['expr'])
                label_true = self.generate_label()
                label_end_if = self.generate_label()
                self.quadruples.append(('ifgoto', expr_result, label_true, '_'))
                self.quadruples.append(('goto', '_', '_', label_end_if))
                self.quadruples.append(('label', '_', '_', label_true))
                self.generate_stmt_tac(stmt_node['then_stmt'])
                self.quadruples.append(('label', '_', '_', label_end_if))

            # If-then-else statement
            elif stmt_type == 'if_then_else':
                expr_result = self.generate_expr_tac(stmt_node['expr'])
                label_true = self.generate_label()
                label_false = self.generate_label()
                label_end_if = self.generate_label()
                self.quadruples.append(('ifgoto', expr_result, label_true, '_'))
                self.quadruples.append(('goto', '_', '_', label_false))
                self.quadruples.append(('label', '_', '_', label_true))
                self.generate_stmt_tac(stmt_node['then_stmt'])
                self.quadruples.append(('goto', '_', '_', label_end_if))
                self.quadruples.append(('label', '_', '_', label_false))
                self.generate_stmt_tac(stmt_node['else_stmt'])
                self.quadruples.append(('label', '_', '_', label_end_if))

            # While loop
            elif stmt_type == 'while':
                label_start_while = self.generate_label()
                label_loop_body = self.generate_label() 
                label_end_while = self.generate_label()
                self.quadruples.append(('label', '_', '_', label_start_while)) 
                expr_result = self.generate_expr_tac(stmt_node['expr'])
                self.quadruples.append(('ifgoto', expr_result, label_loop_body, '_'))
                self.quadruples.append(('goto', '_', '_', label_end_while))
                self.quadruples.append(('label', '_', '_', label_loop_body))
                self.generate_stmt_tac(stmt_node['stmt'])
                self.quadruples.append(('goto', '_', '_', label_start_while))
                self.quadruples.append(('label', '_', '_', label_end_while))
            
            # Return statement
            elif stmt_type == 'return':
                expr_result = self.generate_expr_tac(stmt_node['expr'])
                self.quadruples.append(('return', expr_result, '_', '_'))
            
            # Block statement (nested scope)
            elif stmt_type == 'block':
                self.generate_block_tac(stmt_node['block'])


    def generate_expr_tac(self, expr_node):
        """Processes an expression and generates TAC for it."""
        if expr_node['type'] == 'expr':
            expr_type = expr_node['exprType']

            # Binary operations
            if expr_type == 'binary_op':
                left_result = self.generate_expr_tac(expr_node['left'])
                right_result = self.generate_expr_tac(expr_node['right'])
                temp_var = self.generate_temp_var()
                self.quadruples.append((expr_node['op'], left_result, right_result, temp_var))
                return temp_var

            # Relational operations
            elif expr_type == 'rel_op':
                left_result = self.generate_expr_tac(expr_node['left'])
                right_result = self.generate_expr_tac(expr_node['right'])
                temp_var = self.generate_temp_var()
                self.quadruples.append((expr_node['op'], left_result, right_result, temp_var))
                return temp_var

            # Literals
            elif expr_type == 'literal':
                temp_var = self.generate_temp_var()
                literal_value = expr_node['value'][0] if isinstance(expr_node['value'], tuple) else expr_node['value']
                self.quadruples.append((':=', literal_value, '_', temp_var))
                return temp_var

            # Identifiers
            elif expr_type == 'id':
                return expr_node['id'][0]

        return None