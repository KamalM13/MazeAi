from tkinter import messagebox, Tk
import pygame
import sys
from algorithms import Algorithms



window_width = 700
window_height = 700

window = pygame.display.set_mode((window_width, window_height))

columns = 25
rows = 25

box_width = window_width // columns
box_height = window_height // rows


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None
        self.heuristic = None

    def draw(self, win, color):
        pygame.draw.rect(
            win,
            color,
            (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2),
        )

    def set_neighbours(self,grid):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


def generate_grid():
    grid = []
    for i in range(columns):
        arr = []
        for j in range(rows):
            arr.append(Box(i, j))
        grid.append(arr)
    return grid

# Set Neighbours
def set_neighbours(grid):
    for i in range(columns):
        for j in range(rows):
            grid[i][j].set_neighbours(grid)

def draw_boxes(box,paths):
    box.draw(window, (100, 100, 100))
    if box.queued:
        box.draw(window, (200, 0, 0))
    if box.visited:
        box.draw(window, (0, 200, 0))
    if box in paths:
        box.draw(window, (0, 0, 200))

    if box.start:
        box.draw(window, (0, 200, 200))
    if box.wall:
        box.draw(window, (10, 10, 10))
    if box.target:
        box.draw(window, (200, 200, 0))


def init_start(grid):
    queue = []
    box = grid
    box.start = True
    box.visited = True
    queue.append(box)
    return box,queue


def main():
    algorithm = Algorithms()
    grid = generate_grid()
    set_neighbours(grid)
    start_box,queue = init_start(grid[0][0])
    begin_search = False
    target_box_set = False
    target_box = None
    searching = True
    paths = []
    while True:
        for event in pygame.event.get():
            # Quit Window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Mouse Controls
            elif event.type == pygame.MOUSEMOTION and begin_search == False:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Draw Wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Set Target
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    x_coor = i
                    y_coor = j
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            # algorithm.Astar_search(grid,rows, columns, [x_coor,y_coor])
            searching = algorithm.depth_first_search(
                queue, start_box, target_box, searching, paths
            )

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                draw_boxes(box,paths)
            
        pygame.display.flip()


main()
