from tkinter import messagebox, Tk


class Algorithms:
    def depth_first_search(self, queue, start_box, target_box, searching, paths):
        if len(queue) > 0 and searching:
            current_box = queue.pop(0)
            current_box.visited = True
            if current_box == target_box:
                searching = False
                while current_box.prior != start_box:
                    paths.append(current_box.prior)
                    current_box = current_box.prior
            else:
                for neighbour in current_box.neighbours:
                    if not neighbour.queued and not neighbour.wall:
                        neighbour.queued = True
                        neighbour.prior = current_box
                        queue.insert(0, neighbour)
        else:
            if searching:
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There is no solution!")
                searching = False
        return searching

    def breadth_first_search(self, queue, start_box, target_box):
        path = []
        searching = True
        while searching:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False
        return path

    def get_manhattan_heuristic(self, node, goal):
        x_delta = abs(node[0] - goal[0])
        y_delta = abs(node[1] - goal[1])

        destination = x_delta + y_delta
        return destination

    def Astar_search(self, maze, rows, columns, goal):  # didn't finish yet
        for i in range(columns):
            for j in range(rows):
                if maze[i][j].wall == False:
                    maze[i][j].heuristic = self.get_manhattan_heuristic([i, j], goal)
