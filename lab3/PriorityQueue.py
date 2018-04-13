import heapq


# adapting heapq to our problem
class PriorityQueue:
    def __init__(self, heap):
        self.heap = heap
        heapq.heapify(self.heap)

    def get_heap(self):
        return self.heap

    def extract_min(self):
        return heapq.heappop(self.heap)

    def parent(self, i):
        return int((i - 1) / 2)

    def is_empty(self):
        return len(self.heap) == 0

    def bubble_up(self, i):
        """Takes the node with index i and puts it in the correct position to restore the heap state.
        :param i: index of the node to bubble up
        :return: None
        """
        p = self.parent(i)
        while i > 0 and self.heap[i] < self.heap[p]:
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p
            p = self.parent(i)

    def decrease_key(self, node, old_val, new_val):
        """Updates the distance of the node (old_val) with the new computed distance (new_val), only if the latter
        is greater than the first.

        :param node: identifier of the node, it's not its index
        :param old_val: used as heap.index([old_val, node]) just to find the index of the node that needs the update
        :param new_val: value that will be assigned to the target node - only if new_val > old_val
        :return:
        """
        i = self.heap.index([old_val, node])
        if self.heap[i][0] < new_val:
            return False

        self.heap[i][0] = new_val
        self.bubble_up(i)
        return True
