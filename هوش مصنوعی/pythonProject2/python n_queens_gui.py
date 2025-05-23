#علی مانده زاده 40173116
import tkinter as tk
from tkinter import messagebox
import random

#الگوریتم ژنتیک با جایگشت
def fitness(state):
    # چون state یک جایگشت است، سطرها یکتا هستند؛ فقط قطرها بررسی می‌شن
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(state[i] - state[j]) == abs(i - j):  # برخورد در قطر
                conflicts += 1
    return -conflicts  # برای مرتب‌سازی نزولی

def mutate(state):
    new_state = state[:]
    i, j = random.sample(range(len(state)), 2)
    new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state

def crossover(parent1, parent2):
    # Ordered Crossover (OX) مناسب برای جایگشت‌ها
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[start:end] = parent1[start:end]
    ptr = 0
    for gene in parent2:
        if gene not in child:
            while child[ptr] is not None:
                ptr += 1
            child[ptr] = gene
    return child

def generate_population(n, size):
    base = list(range(n))
    return [random.sample(base, n) for _ in range(size)]

def run_genetic(n, max_generations=1000, population_size=100):
    population = generate_population(n, population_size)
    for _ in range(max_generations):
        population = sorted(population, key=fitness, reverse=True)
        if fitness(population[0]) == 0:
            return population[0]
        next_gen = population[:10]
        while len(next_gen) < population_size:
            p1, p2 = random.choices(population[:50], k=2)
            child = crossover(p1, p2)
            if random.random() < 0.3:
                child = mutate(child)
            next_gen.append(child)
        population = next_gen
    return None

#الگوریتم Backtracking
def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i]:
            return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j]:
            return False
    for i, j in zip(range(row, n), range(col, -1, -1)):
        if board[i][j]:
            return False
    return True

def solve_bt(board, col, n):
    if col >= n:
        return True
    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = 1
            if solve_bt(board, col + 1, n):
                return True
            board[i][col] = 0
    return False

def run_backtracking(n):
    board = [[0] * n for _ in range(n)]
    if solve_bt(board, 0, n):
        state = [row.index(1) for row in board]
        return state
    return None

#رابط گرافیکی(GUI)
CELL_SIZE = 50
PADDING = 10

def draw_board(canvas, state):
    canvas.delete("all")
    if state is None:
        messagebox.showerror("خطا", "راه‌حلی پیدا نشد!")
        return
    n = len(state)
    for row in range(n):
        for col in range(n):
            x1 = PADDING + col * CELL_SIZE
            y1 = PADDING + row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            fill = "white" if (row + col) % 2 == 0 else "gray"
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill)
            if state[col] == row:
                canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="♛", font=("Arial", 24), fill="red")

def solve_and_draw(algorithm, n, canvas):
    if algorithm == "backtracking":
        state = run_backtracking(n)
    elif algorithm == "genetic":
        state = run_genetic(n)
    else:
        state = None
    draw_board(canvas, state)

def create_main_window():
    window = tk.Tk()
    window.title("N Queens Solver - Genetic & Backtracking")

    # انتخاب اندازه n
    tk.Label(window, text="N (تعداد وزیرها):").pack()
    entry_n = tk.Entry(window)
    entry_n.insert(0, "8")
    entry_n.pack()

    canvas = tk.Canvas(window, width=600, height=600)
    canvas.pack(pady=10)

    def run_bt():
        try:
            n = int(entry_n.get())
            solve_and_draw("backtracking", n, canvas)
        except:
            messagebox.showerror("خطا", "عدد معتبر وارد کنید!")

    def run_gen():
        try:
            n = int(entry_n.get())
            solve_and_draw("genetic", n, canvas)
        except:
            messagebox.showerror("خطا", "عدد معتبر وارد کنید!")

    frame = tk.Frame(window)
    frame.pack()

    tk.Button(frame, text="حل با Backtracking", command=run_bt).pack(side=tk.LEFT, padx=10)
    tk.Button(frame, text="حل با Genetic", command=run_gen).pack(side=tk.RIGHT, padx=10)

    window.mainloop()

if __name__ == "__main__":
    create_main_window()
