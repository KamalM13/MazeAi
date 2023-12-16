from tkinter import messagebox, Tk
from priority_queue import PriorityQueue

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

    def breadth_first_search(self, queue, start_box, target_box, searching, paths):
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
                        queue.append(neighbour)
        else:
            if searching:
                Tk().wm_withdraw()
                messagebox.showinfo("No Solution", "There is no solution!")
                searching = False
        return searching

    def get_manhattan_heuristic(self, node, goal):
        x_delta = abs(node.x - goal.x)
        y_delta = abs(node.y - goal.y)

        destination = x_delta + y_delta
        return destination

    def Greedy_search(self, queue, start_box,target_box, paths, priority_queue, searching):
        if(len(priority_queue) == 0):
            queue[0].heuristic = self.get_manhattan_heuristic(queue[0], target_box)
            priority_queue.push(queue[0])
        if len(priority_queue) > 0 and searching:
            node = priority_queue.pop()
            current_box = node[2]
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
                        heuristic = self.get_manhattan_heuristic(neighbour, target_box)
                        neighbour.heuristic = heuristic
                        priority_queue.push(neighbour)
        else:
            if searching:
                Tk().wm_withdraw()
                searching = False
        return searching
        #print(priority_queue.get())
