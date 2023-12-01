from pyamaze import maze,agent


def depth_first_search(maze,start = None):
    if start is None:
        start = (maze.rows,maze.cols)
    visited = [start]
    stack = [start]
    directions = 'ESNW'
    path = {}
    search = []
    while len(stack)>0:
        currentCell = stack.pop()
        search.append(currentCell)
        if currentCell == maze._goal:
            break
        pos = 0
        for d in directions:
            #maze_map returns a dict for all possible directions for the current cell
            if maze.maze_map[currentCell][d] == True:
                match d:
                    case 'E':
                        childCell = (currentCell[0],currentCell[1]+1)
                    case 'W':
                        childCell = (currentCell[0],currentCell[1]-1)
                    case 'N':
                        childCell = (currentCell[0]-1,currentCell[1])
                    case 'S':
                        childCell = (currentCell[0]+1,currentCell[1])
                if childCell not in visited:
                    pos += 1
                    visited.append(childCell)
                    stack.append(childCell)
                    # we store the childcell as key in the dic because it doesn't repeat meaning we have to invert the dict to get the actual solution path
                    path[childCell] = currentCell
        if pos>1:
            maze.markCells.append(currentCell)
    #invert the resulting dict to get the path for the goal
    actualPath = {}
    cell = maze._goal
    while cell != start:
        actualPath[path[cell]] = cell
        cell = path[cell]
    return path,search,actualPath



def create_maze(dim):
    m = maze(dim, dim)
    m.CreateMaze()
    depth_first_search(m)
    return m

def solve_maze(maze):
    path,search,actualPath = depth_first_search(maze)
    a = agent(maze,footprints=True,shape='square',color="green")
    b = agent(maze,1,1,goal = (maze.rows,maze.cols),footprints=True, filled=True,color="cyan")
    c = agent(maze,footprints=True, color="yellow")
    maze.tracePath({a: search}, showMarked=True,delay = 120)
    maze.tracePath({b: path},delay = 120)
    maze.tracePath({c: actualPath},delay = 120)
    maze.run()

if __name__ == "__main__":
    #dim = int(input("Enter the dimension of the maze: "))
    solve_maze(create_maze(8))
