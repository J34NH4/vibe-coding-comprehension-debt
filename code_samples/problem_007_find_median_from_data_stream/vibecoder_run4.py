import heapq

class MedianFinder:
    def __init__(self):
        self.l = []
        self.r = []

    def addNum(self, n):
        heapq.heappush(self.l, -n)
        heapq.heappush(self.r, -heapq.heappop(self.l))
        if len(self.r) > len(self.l):
            heapq.heappush(self.l, -heapq.heappop(self.r))

    def findMedian(self):
        return -self.l[0] if len(self.l) > len(self.r) else (-self.l[0] + self.r[0]) / 2