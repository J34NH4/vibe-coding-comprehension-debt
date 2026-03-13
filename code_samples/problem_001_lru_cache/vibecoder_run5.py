class LRUCache:
    def __init__(self, c):
        self.c = c
        self.d = {}
        self.h = self.t = type('', (), {'k': 0, 'v': 0, 'p': None, 'n': None})()
        self.h.n = self.t.p = self.t

    def get(self, k):
        if k in self.d:
            n = self.d[k]
            n.p.n, n.n.p = n.n, n.p
            n.p, n.n = self.t.p, self.t
            self.t.p.n = self.t.p = n
            return n.v
        return -1

    def put(self, k, v):
        if k in self.d:
            n = self.d[k]
            n.v = v
            n.p.n, n.n.p = n.n, n.p
            n.p, n.n = self.t.p, self.t
            self.t.p.n = self.t.p = n
        else:
            if len(self.d) == self.c:
                del self.d[self.h.n.k]
                self.h.n = self.h.n.n
                self.h.n.p = self.h
            n = type('', (), {'k': k, 'v': v, 'p': self.t.p, 'n': self.t})()
            self.d[k] = self.t.p.n = self.t.p = n