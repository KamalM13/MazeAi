import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.heap2 = []
        self.counter = 0
        self.counter2 = 0  # Counter to maintain original order

    def push(self, item):
        # Use a tuple as the priority key: (priority, unique_id, item)
        #print(f"heuristic: {item.heuristic[0]}, x:{item.x}, y:{item.y}")
        result = item.heuristic.show()
        priority_key = (result[2][0], self.counter, item)
        heapq.heappush(self.heap, priority_key)
        self.counter += 1

    def push_node(self, item):
        # Use a tuple as the priority key: (priority, unique_id, item)
        #print(f"heuristic: {item[0]}, x:{item[1]}, y:{item[2]}")
        priority_key = (item[0], self.counter2, item)
        heapq.heappush(self.heap2, priority_key)
        self.counter2 += 1

    def pop(self):
        if self.heap:
            # Return the item without the priority key
            return heapq.heappop(self.heap)
        else:
            return False
        
    def pop_node(self):
        if self.heap2:
            # Return the item without the priority key
            return heapq.heappop(self.heap2)
        else:
            return False
    
    def show(self):
        if self.heap2:
            return self.heap2[0]
        
    def __len__(self):
        return len(self.heap)
