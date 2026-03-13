class AllOne:
    def __init__(self):
        self.c = {}
        self.h = {}
        self.t = {}
        self.mx = 0
        self.mn = float('inf')
    
    def inc(self, k):
        if k in self.c:
            o = self.c[k]
            self.h[o].discard(k)
            if not self.h[o] and o == self.mn:
                self.mn = min(self.h.keys()) if any(self.h.values()) else float('inf')
            self.c[k] += 1
        else:
            self.c[k] = 1
        n = self.c[k]
        if n not in self.h:
            self.h[n] = set()
        self.h[n].add(k)
        self.mx = max(self.mx, n)
        self.mn = min(self.mn, n) if self.mn != float('inf') else n
    
    def dec(self, k):
        if k not in self.c:
            return
        o = self.c[k]
        self.h[o].discard(k)
        if not self.h[o]:
            if o == self.mx:
                self.mx = max([x for x in self.h.keys() if self.h[x]]) if any(self.h.values()) else 0
            if o == self.mn:
                self.mn = min([x for x in self.h.keys() if self.h[x]]) if any(self.h.values()) else float('inf')
        if self.c[k] == 1:
            del self.c[k]
        else:
            self.c[k] -= 1
            n = self.c[k]
            if n not in self.h:
                self.h[n] = set()
            self.h[n].add(k)
            self.mn = min(self.mn, n)
    
    def getMaxKey(self):
        return next(iter(self.h[self.mx])) if self.mx > 0 and self.h[self.mx] else ""
    
    def getMinKey(self):
        return next(iter(self.h[self.mn])) if self.mn != float('inf') and self.h[self.mn] else ""