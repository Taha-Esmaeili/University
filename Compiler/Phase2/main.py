from lexer import Lexer     # Import the Lexer class to tokenize the input.
from parser import Parser   # Import the Parser class to parse the tokenized input.

if __name__ == '__main__':
    # Create an object of the Parser class to process the input program.
    parser = Parser()

    # Open the input file and read its content.
    with open('input.txt', 'r') as input:
        program = ''.join(input.readlines())  # Read all lines and combine them into a single string.
    

    # Close the input file (On most systems, file is closed at the end of `with` block).
    input.close()

    # Parse the program using the `Parser` object.
    # The `parse` method analyzes the input string and applies the grammar rules.
    result = parser.parse(program)

    # Open the output file for writing.
    with open('output.txt', 'w') as output:
        # Write student name, surname and student ID as a header.
        output.write(
            'Mohammad Taha Karbalaee Esmaeili - 40121803' + ' ' * 10 + 'محمد طاها کربلای اسمعیلی - ۴۰۱۲۱۸۰۳\n'
            )

        # write each rule and the relevant number on each line.
        for key, value in parser.Productions.items():
            output.write(f"{value[0]}{' ' * (10 - len(str(value[0])))}{value[1]}\n")
 
    # Close the output file.
    output.close()