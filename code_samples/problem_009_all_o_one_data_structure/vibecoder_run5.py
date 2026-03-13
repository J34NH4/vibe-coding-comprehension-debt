class AllOne:
    def __init__(self):
        self.d = {}
        self.h = {}
        self.m = 0
        self.x = 0

    def inc(self, k):
        if k in self.d:
            o = self.d[k]
            self.d[k] += 1
            n = self.d[k]
            self.h[o].remove(k)
            if not self.h[o] and o == self.m:
                self.m = min([c for c in self.h if self.h[c]]) if any(self.h[c] for c in self.h) else 0
            if n not in self.h:
                self.h[n] = set()
            self.h[n].add(k)
            self.x = max(self.x, n)
        else:
            self.d[k] = 1
            if 1 not in self.h:
                self.h[1] = set()
            self.h[1].add(k)
            self.m = 1 if self.m == 0 else min(self.m, 1)
            self.x = max(self.x, 1)

    def dec(self, k):
        if k not in self.d:
            return
        o = self.d[k]
        self.h[o].remove(k)
        if not self.h[o] and o == self.x:
            self.x = max([c for c in self.h if self.h[c]]) if any(self.h[c] for c in self.h) else 0
        if o == 1:
            del self.d[k]
        else:
            self.d[k] -= 1
            n = self.d[k]
            if n not in self.h:
                self.h[n] = set()
            self.h[n].add(k)
        if not any(self.h[c] for c in self.h):
            self.m = self.x = 0
        elif not self.h.get(self.m, set()):
            self.m = min([c for c in self.h if self.h[c]])

    def getMaxKey(self):
        return next(iter(self.h[self.x])) if self.x and self.h.get(self.x) else ""

    def getMinKey(self):
        return next(iter(self.h[self.m])) if self.m and self.h.get(self.m) else ""