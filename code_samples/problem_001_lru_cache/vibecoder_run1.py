class LRUCache:
    def __init__(self, c):
        self.c = c
        self.d = {}
        self.h = Node()
        self.t = Node()
        self.h.n = self.t
        self.t.p = self.h
    
    def get(self, k):
        if k in self.d:
            n = self.d[k]
            self.r(n)
            self.a(n)
            return n.v
        return -1
    
    def put(self, k, v):
        if k in self.d:
            n = self.d[k]
            n.v = v
            self.r(n)
            self.a(n)
        else:
            if len(self.d) >= self.c:
                l = self.t.p
                self.r(l)
                del self.d[l.k]
            n = Node(k, v)
            self.d[k] = n
            self.a(n)
    
    def r(self, n):
        n.p.n = n.n
        n.n.p = n.p
    
    def a(self, n):
        n.p = self.h
        n.n = self.h.n
        self.h.n.p = n
        self.h.n = n

class Node:
    def __init__(self, k=0, v=0):
        self.k = k
        self.v = v
        self.p = None
        self.n = None