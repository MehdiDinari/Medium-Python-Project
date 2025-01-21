import tkinter as tk
import random
import time
from queue import Queue

CELL_SIZE = 30  # Taille de chaque cellule
ROWS, COLS = 21, 21  # Dimensions du labyrinthe (doivent être impaires)


def generate_maze(rows, cols):
    """Génère un labyrinthe aléatoire."""
    maze = [["#" for _ in range(cols)] for _ in range(rows)]

    def carve_passages(x, y):
        """Creuse des passages de manière récursive."""
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < rows and 0 < ny < cols and maze[nx][ny] == "#":
                maze[x + dx // 2][y + dy // 2] = " "
                maze[nx][ny] = " "
                carve_passages(nx, ny)

    # Initialisation du labyrinthe avec un point de départ
    maze[1][1] = " "
    carve_passages(1, 1)
    maze[1][0] = "O"  # Départ
    maze[rows - 2][cols - 1] = "X"  # Arrivée

    return maze


def create_grid(canvas, maze):
    """Affiche le labyrinthe sur le canvas."""
    rows, cols = len(maze), len(maze[0])
    for i in range(rows):
        for j in range(cols):
            x1, y1 = j * CELL_SIZE, i * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            color = "black" if maze[i][j] == "#" else "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
            if maze[i][j] == "O":
                canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="blue")
            if maze[i][j] == "X":
                canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")


def find_start(maze):
    """Trouve la position de départ."""
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == "O":
                return i, j
    return None


def find_neighbors(maze, row, col):
    """Trouve les voisins valides."""
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] != "#":
            neighbors.append((r, c))
    return neighbors


def animate_path(canvas, path):
    """Anime le chemin trouvé."""
    for row, col in path:
        x1, y1 = col * CELL_SIZE + 5, row * CELL_SIZE + 5
        x2, y2 = x1 + CELL_SIZE - 10, y1 + CELL_SIZE - 10
        canvas.create_oval(x1, y1, x2, y2, fill="green")
        canvas.update()
        time.sleep(0.1)


def find_path(maze, canvas):
    """Trouve le chemin de O à X."""
    start = find_start(maze)
    if not start:
        return

    q = Queue()
    q.put((start, [start]))
    visited = set()
    visited.add(start)

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        # Si on trouve l'arrivée
        if maze[row][col] == "X":
            animate_path(canvas, path)
            return path

        # Explore les voisins
        for neighbor in find_neighbors(maze, row, col):
            if neighbor not in visited:
                visited.add(neighbor)
                q.put((neighbor, path + [neighbor]))


def main():
    """Point d'entrée principal."""
    maze = generate_maze(ROWS, COLS)

    root = tk.Tk()
    root.title("Solveur de Labyrinthe")
    canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE)
    canvas.pack()

    create_grid(canvas, maze)

    # Démarre la résolution après une seconde
    root.after(1000, find_path, maze, canvas)
    root.mainloop()


if __name__ == "__main__":
    main()
