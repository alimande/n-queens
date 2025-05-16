import tkinter as tk
from tkinter import messagebox

class NQueensSolver:
    def __init__(self, n):
        self.n = n
        self.board = [[0] * n for _ in range(n)]
    #Backtracking algorithms for 4=< n <= 8
    def is_safe(self, row, col):
        # Check column
        for i in range(row):
            if self.board[i][col] == 1:
                return False

        # Check upper left diagonal
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        # Check upper right diagonal
        for i, j in zip(range(row, -1, -1), range(col, self.n)):
            if self.board[i][j] == 1:
                return False

        return True

    def solve_n_queens(self, row=0):
        if row >= self.n:
            return True

        for col in range(self.n):
            if self.is_safe(row, col):
                self.board[row][col] = 1
                if self.solve_n_queens(row + 1):
                    return True
                self.board[row][col] = 0

        return False

    def get_solution(self):
        if self.solve_n_queens():
            return self.board
        else:
            return None

# GUI Implementation
def draw_board(canvas, solution):
    canvas.delete("all")
    n = len(solution)
    cell_size = 50

    for i in range(n):
        for j in range(n):
            x0, y0 = j * cell_size, i * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            color = "white" if (i + j) % 2 == 0 else "gray"
            canvas.create_rectangle(x0, y0, x1, y1, fill=color)

            if solution[i][j] == 1:
                canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill="red")

def solve_and_display():
    try:
        n = int(entry_n.get())
        solver = NQueensSolver(n)
        solution = solver.get_solution()

        if solution:
            draw_board(canvas, solution)
        else:
            messagebox.showerror("Error", f"No solution exists for {n}-Queens")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer")

# Main GUI Window
root = tk.Tk()
root.title("N-Queens Solver")

frame = tk.Frame(root)
frame.pack(pady=10)

label = tk.Label(frame, text="Enter N (number of queens):")
label.pack(side=tk.LEFT)

entry_n = tk.Entry(frame, width=5)
entry_n.pack(side=tk.LEFT)

button_solve = tk.Button(frame, text="Solve", command=solve_and_display)
button_solve.pack(side=tk.LEFT, padx=5)

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack(pady=10)

root.mainloop()

#علی مانده زاده 40173116