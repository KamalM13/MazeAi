from tkinter import messagebox, Tk
import pygame
import sys
from algorithms import Algorithms
from priority_queue import PriorityQueue

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

    def draw(self, win, color, game):
        pygame.draw.rect(
            win,
            color,
            (
                self.x * game.box_width,
                95 + self.y * game.box_height,
                game.box_width - 2,
                game.box_height - 2,
            ),
        )

    def set_neighbours(self, grid, game):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < game.columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < game.rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


class Toolbar:
    def __init__(self, x, y, width, height):
        pygame.font.init()
        self.reset_button_rect = pygame.Rect(x + width - 100, y + 5, 100, height)
        self.reset_button_color = (255, 255, 255)
        self.reset_button_text = "Reset"
        self.font = pygame.font.Font(None, 36)

    def draw(self, window):
        pygame.draw.rect(window, self.reset_button_color, self.reset_button_rect)
        reset_text = self.font.render(self.reset_button_text, True, (0, 0, 0))
        reset_text_rect = reset_text.get_rect(center=self.reset_button_rect.center)
        window.blit(reset_text, reset_text_rect)


class AlgorithmMenu:
    def __init__(self, x, y, width, height, font, algorithms):
        self.menu_rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.algorithms = algorithms
        self.selected_algorithm = None

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.menu_rect)
        for i, algorithm in enumerate(self.algorithms):
            row = i // 3
            col = i % 3
            text = self.font.render(algorithm, True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(
                    self.menu_rect.x
                    + col * (self.menu_rect.width // 4)
                    + (self.menu_rect.width // 6),
                    self.menu_rect.y + row * 30 + 30,
                )
            )
            window.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, algorithm in enumerate(self.algorithms):
                    row = i // 3
                    col = i % 3
                    text_rect = pygame.Rect(
                        self.menu_rect.x + col * (self.menu_rect.width // 3),
                        self.menu_rect.y + row * 30,
                        self.menu_rect.width // 4,
                        30,
                    )
                    if text_rect.collidepoint(event.pos):
                        self.selected_algorithm = self.algorithms[i]


class window:
    def __init__(self, x, y):
        pygame.font.init()
        self.window_width = x
        self.window_height = y
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.columns = 25
        self.rows = 25
        self.box_width = self.window_width // self.columns
        self.box_height = (self.window_height) // self.rows
        self.grid = self.generate_grid()
        self.set_neighbours(self.grid)
        self.start_box = self.init_start(self.grid[0][0])
        self.queue = [self.start_box]
        self.toolbar = Toolbar(0, 0, self.window_width, 50)
        self.font = pygame.font.Font(None, 36)
        self.toolbar = Toolbar(0, 0, self.window_width, 50)
        self.algorithm_menu = AlgorithmMenu(
            0, 0, self.window_width, 90, self.font, ["DFS", "BFS", "Greedy"]
        )

    def generate_grid(self):
        grid = []
        for i in range(self.columns):
            arr = []
            for j in range(self.rows):
                arr.append(Box(i, j))
            grid.append(arr)
        return grid

    def set_neighbours(self, grid):
        for i in range(self.columns):
            for j in range(self.rows):
                grid[i][j].set_neighbours(grid, self)

    def init_start(self, box):
        box.start = True
        self.draw_boxes(box, [])
        return box

    def draw_boxes(self, box, paths):
        box.draw(self.window, (100, 100, 100), self)
        if box.queued:
            box.draw(self.window, (200, 0, 0), self)
        if box.visited:
            box.draw(self.window, (0, 200, 0), self)
        if box in paths:
            box.draw(self.window, (0, 0, 200), self)

        if box.start:
            box.draw(self.window, (0, 200, 200), self)
        if box.wall:
            box.draw(self.window, (10, 10, 10), self)
        if box.target:
            box.draw(self.window, (200, 200, 0), self)


def main():
    game = window(700, 700)
    algorithm = Algorithms()
    priority_queue = PriorityQueue()
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
                y = pygame.mouse.get_pos()[1] - 95
                # Draw Wall
                if event.buttons[0]:
                    i = x // game.box_width
                    j = y // game.box_height
                    game.grid[i][j].wall = True
                # Set Target
                if event.buttons[2] and not target_box_set:
                    i = x // game.box_width
                    j = y // game.box_height
                    target_box = game.grid[i][j]
                    target_box.target = True
                    target_box_set = True
            game.algorithm_menu.handle_event(event)
            # Start Algorithm
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            # algorithm.Astar_search(grid,rows, columns, [x_coor,y_coor])
            if game.algorithm_menu.selected_algorithm == "DFS":
                searching = algorithm.depth_first_search(
                    game.queue, game.start_box, target_box, searching, paths
                )
                # Tk().wm_withdraw()
                # messagebox.showinfo("Information", game.algorithm_menu.selected_algorithm)
            elif game.algorithm_menu.selected_algorithm == "BFS":
                searching = algorithm.breadth_first_search(
                    game.queue, game.start_box, target_box, searching, paths
                )
            elif game.algorithm_menu.selected_algorithm == "Greedy":
                searching = algorithm.Greedy_search(
                    game.queue, game.start_box,target_box, paths, priority_queue, searching
                )

        game.window.fill((0, 0, 0))

        for i in range(game.columns):
            for j in range(game.rows):
                box = game.grid[i][j]
                game.draw_boxes(box, paths)
        game.algorithm_menu.draw(game.window)
        game.toolbar.draw(game.window)
        pygame.display.flip()


main()
