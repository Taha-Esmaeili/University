from parser import Parser # Import the Parser class to parse the tokenized input and build Abstract Syntax Tree.
from codeGenerator import TACGenerator # Import the TACGenerator to generate TAC codes from AST.

if __name__ == '__main__':
    # Create an object of the Parser class to process the input program.
    parser = Parser()

    # Create an object of the TACGenerator class to process the input program.
    tacgenerator = TACGenerator()

    # Open the input file and read its content.
    with open('input.txt', 'r') as input:
        program = ''.join(input.readlines())  # Read all lines and combine them into a single string.

    
    # Build an AST from input
    ast = parser.parse(program)
    if ast:
       

        tac_code = tacgenerator.generate_program_tac(ast)

    # Open the output file for writing.
        with open('output.txt', 'w') as output:
            # Write student name, surname and student ID as a header.
            output.write(
                'Mohammad Taha Karbalaee Esmaeili - 40121803' + ' ' * 10 + 'محمد طاها کربلای اسمعیلی - ۴۰۱۲۱۸۰۳\n'
                )

            # Wrtie TAC genereated code in the output file
            output.write(tac_code)

        # Close the output file.
        output.close()
    else:
        print("Parsing failed, no TAC generated.")