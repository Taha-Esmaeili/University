import ply.lex as lex

class Lexer:
    # Mapping of reserved words to their token names.
    reserved = {
        'program':  'PROGRAM_KW',
        'function': 'FUNCTION_KW',
        'begin':    'BEGIN_KW',
        'end':      'END_KW',
        'while':    'WHILE_KW',
        'do':       'DO_KW',
        'for':      'FOR_KW',
        'to':       'TO_KW',
        'if':       'IF_KW',
        'then':     'THEN_KW',
        'else':     'ELSE_KW',
        'integer':  'INTEGER_KW',
        'real':     'REAL_KW',
        'boolean':  'BOOLEAN_KW',
        'return':   'RETURN_KW',
        'and':      'AND_KW',
        'or':       'OR_KW',
        'true':     'TRUE_KW',
        'false':    'FALSE_KW'
    }


    # Token list: Includes reserved words and custom tokens.
    tokens = [
        'IDENTIFIER',       # Variable or function names
        'Illegal_Lexeme',   # Invalid lexemes (e.g., numbers starting with 0)
        'INTEGER_NUMBER',   # Integer literals
        'REAL_NUMBER',      # Real literals
        'ASSIGN_OP',        # Assignment operator :=
        'MUL_OP',           # Multiplication operator *
        'DIV_OP',           # Division operator /
        'ADD_OP',           # Addition operator +
        'SUB_OP',           # Subtraction operator -
        'LT_OP',            # Less than operator <
        'LE_OP',            # Less than or equal to operator <=
        'NE_OP',            # Not equal operator <>
        'EQ_OP',            # Equality operator =
        'GE_OP',            # Greater than or equal to operator >=
        'GT_OP',            # Greater than operator >
        'COLON',            # Colon :
        'SEMICOLON',        # Semicolon ;
        'COMMA',            # Comma ,
        'LEFT_PA',          # Left parenthesis (
        'RIGHT_PA'          # Right parenthesis )
    ] + list(reserved.values())   # Add reserved keywords to the token list.

    
    # Regular expressions for token patterns.
    t_ASSIGN_OP  = r':='
    t_MUL_OP     = r'\*'
    t_DIV_OP     = r'/'
    t_ADD_OP     = r'\+'
    t_SUB_OP     = r'-'
    t_LT_OP      = r'='
    t_LE_OP      = r'<='
    t_NE_OP      = r'<>'
    t_EQ_OP      = r'='
    t_GE_OP      = r'>='
    t_GT_OP      = r'>'
    t_COLON      = r':'
    t_SEMICOLON  = r';'
    t_COMMA      = r','
    t_LEFT_PA    = r'\('
    t_RIGHT_PA   = r'\)'
    t_ignore     = ' \t'    # Ignore spaces and tabs.


    def __init__(self):
        """
        Initializes the Lexer object.
        - Compiles the lexer using the PLY `lex` module.
        - Initializes the symbol table as an empty dictionary.
        """
        self.lexer = lex.lex(module=self)
        self.symbol_table = {}


    def get_stno(self, id):
        """
        Get or assign a unique symbol table number for the given identifier.
        Args:
            id (str): Identifier or constant.
        Returns:
            int: Unique index for the identifier in the symbol table.
        """
        if id not in self.symbol_table:
            self.symbol_table[id] = len(self.symbol_table)
        return self.symbol_table[id]


    def t_IDENTIFIER(self, t):
        r'[a-zA-Z]\w*'

        """
        Matches identifiers and reserved keywords.
        - If it's a reserved word, assigns the corresponding token type.
        - Otherwise, adds it to the symbol table and returns as an identifier.
        """
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        if t.type == 'IDENTIFIER':
            t.value = (t.value, self.get_stno(t.value))
        return t

    def t_REAL_NUMBER(self, t):
        r'\d+\.\d+([eE][+-]?\d+)?|\d+([eE][+-]?\d+)'

        """
        Matches real (floating-point) numbers, with optional scientific notation.
        """
        t.value = (float(t.value), self.get_stno(t.value))
        return t

    def t_INTEGER_NUMBER(self, t):
        r'\d+'

        """
        Matches integer numbers.
        - Identifies illegal lexemes (e.g., leading zeroes in multi-digit numbers).
        """
        if t.value[0] == '0' and len(t.value) != 1:
            t.type = 'Illegal_Lexeme'
        else:
            t.value = (int(t.value), self.get_stno(int(t.value)))
        return t

    def t_error(self, t):
        """
        Handles illegal characters.
        - Prints an error message and skips the invalid character.
        """
        print(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
        self.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'

        """
        Tracks newlines to maintain accurate line numbers.
        """
        t.lexer.lineno += len(t.value)

    def tokenize(self, data):
        """
        Tokenizes the input data.
        Args:
            data (str): Source code to tokenize.
        Returns:
            list: List of token objects.
        """
        self.lexer.input(data)
        tokens = []
        while True:
            token = self.lexer.token()
            if not token:
                break
            tokens.append(token)
        return tokens