import ply.yacc as yacc
from lexer import Lexer # The lexer implemented in phase 1

class Parser:
    """
    A parser implementation using PLY (Python Lex-Yacc) for a predefined grammar.
    This parser processes tokens generated by the Lexer class, checks the input against
    the grammar rules, and returns the list of applied production rules.


    Attributes:
        tokens (list): List of tokens imported from the Lexer.
        Productions (dict): Stores production rules with their rule numbers and definitions.
        rule_count (int): Counter for production rule numbers.
        precedence (tuple): Operator precedence and associativity rules for the grammar.
    """


    tokens = Lexer.tokens  # Import token definitions from the Lexer.
    Productions = {}       # Stores production rules and their corresponding definitions.
    rule_count = 1         # Rule counter for numbering productions.

    # Operator precedence and associativity rules.
    precedence = (
        ('left', 'MUL_OP', 'DIV_OP'),   # Multiplication and division have higher precedence.
        ('left', 'ADD_OP', 'SUB_OP'),   # Addition and subtraction.
        ('nonassoc', 'LT_OP', 'LE_OP', 'NE_OP', 'EQ_OP', 'GE_OP', 'GT_OP'),   # Relational operators.
        ('left', 'AND_KW'),   # Logical AND.
        ('left', 'OR_KW')   # Logical OR.
    )

    def __init__(self):
        """
        Initializes the Parser.
        - Creates a Lexer instance for tokenizing input.
        - Builds the parser using PLY's yacc module.
        """
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self, debug=False)
    

    def log_productions(self, rule_no, production):
        """
        Logs a production rule for debugging and analysis purposes.

        Args:
            rule_no (int): Rule number.
            production (str): The production rule as a string.
        """
        self.Productions[self.rule_count] = (rule_no, production)
        self.rule_count += 1

    # Grammar rules start here. Each rule is defined as a method with a docstring.
    def p_start(self, p):
        '''start : PROGRAM_KW IDENTIFIER SEMICOLON decList funcList block'''
        self.log_productions(1, "start -> program id ; decList funcList block")

    def p_decList_1(self, p):
        '''decList : decs'''
        self.log_productions(2, "decList -> decs")

    def p_decList_2(self, p):
        '''decList : decs decList'''
        self.log_productions(3, "decList -> decs decList")

    def p_decs_1(self, p):
        '''decs : type varList SEMICOLON'''
        self.log_productions(4, "decs -> type varList ;")

    def p_decs_2(self, p):
        '''decs : empty'''
        self.log_productions(5, "decs -> ε")

    def p_type_1(self, p):
        '''type : INTEGER_KW'''
        self.log_productions(6, "type -> integer")

    def p_type_2(self, p):
        '''type : REAL_KW'''
        self.log_productions(7, "type -> real")

    def p_type_3(self, p):
        '''type : BOOLEAN_KW'''
        self.log_productions(8, "type -> boolean")

    def p_varList_1(self, p):
        '''varList : IDENTIFIER'''
        self.log_productions(9, "varList -> id")

    def p_varList_2(self, p):
        '''varList : varList COMMA IDENTIFIER'''
        self.log_productions(10, "varList -> varList, id")

    def p_funcList_1(self, p):
        '''funcList : funcList funcDec'''
        self.log_productions(11, "funcList -> funcList funcDec")

    def p_funcList_2(self, p):
        '''funcList : empty'''
        self.log_productions(12, "funcList -> ε")

    def p_funcDec(self, p):
        '''funcDec : FUNCTION_KW IDENTIFIER parameters COLON type decList block'''
        self.log_productions(13, "funcDec -> function id parameters : type decList block")

    def p_parameters(self, p):
        '''parameters : LEFT_PA decList RIGHT_PA'''
        self.log_productions(14, "parameters -> ( decList )")

    def p_block(self, p):
        '''block : BEGIN_KW stmtList END_KW'''
        self.log_productions(15, "block -> begin stmtList end")

    def p_stmtList_1(self, p):
        '''stmtList : stmt'''
        self.log_productions(16, "stmtList -> stmt")

    def p_stmtList_2(self, p):
        '''stmtList : stmtList stmt'''
        self.log_productions(17, "stmtList -> stmtList stmt")

    def p_stmt_1(self, p):
        '''stmt : IDENTIFIER ASSIGN_OP expr SEMICOLON'''
        self.log_productions(18, "stmt -> id := expr ;")

    def p_stmt_2(self, p):
        '''stmt : IF_KW expr THEN_KW stmt'''
        self.log_productions(19, "stmt -> if expr then stmt")

    def p_stmt_3(self, p):
        '''stmt : IF_KW expr THEN_KW stmt ELSE_KW stmt'''
        self.log_productions(20, "stmt -> if expr then stmt else stmt")

    def p_stmt_4(self, p):
        '''stmt : WHILE_KW expr DO_KW stmt'''
        self.log_productions(21, "stmt -> while expr do stmt")

    def p_stmt_5(self, p):
        '''stmt : FOR_KW IDENTIFIER ASSIGN_OP expr TO_KW expr DO_KW stmt'''
        self.log_productions(22, "stmt -> for id := expr to expr do stmt")

    def p_stmt_6(self, p):
        '''stmt : RETURN_KW expr SEMICOLON'''
        self.log_productions(23, "stmt -> return expr ;")

    def p_stmt_7(self, p):
        '''stmt : block'''
        self.log_productions(24, "stmt -> block")

    def p_expr_1(self, p):
        '''expr : expr AND_KW expr'''
        self.log_productions(25, "expr -> expr and expr")

    def p_expr_2(self, p):
        '''expr : expr OR_KW expr'''
        self.log_productions(26, "expr -> expr or expr")

    def p_expr_3(self, p):
        '''expr : expr MUL_OP expr'''
        self.log_productions(27, "expr -> expr * expr")

    def p_expr_4(self, p):
        '''expr : expr DIV_OP expr'''
        self.log_productions(28, "expr -> expr / expr")

    def p_expr_5(self, p):
        '''expr : expr ADD_OP expr'''
        self.log_productions(29, "expr -> expr + expr")

    def p_expr_6(self, p):
        '''expr : expr SUB_OP expr'''
        self.log_productions(30, "expr -> expr - expr")

    def p_expr_7(self, p):
        '''expr : expr relop expr'''
        self.log_productions(31, "expr -> expr relop expr")

    def p_expr_8(self, p):
        '''expr : LEFT_PA expr RIGHT_PA'''
        self.log_productions(32, "expr -> ( expr )")

    def p_expr_9(self, p):
        '''expr : INTEGER_NUMBER'''
        self.log_productions(33, "expr -> integerNumber")

    def p_expr_10(self, p):
        '''expr : REAL_NUMBER'''
        self.log_productions(34, "expr -> realNumber")

    def p_expr_11(self, p):
        '''expr : TRUE_KW'''
        self.log_productions(35, "expr -> true")

    def p_expr_12(self, p):
        '''expr : FALSE_KW'''
        self.log_productions(36, "expr -> false")

    def p_expr_13(self, p):
        '''expr : IDENTIFIER LEFT_PA actualparamlist RIGHT_PA'''
        self.log_productions(37, "expr -> id ( actualparamlist )")

    def p_expr_14(self, p):
        '''expr : IDENTIFIER'''
        self.log_productions(38, "expr -> id")

    def p_actualparamlist_1(self, p):
        '''actualparamlist : expr'''
        self.log_productions(39, "actualparamlist -> expr")

    def p_actualparamlist_2(self, p):
        '''actualparamlist : actualparamlist COMMA expr'''
        self.log_productions(40, "actualparamlist -> actualparamlist, expr")

    def p_actualparamlist_3(self, p):
        '''actualparamlist : IDENTIFIER'''
        self.log_productions(41, "actualparamlist -> id")

    def p_actualparamlist_4(self, p):
        '''actualparamlist : empty'''
        self.log_productions(42, "actualparamlist -> ε")

    def p_relop_1(self, p):
        '''relop : LT_OP'''
        self.log_productions(43, "relop -> <")

    def p_relop_2(self, p):
        '''relop : LE_OP'''
        self.log_productions(44, "relop -> <=")

    def p_relop_3(self, p):
        '''relop : EQ_OP'''
        self.log_productions(45, "relop -> =")

    def p_relop_4(self, p):
        '''relop : NE_OP'''
        self.log_productions(46, "relop -> <>")

    def p_relop_5(self, p):
        '''relop : GE_OP'''
        self.log_productions(47, "relop -> >=")

    def p_relop_6(self, p):
        '''relop : GT_OP'''
        self.log_productions(48, "relop -> >")

    # Rule for empty production.
    def p_empty(self, p):
        '''empty :'''
        pass

    # Error handling rule.
    def p_error(self, p):
        if p:
            print(f"Syntax error at token '{p.type}' with value '{p.value}' on line {p.lineno}")
        else:
            print("Syntax error at EOF")

    def parse(self, data):
        """
        Parses the input data and generates a syntax tree.

        Args:
            data (str): The source code to be parsed.

        Returns:
            The result of the parsing process.
        """
        return self.parser.parse(data)