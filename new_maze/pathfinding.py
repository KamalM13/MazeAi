from tkinter import messagebox, Tk
import pygame
import sys
from algorithms import Algorithms
from priority_queue import PriorityQueue
import random
import button

class MainMenu:
    def __init__(self, x, y, width, height, font="arialblack"):#800 600
        screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.text_color = (255, 255, 255)

        self.font = pygame.font.SysFont(font, 40)
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze solver")

        draw_img = pygame.image.load("new_maze/image/draw_maze.png").convert_alpha()
        generate_img = pygame.image.load("new_maze/image/generate_maze.png").convert_alpha()
        submit_img = pygame.image.load("new_maze/image/submit.png").convert_alpha() #will be updated after internet back :d

        self.draw_button = button.Button(500, 350, draw_img, 1.6)
        self.generate_button = button.Button(50, 350, generate_img, 1.5)
        self.submit_button = button.Button(340, 375, submit_img, 1)

        self.rows_input = button.Input(250, 200)
        self.columns_input = button.Input(250, 300)

        self.column_label = button.Label(screen, "Columns:", 130, 305, 36)
        self.row_label = button.Label(screen, "Rows:", 150, 205, 36)
    def draw_input(self, screen):
        self.rows_input.draw(screen)
        self.columns_input.draw(screen)
    def draw_labels(self,screen):
        self.row_label.draw(screen)
        self.column_label.draw(screen)
    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.menu_rect)
        
        options = ["Select Algorithm", "Reset Maze", "Start Pathfinding"]
        
        for i, option in enumerate(options):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(
                    self.menu_rect.centerx,
                    self.menu_rect.y + i * 30 + 30,
                )
            )
            window.blit(text, text_rect)
            
class Box:
    def __init__(self, i, j, width, height):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.visitedMaze = False
        self.neighbours = []
        self.prior = None
        self.heuristic = None
        self.width = width
        self.height = height
        self.image=pygame.image.load("new_maze/image/block.jpg")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, win, color, game):
        if self.wall:
          win.blit(
                self.image,
                (
                    self.x * game.box_width + 1,
                    95 + self.y * game.box_height + 1,
                ),
            )
        else:
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
    
    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.reset_button_rect.collidepoint(event.pos):
                return 1
            

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
                        self.menu_rect.x + col * (self.menu_rect.width // 4),
                        self.menu_rect.y + row * 30,
                        self.menu_rect.width // 3,
                        30,
                    )
                    if text_rect.collidepoint(event.pos):
                        self.selected_algorithm = self.algorithms[i]
                        # create a messagebox here
                        Tk().wm_withdraw()
                        messagebox.showinfo(
                            "Info",
                            "Please click on a start and end node and then press spacebar to start pathfinding!"
                            + self.selected_algorithm,
                        )


class window:
    def __init__(self, x, y, columns=50, rows=50):
        self.window_width = x
        self.window_height = y
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.columns = columns
        self.rows = rows
        self.box_width = self.window_width // self.columns
        self.box_height = (self.window_height - 95) // self.rows
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
                arr.append(Box(i, j, self.box_width, self.box_height))
            grid.append(arr)
        return grid

    def generate_maze(self):
        # Set all cells as walls
        for i in range(self.columns):
            for j in range(self.rows):
                self.grid[i][j].wall = True

        stack = [(self.start_box.x, self.start_box.y)]

        while len(stack) > 0:
            x, y = stack[-1]
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)
            found = False
            for dx, dy in directions:
                nx, ny = x + 2 * dx, y + 2 * dy

                if (
                    nx >= 0
                    and ny >= 0
                    and nx < self.columns
                    and ny < self.rows
                    and self.grid[nx][ny].wall == True
                ):
                    # Open a path
                    self.grid[nx][ny].wall = False
                    self.grid[x + dx][y + dy].wall = False

                    # Move to the next cell
                    stack.append((nx, ny))
                    found = True
                    break

            if not found:
                stack.pop()

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


def draw_maze(game):
        algorithm = Algorithms()
        priority_queue = PriorityQueue()
        paths = []
        begin_search = False
        target_box_set = False
        target_box = None
        searching = True
        stop = False
        while not(stop):
            for event in pygame.event.get():
                # Quit Window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Mouse Controls
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1] - 95
                    i = x // game.box_width
                    j = y // game.box_height
                    if game.grid[i][j].wall == True:
                        game.grid[i][j].wall = False
                    target_box = game.grid[i][j]
                    target_box.target = True
                elif (event.type == pygame.MOUSEMOTION) and begin_search == False:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1] - 95
                    # Draw Wall
                    if event.buttons[0]:
                        i = x // game.box_width
                        j = y // game.box_height
                        game.grid[i][j].wall = True
                game.algorithm_menu.handle_event(event)
                stop = game.toolbar.handle(event)
                if stop:
                    stop = True
                    return "maze_input"
                # Start Algorithm
                if event.type == pygame.KEYDOWN:
                    begin_search = True

            if begin_search:
                # algorithm.Astar_search(grid,rows, columns, [x_coor,y_coor])
                if game.algorithm_menu.selected_algorithm == "DFS":
                    searching = algorithm.depth_first_search(
                        game.queue, game.start_box, target_box, searching, paths
                    )
                elif game.algorithm_menu.selected_algorithm == "BFS":
                    searching = algorithm.breadth_first_search(
                        game.queue, game.start_box, target_box, searching, paths
                    )
                elif game.algorithm_menu.selected_algorithm == "Greedy":
                    searching = algorithm.Greedy_search(
                        game.queue,
                        game.start_box,
                        target_box,
                        paths,
                        priority_queue,
                        searching,
                    )
            game.window.fill((0, 0, 0))

            for i in range(game.columns):
                for j in range(game.rows):
                    box = game.grid[i][j]
                    game.draw_boxes(box, paths)
            game.algorithm_menu.draw(game.window)
            game.toolbar.draw(game.window)
            pygame.display.flip()

def main():
    pygame.font.init()
    menu = MainMenu(0,0,800,700)
    screen = pygame.display.set_mode((800, 700))
    run = True
    menu_status = "maze_input"
    while run:
        screen.fill((52, 78, 91))
        if menu_status == "menu":
            if menu.draw_button.draw(screen):
                menu_status = "draw_maze"
            if menu.generate_button.draw(screen):
                menu_status = "draw_maze"
                game.generate_maze()
        elif menu_status == "draw_maze":
            menu_status = draw_maze(game)
        elif menu_status == "maze_input":
            menu.draw_input(screen)
            menu.draw_labels(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu.rows_input.rectangle.collidepoint(event.pos):
                        menu.rows_input.active = True
                        menu.rows_input.currentColor = menu.rows_input.active_color
                    else:
                        menu.rows_input.active = False
                        menu.rows_input.currentColor = menu.rows_input.passive_color

                    if menu.columns_input.rectangle.collidepoint(event.pos):
                        menu.columns_input.active = True
                        menu.columns_input.currentColor = menu.columns_input.active_color
                    else:
                        menu.columns_input.active = False
                        menu.columns_input.currentColor = menu.columns_input.passive_color
                if event.type == pygame.KEYDOWN:
                    if menu.rows_input.active:
                        if event.key == pygame.K_BACKSPACE:
                            menu.rows_input.user_text = menu.rows_input.user_text[:-1]
                        else:
                            menu.rows_input.user_text += event.unicode
                    if menu.columns_input.active:
                        if event.key == pygame.K_BACKSPACE:
                            menu.columns_input.user_text = menu.columns_input.user_text[:-1]
                        else:
                            menu.columns_input.user_text += event.unicode
            if menu.submit_button.draw(screen):
                menu_status = "menu"
                game = window(800, 700,int(menu.columns_input.user_text),int(menu.rows_input.user_text))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT:
                    run = False

        pygame.display.flip()
main()
