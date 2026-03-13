from collections import defaultdict

class AllOne:
    def __init__(self):
        self.c = defaultdict(int)
        self.s = defaultdict(set)
        self.mn = 0
        self.mx = 0

    def inc(self, k):
        if k in self.c:
            self.s[self.c[k]].remove(k)
            if not self.s[self.c[k]] and self.c[k] == self.mn:
                self.mn += 1
        self.c[k] += 1
        self.s[self.c[k]].add(k)
        if self.c[k] == 1:
            self.mn = 1
        if self.c[k] > self.mx:
            self.mx = self.c[k]

    def dec(self, k):
        if k not in self.c:
            return
        self.s[self.c[k]].remove(k)
        if not self.s[self.c[k]] and self.c[k] == self.mx:
            self.mx -= 1
        if self.c[k] == 1:
            del self.c[k]
            if not self.c:
                self.mn = self.mx = 0
            elif self.mn == 1:
                self.mn = min(self.c.values())
        else:
            self.c[k] -= 1
            self.s[self.c[k]].add(k)
            if self.c[k] < self.mn:
                self.mn = self.c[k]

    def getMaxKey(self):
        return next(iter(self.s[self.mx])) if self.mx else ""

    def getMinKey(self):
        return next(iter(self.s[self.mn])) if self.mn else ""