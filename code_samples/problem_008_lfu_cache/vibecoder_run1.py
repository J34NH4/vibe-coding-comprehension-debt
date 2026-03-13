from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.c = capacity
        self.m = 0
        self.v = {}
        self.f = defaultdict(int)
        self.g = defaultdict(OrderedDict)
    
    def get(self, key):
        if key not in self.v: return -1
        self._u(key)
        return self.v[key]
    
    def put(self, key, value):
        if self.c <= 0: return
        if key in self.v:
            self.v[key] = value
            self._u(key)
            return
        if len(self.v) >= self.c:
            k, _ = self.g[self.m].popitem(last=False)
            del self.v[k]
            del self.f[k]
        self.v[key] = value
        self.f[key] = 1
        self.g[1][key] = True
        self.m = 1
    
    def _u(self, key):
        f = self.f[key]
        self.f[key] += 1
        del self.g[f][key]
        if not self.g[self.m] and self.m == f: self.m += 1
        self.g[f + 1][key] = True