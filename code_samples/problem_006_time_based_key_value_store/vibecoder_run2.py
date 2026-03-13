class TimeMap:
    def __init__(self):
        self.d = {}
    
    def set(self, k, v, t):
        if k not in self.d: self.d[k] = []
        self.d[k].append((t, v))
    
    def get(self, k, t):
        if k not in self.d: return ""
        a = self.d[k]
        l, r = 0, len(a) - 1
        res = ""
        while l <= r:
            m = (l + r) // 2
            if a[m][0] <= t:
                res = a[m][1]
                l = m + 1
            else:
                r = m - 1
        return res