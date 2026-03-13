class LRUCache:
    def __init__(self, c):
        self.c = c
        self.d = {}
        self.h = self.t = None

    def get(self, k):
        if k not in self.d: return -1
        n = self.d[k]
        self._r(n)
        self._a(n)
        return n.v

    def put(self, k, v):
        if k in self.d:
            n = self.d[k]
            n.v = v
            self._r(n)
            self._a(n)
        else:
            n = self._n(k, v)
            self.d[k] = n
            self._a(n)
            if len(self.d) > self.c:
                del self.d[self.t.k]
                self._r(self.t)

    def _n(self, k, v):
        n = type('', (), {'k': k, 'v': v, 'p': None, 'n': None})()
        return n

    def _r(self, n):
        if n.p: n.p.n = n.n
        else: self.h = n.n
        if n.n: n.n.p = n.p
        else: self.t = n.p

    def _a(self, n):
        n.p = n.n = None
        if not self.h:
            self.h = self.t = n
        else:
            n.n = self.h
            self.h.p = n
            self.h = n