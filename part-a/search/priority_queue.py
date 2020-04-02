from heapq import heappush, heappop
class PriorityQueue(object):
    """
    This is my version of a Priority Queue implemented with
    a heap as the underlying data structure
    """
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def append(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def pop(self):
        return self.queue.pop(0)
