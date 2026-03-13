from collections import defaultdict

class LFUCache:
    def __init__(self, capacity):
        self.c = capacity
        self.v = {}
        self.f = defaultdict(int)
        self.g = defaultdict(list)
        self.m = 0

    def get(self, key):
        if key not in self.v: return -1
        self._u(key)
        return self.v[key]

    def put(self, key, value):
        if self.c == 0: return
        if key in self.v:
            self.v[key] = value
            self._u(key)
        else:
            if len(self.v) >= self.c:
                k = self.g[self.m].pop(0)
                if not self.g[self.m]: self.m += 1
                del self.v[k]
                del self.f[k]
            self.v[key] = value
            self.f[key] = 1
            self.g[1].append(key)
            self.m = 1

    def _u(self, key):
        f = self.f[key]
        self.g[f].remove(key)
        if not self.g[f] and f == self.m: self.m += 1
        self.f[key] += 1
        self.g[f + 1].append(key)