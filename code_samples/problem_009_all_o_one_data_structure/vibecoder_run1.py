class AllOne:
    def __init__(self):
        self.d = {}
        self.c = {}
        self.mx = 0
        self.mn = float('inf')

    def inc(self, key):
        if key in self.d:
            old = self.d[key]
            self.c[old].discard(key)
            if not self.c[old] and old == self.mn:
                self.mn = min([k for k in self.c if self.c[k]] or [float('inf')])
            self.d[key] += 1
        else:
            self.d[key] = 1
            self.mn = 1
        new = self.d[key]
        if new not in self.c:
            self.c[new] = set()
        self.c[new].add(key)
        self.mx = max(self.mx, new)

    def dec(self, key):
        if key not in self.d:
            return
        old = self.d[key]
        self.c[old].discard(key)
        if not self.c[old]:
            if old == self.mx:
                self.mx = max([k for k in self.c if self.c[k]] or [0])
            if old == self.mn:
                self.mn = min([k for k in self.c if self.c[k]] or [float('inf')])
        if old == 1:
            del self.d[key]
        else:
            self.d[key] -= 1
            new = self.d[key]
            if new not in self.c:
                self.c[new] = set()
            self.c[new].add(key)
            self.mn = min(self.mn, new)

    def getMaxKey(self):
        return next(iter(self.c[self.mx])) if self.mx > 0 and self.c[self.mx] else ""

    def getMinKey(self):
        return next(iter(self.c[self.mn])) if self.mn < float('inf') and self.c[self.mn] else ""