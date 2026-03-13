from collections import defaultdict

class LFUCache:
    def __init__(self, capacity):
        self.c = capacity
        self.k = {}
        self.f = {}
        self.g = defaultdict(set)
        self.m = 0
        self.s = 0

    def get(self, key):
        if key not in self.k:
            return -1
        self.g[self.f[key]].remove(key)
        if not self.g[self.m] and self.f[key] == self.m:
            self.m += 1
        self.f[key] += 1
        self.g[self.f[key]].add(key)
        return self.k[key]

    def put(self, key, value):
        if self.c <= 0:
            return
        if key in self.k:
            self.k[key] = value
            self.get(key)
            return
        if self.s >= self.c:
            r = self.g[self.m].pop()
            del self.k[r]
            del self.f[r]
            self.s -= 1
        self.k[key] = value
        self.f[key] = 1
        self.g[1].add(key)
        self.m = 1
        self.s += 1