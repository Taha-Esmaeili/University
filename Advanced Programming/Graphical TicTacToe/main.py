import random as r
import tkinter as tk
from tkinter import messagebox

class Game:
    '''
    Attributes:
        values: a 3x3 matrix representing the Tic-Tac-Toe board
    
    Methods:
        __init__(self):
            Initializes a new instance of the Game class with an empty 3x3 board.

        AI(self):
            Determines the next move for the computer player using a simple AI logic.
        
        Check(self):
            Checks the current state of the Tic-Tac-Toe board to determine if there is a winner or a tie
    '''
    def __init__(self):
        """
        Parameters:
        - None

        Attributes:
        - values: a 3x3 matrix representing the Tic-Tac-Toe board
        """
        self.values = [['' for ـ in range(3)] for _ in range(3)]

    def AI(self):
        """
        Parameters:
        - None

        Returns:
        - Tuple (row, col): the next move for the computer player
        """
        # AI logic to determine the next move for the computer player

        #Check vertically
        for player in ('O','X'): # Firstly check the winning situation for AI move (O), then check for blocking player winnig move (X)
            for row in range(3):
                for col in range(3):
                    if self.values[row-1][col]==self.values[row-2][col]==player!=self.values[row][col] and self.values[row][col]=='':
                        return (row,col)

        #Check horizontally
            for row in range(3):
                for col in range(3):
                    if self.values[row][col-1]==self.values[row][col-2]==player!=self.values[row][col] and self.values[row][col]=='':
                        return (row,col)
        
        #Check diagonally
            for row in range(3):
                if self.values[row-1][row-1]==self.values[row-2][row-2]==player!=self.values[row][row] and self.values[row][row]=='':
                    return (row,row)


        #Check corners
        for row in (0,2):
            for col in (0,2):
                if self.values[row][col]=='':
                    return (row,col)
        
        # Check if the center is free
        if self.values[1][1] == '':
            return (1,1)
        
        #Check if the final move need to win or block the opponent move
        for row,col in ((0,1), (1,0), (1,2), (2,1)):
            if self.values[row][col] == '':
                return (row,col)

    def Check(self):
        """
        Parameters:
        - None

        Returns:
        - str or None: 'X' if player X wins, 'O' if player O wins, 'Tie' for a tie, None if the game is ongoing
        """
        # Checks the current state of the Tic-Tac-Toe board to determine if there is a winner or a tie

        #Check horizontally
        for row in range(3):
            if self.values[row][0]==self.values[row][1]==self.values[row][2]:
                return self.values[row][0]
            
        #Check vertically
        for col in range(3):
            if self.values[0][col]==self.values[1][col]==self.values[2][col]:
                return self.values[0][col]
        
        #Check diognally
        if self.values[0][0]==self.values[1][1]==self.values[2][2]:
            return self.values[0][0]
        if self.values[0][2]==self.values[1][1]==self.values[2][0]:
            return self.values[0][2]
        

        #Check Tie statement
        empty_cells = 0
        for row in range(3):
            for col in range(3):
                if self.values[row][col] == '':
                    empty_cells += 1
        
        if empty_cells == 0:
            return 'Tie'
        
        return None


class GUI:
    '''
    Attributes:
        root: Tkinter root window
        turn: current player's turn (1 or 2)
        computer_score: computer player's score
        player_score: human player's score
        board: Game instance representing the Tic-Tac-Toe game state
        buttons: 3x3 matrix of Tkinter buttons representing the game board
    
    Methods:
        __init__(self, root, turn):
            Initializes a new instance of the GUI class with the specified root window and starting player.
        
        create_buttons(self):
            Creates and configures the GUI buttons for the Tic-Tac-Toe board.
        
        create_labels(self):
            Creates and configures the GUI labels for displaying scores.
        
        click(self, event, row, col):
            Handles the button click event and initiates player moves.
        
        player_move(self, button, row, col):
            Updates the GUI and game state for a player move.
        
        computer_move(self):
            Initiates the computer's move and updates the GUI and game state.
        
        is_position_valid(self, row, col): 
            Checks if the specified position on the board is a valid move.
        
        is_game_continue(self): 
            Checks the current state of the game to determine if it should continue or end.
        
        reset(self):
            Resets the game state and updates the GUI for a new game.
        '''
    def __init__(self, root, turn):
        """
        Parameters:
        - root: Tkinter root window
        - turn: 1 or 2 indicating the starting player

        Attributes:
        - root: Tkinter root window
        - turn: current player's turn (1 or 2)
        - computer_score: computer player's score
        - player_score: human player's score
        - board: Game instance representing the Tic-Tac-Toe game state
        - buttons: 3x3 matrix of Tkinter buttons representing the game board
        """

        # Initialize the GUI for the Tic Tac Toe game
        self.root = root
        self.turn = turn

        # Set up player and computer scores
        self.computer_score = 0
        self.player_score = 0

        # Create a Game instance to handle game logic
        self.board = Game()

        # Initialize a 3x3 grid of buttons
        self.buttons = [['' for _ in range(3)] for _ in range(3)]

        # Create buttons and labels on the GUI
        self.create_buttons()
        self.create_labels()

        # Initialize the randomization
        if self.turn == 2:
            self.computer_move()
            self.turn = 1

    def create_buttons(self):
        """
        Parameters:
        - None

        Returns:
        - None

        Creates and configures the GUI buttons for the Tic-Tac-Toe board
        """
        
        # Create buttons for the Tic Tac Toe grid
        for row in range(3):
            for col in range(3):

                self.buttons[row][col] = tk.Button(text=" ", height=4,width=6, bg= '#1A1A1A' , font=("Helvetica", 18 ), )
                self.buttons[row][col].grid(row = row, column = col )
                # Bind button presses to the click method
                self.buttons[row][col].bind("<ButtonPress>", lambda event, row = row, col = col: self.click(event, row, col) )

    def create_labels(self):
        """
        Parameters:
        - None

        Returns:
        - None

        Creates and configures the GUI labels for displaying scores
        """
        # Create labels to display computer and player scores

        computer_label = tk.Label(text='Computer score: {}'.format(self.computer_score),bg='#1A1A1A',foreground='#C0C0FF',  font=("Helvetica", 18 ))
        computer_label.grid(row=3, column= 0 , columnspan= 3 , sticky='nswe')

        player_label = tk.Label(text='Your score: {}'.format(self.player_score), bg='#1A1A1A',foreground='#C0C0FF', font=("Helvetica", 18 ))
        player_label.grid(row=4, column= 0 , columnspan= 3 , sticky= 'nsew')

    def click(self, event, row, col):
        """
        Parameters:
        - event: Tkinter event object
        - row: row index of the clicked button
        - col: column index of the clicked button

        Returns:
        - None

        Handles the button click event and initiates player moves
        """
        # Handle button click event
        
        button = event.widget

        # Check if the clicked position is valid, make the player move, and trigger computer move if the game continues
        if self.is_position_valid(row,col):
            if self.turn == 1 and self.is_game_continue():
                self.player_move(button , row , col)
                if self.is_game_continue():
                    self.computer_move()

    def player_move(self, button, row, col):
        """
        Parameters:
        - button: Tkinter button object
        - row: row index of the clicked button
        - col: column index of the clicked button

        Returns:
        - None

        Updates the GUI and game state for a player move
        """
        # Handle the player's move

        # Update button appearance and game board
        button.config(text = 'X' , state= 'disabled', disabledforeground= '#7979CD')
        self.board.values[row][col] = 'X'
        self.is_game_continue()

    def computer_move(self):
        """
        Parameters:
        - None

        Returns:
        - None

        Initiates the computer's move and updates the GUI and game state
        """
        # Handle the computer's move
        # Update button appearance and game board
        row , col = self.board.AI()[0] , self.board.AI()[1]
        self.buttons[row][col].config(text = 'O' ,  state= 'disabled', disabledforeground='#EEEEE9')
        self.board.values[row][col] = 'O'
        self.is_game_continue()

    def is_position_valid(self, row, col):
        """
        Parameters:
        - row: row index to check
        - col: column index to check

        Returns:
        - bool: True if the specified position on the board is a valid move, False otherwise
        """
        # Check if a position on the board is valid

        # Returns True if valid, False otherwise
        if self.board.values[row][col]== '':
            return True
        else:
            return False

    def is_game_continue(self):
        """
        Parameters:
        - None

        Returns:
        - bool: True if the game should continue, False otherwise

        Checks the current state of the game to determine if it should continue or end
        """
        
        # Check if the game should continue
        # Display messages for win, lose, or tie
        # Update scores and reset the game if needed
        # Returns True if the game continues, False otherwise

        if self.board.Check() == 'O':
            messagebox.showinfo('Lose','You lost :(')
            self.computer_score += 1
            self.reset()
        
        elif self.board.Check() == 'X':
            messagebox.showinfo('Win','You won :)')
            self.player_score += 1
            self.reset()

        elif self.board.Check() == 'Tie':
            messagebox.showinfo('Tie',"It's a draw /: ")
            self.reset()

        else:
            return True

    def reset(self):
        """
        Parameters:
        - None

        Returns:
        - None

        Resets the game state and updates the GUI for a new game
        """
        # Reset the game board and GUI

        # Create new buttons and labels
        self.buttons = [['' for _ in range(3)] for _ in range(3)]
        self.create_buttons()
        self.board.values = [['' for _ in range(3)] for _ in range(3)]
        self.create_labels()


# Main block of code
if __name__ == '__main__':
    '''
    Creates the main Tkinter window for the Tic Tac Toe game.
    Initializes the GUI with a random turn for the player and computer.
    Starts the Tkinter event loop.
    '''

    # Create the main Tkinter window for the Tic Tac Toe game
    root = tk.Tk()
    root.title('TicTacToe')
    root.resizable(False,False)

    # Initialize the GUI with a random turn for the player and computer
    TicTacToe_GUI = GUI(root , r.randint(1,2))

    # Start the Tkinter event loop
    root.mainloop()
