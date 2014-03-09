class DSU:
    def __init__(self, vertices):
        # noinspection PyTypeChecker
        self.vertices_index = dict(reversed(pair) for pair in enumerate(vertices))
        self.parents = [None] * len(vertices)
        self.rank = [1] * len(vertices)

    def _find(self, a):
        if self.parents[a] is None:
            return a
        result = self._find(self.parents[a])
        self.parents[a] = result
        return result

    def find(self, a):
        return self._find(self.vertices_index[a])

    def union(self, a, b):
        head1, head2 = self.find(a), self.find(b)
        if head1 == head2:
            return
        if self.rank[head1] == self.rank[head2]:
            self.rank[head1] += 1
            self.parents[head2] = head1
        elif self.rank[head1] > self.rank[head2]:
            self.parents[head2] = head1
        else:
            self.parents[head1] = head2
