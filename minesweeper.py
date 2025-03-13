import tkinter as tk  # Import tkinter for GUI
from tkinter import messagebox  # Import messagebox for displaying alerts
import random  # Import random for shuffling columns

# Constants
GRID_SIZE = 8  # Define the grid size for Minesweeper (8x8)

# Create the main window
window = tk.Tk()  # Initialize the Tkinter main window
window.title("Minesweeper (8 Queen Strategy)")  # Set the title of the window

# Game variables
board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]  # Initialize the game board with all cells set to 0 (safe)
buttons = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]  # Placeholder for button objects for each cell
mine_positions = []  # List to store positions of mines

# Place mines using the 8-Queen strategy
def place_mines():
    # Use sets to track columns and diagonals that are under attack
    columns = set()  # Track which columns already have mines
    diag1 = set()  # Track left-to-right diagonals (row - col)
    diag2 = set()  # Track right-to-left diagonals (row + col)

    # Backtracking function to place mines row by row
    def solve(row):
        if row == GRID_SIZE:  # If all rows have been filled with mines, the placement is complete
            return True
        for col in range(GRID_SIZE):  # Try placing a mine in each column of the current row
            if col not in columns and (row - col) not in diag1 and (row + col) not in diag2:
                # If placing the mine doesn't conflict with columns or diagonals
                board[row][col] = 1  # Place a mine at the current cell
                mine_positions.append((row, col))  # Add the position to the mine list
                columns.add(col)  # Mark the column as attacked
                diag1.add(row - col)  # Mark the left-to-right diagonal as attacked
                diag2.add(row + col)  # Mark the right-to-left diagonal as attacked

                if solve(row + 1):  # Recursively attempt to place mines in the next row
                    return True

                # Backtrack if placement fails
                board[row][col] = 0  # Remove the mine
                mine_positions.pop()  # Remove the position from the mine list
                columns.remove(col)  # Unmark the column
                diag1.remove(row - col)  # Unmark the left-to-right diagonal
                diag2.remove(row + col)  # Unmark the right-to-left diagonal
        return False  # Return False if no valid placement is found for the current row

    solve(0)  # Start placing mines from the first row

# Calculate the number of adjacent mines for each cell
def calculate_adjacent_mines():
    for row in range(GRID_SIZE):  # Iterate through all rows
        for col in range(GRID_SIZE):  # Iterate through all columns
            if board[row][col] == 1:  # Skip cells with mines
                continue
            # Count mines in all adjacent cells
            board[row][col] = sum(
                board[i][j] == 1  # Check if the cell contains a mine
                for i in range(max(0, row - 1), min(GRID_SIZE, row + 2))  # Row range for adjacent cells
                for j in range(max(0, col - 1), min(GRID_SIZE, col + 2))  # Column range for adjacent cells
            )

# Reveal all mines when the game is over
def reveal_mines():
    for r, c in mine_positions:  # Loop through all mine positions
        buttons[r][c].config(text="*", bg="red", state="disabled", relief=tk.SUNKEN)  # Mark mines with "*"

# Reveal neighbors if the clicked cell has 0 adjacent mines
def reveal_safe_neighbors(row, col):
    for i in range(max(0, row - 1), min(GRID_SIZE, row + 2)):  # Loop through rows of neighboring cells
        for j in range(max(0, col - 1), min(GRID_SIZE, col + 2)):  # Loop through columns of neighboring cells
            if buttons[i][j]["state"] == "normal":  # Check if the cell is not yet revealed
                buttons[i][j].config(text=str(board[i][j]), state="disabled", relief=tk.SUNKEN)  # Reveal the cell
                if board[i][j] == 0:  # If the cell has no adjacent mines, recursively reveal neighbors
                    reveal_safe_neighbors(i, j)

# Handle cell click event
def on_cell_click(row, col):
    if board[row][col] == 1:  # If a mine is clicked
        buttons[row][col].config(text="*", bg="red")  # Show mine and change button color
        reveal_mines()  # Reveal all mines
        messagebox.showinfo("Game Over", "You clicked on a mine!")  # Display game over message
        window.quit()  # Quit the game
    else:  # If a safe cell is clicked
        buttons[row][col].config(text=str(board[row][col]), state="disabled", relief=tk.SUNKEN)  # Show adjacent mine count
        if board[row][col] == 0:  # If there are no adjacent mines, reveal neighbors
            reveal_safe_neighbors(row, col)
        # Check if the player has cleared the board
        if all(buttons[r][c]["state"] == "disabled" or board[r][c] == 1
               for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
            reveal_mines()  # Reveal all mines for clarity
            messagebox.showinfo("Congratulations!", "You cleared the board!")  # Display win message
            window.quit()  # Quit the game

# Initialize the game
def initialize_game():
    place_mines()  # Place mines on the board using the 8-Queens strategy
    calculate_adjacent_mines()  # Calculate adjacent mine counts

    # Create the buttons for the grid and assign the click event
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            buttons[row][col] = tk.Button(window, width=5, height=2, font=("Arial", 18),  # Create a button
                                          command=lambda r=row, c=col: on_cell_click(r, c))  # Bind click event
            buttons[row][col].grid(row=row, column=col)  # Place the button on the grid

# Show the start screen
def show_start_screen():
    tk.Label(window, text="Welcome to Minesweeper!", font=("Arial", 32)).pack(pady=40)  # Add welcome message
    tk.Button(window, text="Start Game", font=("Arial", 16), command=start_game).pack(pady=10)  # Add start button
    tk.Button(window, text="Quit", font=("Arial", 16), command=window.quit).pack(pady=30)  # Add quit button

# Start the game
def start_game():
    for widget in window.winfo_children():  # Remove start screen widgets
        widget.destroy()
    initialize_game()  # Initialize the game board

# Run the game
show_start_screen()  # Show the start screen
window.mainloop()  # Start the Tkinter event loop
