from lexer import Lexer   # Import the Lexer class for tokenization.

if __name__ == '__main__':
    # Create an instance of the Lexer class.
    lexer = Lexer()
    tokens = [] # List to store tokens.

    # Open the input file and read its content.
    with open('input.txt', 'r') as input:
        lines = ''.join(input.readlines())  # Read all lines and join them into a single string.
        tokens = lexer.tokenize(lines)  # Tokenize the input content.

    # Close the input file (On most systems, file is closed at the end of `with` block).
    input.close()
    

    # Open the output file for writing.
    with open('output.txt', 'w') as output:
        # Write student name, surname and student ID as a header.
        output.write(
            'Mohammad Taha Karbalaee Esmaeili - 40121803' + ' ' * 10 + 'محمد طاها کربلای اسمعیلی - ۴۰۱۲۱۸۰۳\n'
            )

        # Write each token in the formatted output.
        for token in tokens:
            if token.type in ('IDENTIFIER', 'INTEGER_NUMBER', 'REAL_NUMBER'):
                # For specific tokens, include their value and symbol table index.
                output.write(
                    str(token.value[0]) + ' ' * (30 - len(str(token.value[0]))) + f'<{token.type}, {token.value[1]}>\n'
                    )
            else:
                # For other tokens, only include their value and type.
                output.write(
                    token.value + ' ' * (30 - len(token.value)) + f'<{token.type}, ->\n'
                    )
    
    # Close the output file.
    output.close()