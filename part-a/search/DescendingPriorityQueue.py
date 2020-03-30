from queue import PriorityQueue

class DescendingPriorityQueue(PriorityQueue):

    def put(self, elem):
        PriorityQueue.put(self, (elem[0] * -1, elem[1]))

    def get(self):
        elem = PriorityQueue.get(self)
        return (elem[0] * -1, elem[1])
