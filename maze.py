import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
from queue import Queue


def create_maze(dim):
    #create maze with all walls
    maze = np.ones((dim * 2 + 1, dim * 2 + 1))
    #define start
    x, y = (0, 0)
    maze[2 * x + 1, 2 * y + 1] = 0

    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]
        #define directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx >= 0 and nx < dim and ny >= 0 and ny < dim and maze[2 * nx +
                                                                      1,
                                                                      2 * ny +
                                                                      1] == 1:
                maze[2 * nx + 1, 2 * ny + 1] = 0
                maze[2 * x + 1 + dx, 2 * y + 1 + dy] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()

    #create entry and exit
    maze[1, 0] = 0
    maze[-2, -1] = 0
    return maze


def breadth_first_search(maze):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    start = (1, 1)
    end = (maze.shape[0] - 2, maze.shape[1] - 2)
    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True
    queue = Queue()
    queue.put((start, []))
    while not queue.empty():
        (node, path) = queue.get()
        for dx, dy in directions:
            nx = (node[0] + dx, node[1] + dy)
            if nx == end:
                return path + [nx]
            if nx[0] >= 0 and nx[0] < maze.shape[0] and nx[1] >= 0 and nx[
                    1] < maze.shape[1] and maze[nx] == 0 and not visited[nx]:
                visited[nx] = True
                queue.put((nx, path + [nx]))


def plot_maze(maze, path):
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_edgecolor('white')
    fig.patch.set_linewidth(0)
    ax.imshow(maze, cmap=plt.cm.binary, interpolation='nearest')
    if path is not None:
        x_cords = [x[1] for x in path]
        y_cords = [y[0] for y in path]
        ax.plot(x_cords, y_cords, color='red', linewidth=2)
    #hiding axis
    ax.set_xticks([])
    ax.set_yticks([])
    #adding entry and exit arrows
    ax.arrow(0,
             1,
             .4,
             0,
             fc='green',
             ec='green',
             head_width=0.6,
             head_length=0.6)
    ax.arrow(maze.shape[1] - 1,
             maze.shape[0] - 2,
             0.4,
             0,
             fc='purple',
             ec='purple',
             head_width=0.6,
             head_length=0.6)
    plt.show()


def animate_maze(maze, path=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_edgecolor('white')
    fig.patch.set_linewidth(0)
    ax.imshow(maze, cmap=plt.cm.binary, interpolation='nearest')
    ax.set_xticks([])
    ax.set_yticks([])
    if path is not None:
        line, = ax.plot([], [], color='purple', linewidth=2)

        def init():
            line.set_data([], [])
            return line,

        def update(frame):
            x, y = path[frame]
            line.set_data(*zip(*[(p[1], p[0]) for p in path[:frame + 1]]))
            return line,

        ani = animation.FuncAnimation(fig,
                                      update,
                                      frames=range(len(path)),
                                      init_func=init,
                                      blit=True,
                                      repeat=False,
                                      interval=10)
    ax.arrow(0,
             1,
             .4,
             0,
             fc='green',
             ec='green',
             head_width=0.6,
             head_length=0.6)
    ax.arrow(maze.shape[1] - 1,
             maze.shape[0] - 2,
             0.4,
             0,
             fc='red',
             ec='red',
             head_width=0.6,
             head_length=0.6)
    plt.show()


if __name__ == "__main__":
    #dim = int(input("Enter the dimension of the maze: "))
    maze = create_maze(30)
    path = breadth_first_search(maze)
    animate_maze(maze, path)
