import logging
import tkinter as tk
import random


class SudokuGUI:
    modified_cells = set()

    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.board_frame = tk.Frame(self.master)
        self.button_frame = tk.Frame(self.master)
        self.board_frame.pack()
        self.create_board()
        self.create_buttons()

    def fill_square(self, start_row, start_col):
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[start_row + i][start_col + j] = nums.pop()

    def create_board(self):
        self.modified_cells.clear()
        padding = 10
        cell_size = 50
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(0, 9, 3):
            self.fill_square(i, i)
        self.initial_board = [
            row[:] for row in self.board
        ]  # Store the initial state of the board
        self.solve_sudoku(self.board)  # Solve the generated Sudoku board
        self.remove_numbers()  # Remove some numbers to create the puzzle
        board_size = cell_size * 9 + 2 * padding
        if hasattr(self, "canvas"):
            self.canvas.destroy()

        # Create a new canvas for the board
        self.canvas = tk.Canvas(
            self.board_frame, width=board_size, height=board_size, bg="white"
        )
        self.canvas.pack()

        for i in range(9):
            for j in range(9):
                x0 = padding + j * cell_size
                y0 = padding + i * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                if self.board[i][j] == 0:
                    self.modified_cells.add((i, j))
                cell_value = self.board[i][j]
                if cell_value != 0:
                    self.canvas.create_text(
                        x0 + cell_size / 2,
                        y0 + cell_size / 2,
                        text=cell_value,
                        font=("Helvetica", 16),
                    )
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

    def remove_numbers(self):
        # Remove some numbers from the solved Sudoku board to create the puzzle
        for _ in range(40):  # Adjust the number of numbers to remove as needed
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            self.modified_cells.add((row, col))  # Track modified cell
            self.board[row][col] = 0

    def is_valid(self, board, row, col, num):
        # Check if the number is already present in the row
        for i in range(9):
            if board[row][i] == num:
                return False
        # Check if the number is already present in the column
        for i in range(9):
            if board[i][col] == num:
                return False
        # Check if the number is already present in the 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(self, board):
        # Find an empty cell
        empty_cell = self.find_empty_cell(board)
        if not empty_cell:
            return True  # Board is solved
        row, col = empty_cell
        # Try each number from 1 to 9
        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0  # Backtrack if solution is not possible
        return False  # No solution found

    def find_empty_cell(self, board):
        # Find an empty cell in the board (cell with value 0)
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None  # No empty cell found

    def solve_sudoku_gui(self):
        # Solve the Sudoku board and update the GUI
        self.solve_sudoku(self.board)
        self.update_board_gui()

    # def update_board_gui(self):
    #     # Update the Sudoku board GUI with the solved board
    #     self.canvas.delete("all")
    #     padding = 10
    #     cell_size = 50
    #     board_size = cell_size * 9 + 2 * padding
    #     for i in range(9):
    #         for j in range(9):
    #             x0 = padding + j * cell_size
    #             y0 = padding + i * cell_size
    #             x1 = x0 + cell_size
    #             y1 = y0 + cell_size
    #             cell_value = self.board[i][j]
    #             self.canvas.create_text(
    #                 x0 + cell_size / 2,
    #                 y0 + cell_size / 2,
    #                 text=cell_value,
    #                 font=("Helvetica", 16),
    #             )
    #             self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

    def update_board_gui(self):
        # Clear the canvas
        self.canvas.delete("all")
        padding = 10
        cell_size = 50
        board_size = cell_size * 9 + 2 * padding
        for i in range(9):
            for j in range(9):
                x0 = padding + j * cell_size
                y0 = padding + i * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size
                cell_value = self.board[i][j]
                if cell_value != 0:
                    if (
                        i,
                        j,
                    ) in self.modified_cells:  # Check if cell was modified during solving
                        self.canvas.create_rectangle(
                            x0, y0, x1, y1, fill="light gray", outline="black"
                        )
                    self.canvas.create_text(
                        x0 + cell_size / 2,
                        y0 + cell_size / 2,
                        text=cell_value,
                        font=("Helvetica", 16),
                    )
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

    def create_buttons(self):
        self.button_frame.pack(pady=10)

        solve_button = tk.Button(
            self.button_frame,
            text="Solve",
            command=self.solve_sudoku_gui,
            bg="black",
            fg="white",
            padx=10,
            pady=5,
            bd=0,
            width=10,
            height=2,
        )
        solve_button.pack(
            side=tk.LEFT, padx=(0, 10)
        )  # Add horizontal space between buttons
        new_puzzle_button = tk.Button(
            self.button_frame,
            text="New Puzzle",
            command=self.generate_new_puzzle,
            bg="gray",
            padx=10,
            pady=5,
            bd=0,
            width=10,
            height=2,
        )
        new_puzzle_button.pack(side=tk.LEFT)

    def generate_new_puzzle(self):
        self.create_board()

    def remove_numbers(self):
        # Remove some numbers from the solved Sudoku board to create the puzzle
        for _ in range(40):  # Adjust the number of numbers to remove as needed
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            self.board[row][col] = 0


def main():
    root = tk.Tk()
    sudoku_gui = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
