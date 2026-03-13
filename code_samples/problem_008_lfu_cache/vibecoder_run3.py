from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.c = capacity
        self.kv = {}
        self.kf = {}
        self.fk = defaultdict(OrderedDict)
        self.m = 0
    
    def get(self, key):
        if key not in self.kv:
            return -1
        self._u(key)
        return self.kv[key]
    
    def put(self, key, value):
        if self.c <= 0:
            return
        if key in self.kv:
            self.kv[key] = value
            self._u(key)
            return
        if len(self.kv) >= self.c:
            k, _ = self.fk[self.m].popitem(last=False)
            del self.kv[k]
            del self.kf[k]
        self.kv[key] = value
        self.kf[key] = 1
        self.fk[1][key] = None
        self.m = 1
    
    def _u(self, key):
        f = self.kf[key]
        del self.fk[f][key]
        if not self.fk[f] and f == self.m:
            self.m += 1
        self.kf[key] = f + 1
        self.fk[f + 1][key] = None