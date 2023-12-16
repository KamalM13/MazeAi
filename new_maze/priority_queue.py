import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.counter = 0  # Counter to maintain original order

    def push(self, item):
        # Use a tuple as the priority key: (priority, unique_id, item)
        priority_key = (item.heuristic, self.counter, item)
        heapq.heappush(self.heap, priority_key)
        self.counter += 1

    def pop(self):
        if self.heap:
            # Return the item without the priority key
            return heapq.heappop(self.heap)
        else:
            return False
        
    def __len__(self):
        return len(self.heap)
