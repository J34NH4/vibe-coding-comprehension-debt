class LRUCache:
    def __init__(self, c):
        self.c, self.d, self.h, self.t = c, {}, Node(), Node()
        self.h.n = self.t
        self.t.p = self.h
    
    def get(self, k):
        if k in self.d:
            self.m(self.d[k])
            return self.d[k].v
        return -1
    
    def put(self, k, v):
        if k in self.d:
            self.d[k].v = v
            self.m(self.d[k])
        else:
            if len(self.d) >= self.c:
                self.r(self.t.p)
            self.a(Node(k, v))
    
    def a(self, n):
        self.d[n.k] = n
        n.n = self.h.n
        n.p = self.h
        self.h.n.p = n
        self.h.n = n
    
    def r(self, n):
        del self.d[n.k]
        n.p.n = n.n
        n.n.p = n.p
    
    def m(self, n):
        self.r(n)
        self.a(n)

class Node:
    def __init__(self, k=0, v=0):
        self.k, self.v, self.p, self.n = k, v, None, None