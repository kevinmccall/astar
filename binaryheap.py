class MaxHeap:
    def __init__(self) -> None:
        self.tree = []
        self.length = 0
    
    def _max_heapify(self):
        pass

    def append(self, val):
        self.tree.append(val)
        self.length += 1
        parent_index = self._get_parent(self.length)
        if self.tree[parent_index] < val:
            self.tree[self.length] = self.tree[parent_index]
            self.tree[parent_index] = val
    
    
    def _get_parent(self, n):
        return n // 2

    def _get_left(self, n):
        return n * 2
    
    def _get_right(self, n):
        return n * 2