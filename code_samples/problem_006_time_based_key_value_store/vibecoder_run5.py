from collections import defaultdict
import bisect

class TimeMap:
    def __init__(self):
        self.d = defaultdict(list)
    
    def set(self, k, v, t):
        self.d[k].append((t, v))
    
    def get(self, k, t):
        if k not in self.d: return ""
        a = self.d[k]
        i = bisect.bisect_right(a, (t, chr(127)))
        return a[i-1][1] if i > 0 else ""