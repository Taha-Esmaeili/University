import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox,filedialog

class SudokuGrid:
    """
    Class representing a Sudoku grid and associated operations.
    """
    def __init__(self):
        """
        Initialize a 9x9 Sudoku grid with all cells set to 0.
        """
        self.grid = [[0] * 9 for _ in range(9)]

    def is_valid(self, row, col, num):
        """
        Check if a number can be placed in a specific cell.

        Parameters:
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        num (int): The number to be placed in the cell.

        Returns:
        bool: True if the number can be placed, False otherwise.
        """

        # Check if the number already exists in the row
        if num in self.grid[row]:
            return False

        # Check if the number already exists in the column
        if num in [self.grid[i][col] for i in range(9)]:
            return False

        # Check if the number already exists in the 3x3 section
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False

        return True

    def solve(self):
        """
        Solve the Sudoku puzzle using backtracking.

        Returns:
        bool: True if the puzzle is solved, False if no solution exists.
        """
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True  # Puzzle solved

        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num

                if self.solve():
                    return True

                self.grid[row][col] = 0  # Reset the cell if the solution is not found
        return False

    def find_empty_cell(self):
        """
        Find the next empty cell in the grid.

        Returns:
        tuple: (row, col) of the empty cell, or None if no empty cells exist.
        """
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j  # Return the row and column of the empty cell

        return None

    def generate_puzzle(self, difficulty):
        """
        Generate a Sudoku puzzle by solving a full grid and removing cells based on difficulty.

        Parameters:
        difficulty (int): The number of filled cells to leave in the grid (81 - difficulty).
        """
        self.solve()  # Generate a complete Sudoku solution

        # Remove cells based on the difficulty level
        cells_to_remove = 81 - difficulty
        if cells_to_remove == 81:
            for row in range(9):
                for col in range(9):
                    self.grid[row][col]=0
        else:
            num = 0
            while num !=cells_to_remove:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                if self.grid[row][col] != 0:
                    self.grid[row][col] = 0
                    num += 1
                else :
                    pass

class SudokuGUI:

    """
    Class representing the graphical user interface (GUI) for the Sudoku game.
    """

    def __init__(self, root):
        """
        Initialize the Sudoku GUI.

        Parameters:
        root (Tk): The root window of the tkinter application.
        """
        self.root = root
        self.root.title("Sudoku")

        self.sudoku_grid = SudokuGrid()


        #Get value from radiobuttons
        self.get_level = IntVar()
        self.get_level.set(-1)


        #Create the Sudoku grid
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
    
                if (i in (0, 1, 2, 6, 7, 8) and j in (3, 4, 5)) or (i in (3, 4, 5) and j in (0, 1, 2, 6, 7, 8)):
                    color = "#d9d9d9"
                else:
                    color = "white"
                
                entry = tk.Entry(root, justify="center", font=("Arial", 16, "bold"), width=2 , background=color)
                entry.grid(row=i, column=j, padx=2 , pady=2)
                row.append(entry)
            self.cells.append(row)


        
        # Create buttons
        Easy_button = Radiobutton(self.root, text="Easy",value=50, font=("Helvetica", 11), variable=self.get_level)
        Easy_button.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

        Medium_button = Radiobutton(self.root, text="Medium", value=40, font=("Helvetica", 11), variable=self.get_level)
        Medium_button.grid(row=9, column=3, columnspan=3, padx=5, pady=5)

        Difficult_button = Radiobutton(self.root, text="Difficult", value=30, font=("Helvetica", 11), variable=self.get_level)
        Difficult_button.grid(row=9, column=6, columnspan=3, padx=5, pady=5)

        self.solve_button = tk.Button(root, height=1, width=20, text="Solve",font=("Helvetica", 12), command=self.solve_puzzle, state='disabled')
        self.solve_button.grid(row=10, column=1,columnspan=10, pady=10)

        self.create_button = tk.Button(root,height=1, width=20, text="Create",font=("Helvetica", 12), command=self.generate_puzzle, state='normal')
        self.create_button.grid(row=11, column=1,columnspan=10, pady=10)

        self.create_button = tk.Button(root,height=1, width=20, text="Check",font=("Helvetica", 12), command=self.Check, state='normal')
        self.create_button.grid(row=12, column=1,columnspan=10, pady=10)

        self.create_button = tk.Button(root,height=1, width=20, text="Load",font=("Helvetica", 12), command=self.Load, state='normal')
        self.create_button.grid(row=13, column=1,columnspan=10, pady=10)



    def solve_puzzle(self):
        """
        Solve the Sudoku puzzle displayed on the GUI.
        Checks for duplicates and updates the grid with the solution.
        """
        for row in range(9):
            for col in range(9):
                num = self.cells[row][col].get()
                if num != '':
                    if self.solve_duplicate(row, col, int(num)):
                        return messagebox.showerror("Error", "NO solution found!!! ")
                value = self.cells[row][col].get()
                if value:
                    self.sudoku_grid.grid[row][col] = int(value)
        if self.sudoku_grid.solve():
            self.update_grid()
            messagebox.showinfo("Sudoku", "Puzzle solved!")
        else:
            messagebox.showerror("Sudoku", "No solution found!")


    def solve_duplicate(self, row, col, num):
        """
        Check for duplicate numbers in the current row, column, and 3x3 block in the GUI grid.

        Parameters:
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        num (int): The number to check for duplicates.

        Returns:
        bool: True if a duplicate is found, False otherwise.
        """
        for i in range(9):
            if self.cells[row][i].get() == str(num) and i != col:
                return True

        for i in range(9):
            if self.cells[i][col].get() == str(num) and i != row:
                return True

        block_row = row // 3
        block_col = col // 3
        for i in range(block_row * 3, block_row * 3 + 3):
            for j in range(block_col * 3, block_col * 3 + 3):
                if self.cells[i][j].get() == str(num) and (i != row or j != col):
                    return True

        return False



    def check_duplicate(self, row, col, num):
        """
        Check for duplicate numbers in the current row, column, and 3x3 block in the GUI grid.

        Parameters:
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        num (int): The number to check for duplicates.

        Returns:
        bool: True if a duplicate is found, False otherwise.
        """
        for i in range(9):
            if self.sudoku_grid.grid[row][i] == num and i != col:
                return True

        for i in range(9):
            if self.sudoku_grid.grid[i][col] == num and i != row:
                return True

        block_row = row // 3
        block_col = col // 3
        for i in range(block_row * 3, block_row * 3 + 3):
            for j in range(block_col * 3, block_col * 3 + 3):
                if self.sudoku_grid.grid[i][j] == num and (i != row or j != col):
                    return True

        return False


    def generate_puzzle(self ):
        """
        Generate a new Sudoku puzzle and display it on the GUI.
        """
        self.create_button.config(state='disabled')
        self.solve_button.config(state='active')
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)
                self.cells[i][j].config(fg='black')


        self.sudoku_grid = SudokuGrid()
        self.sudoku_grid.generate_puzzle(difficulty=self.get_level.get()+1)
        self.update_grid()


 
    def update_grid(self):
        """
        Update the GUI grid with the values from the internal Sudoku grid.
        Cells with values are displayed in blue.
        """
        for i in range(9):
            for j in range(9):
                value = self.sudoku_grid.grid[i][j]
                if value != 0:
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(value))
                    self.cells[i][j].config(fg='blue')


    def Check(self):
        """
        Check the current Sudoku puzzle on the GUI for completeness and correctness.
        """
        for row in range(9):
            for column in range(9):
                if self.cells[row][column].get() == '':
                    return messagebox.showwarning("Error", "Each row and column \nneeds to be filled out!")
                elif (int(self.cells[row][column].get()) > 9) or (int(self.cells[row][column].get()) < 0):
                    return messagebox.showwarning("Error", "Numbers must be between 1 and 9")

        for column in range(9):
            values = [self.cells[row][column].get() for row in range(9) if self.cells[row][column].get()]

            if len(set(values)) != len(values):
                return messagebox.showerror('Error', 'Incorrect solution! \n You lost :(')

        messagebox.showinfo("Success", "You won :) ")
        return


    def Load(self):
        """
        Load a Sudoku puzzle from a file and display it on the GUI.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as f:
                content = f.read()
                # Parse the content
                for row, line in enumerate(content.split('\n')) :
                    for col, num in enumerate(line.split(',')) :
                        self.sudoku_grid.grid[row][col] = num.strip()
                        if self.sudoku_grid.grid[row][col] == '0' :
                            self.sudoku_grid.grid[row][col] = 0

                # Update the GUI with the loaded Sudoku
                self.update_grid()
                self.solve_button.config(state='active')


root = tk.Tk()
root.resizable(False,False)
sudoku_gui = SudokuGUI(root)
root.mainloop()
