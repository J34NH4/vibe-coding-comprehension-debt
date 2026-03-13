import heapq

class MedianFinder:
    def __init__(self):
        self.l = []
        self.r = []

    def addNum(self, n):
        if not self.l or n <= -self.l[0]:
            heapq.heappush(self.l, -n)
        else:
            heapq.heappush(self.r, n)
        
        if len(self.l) > len(self.r) + 1:
            heapq.heappush(self.r, -heapq.heappop(self.l))
        elif len(self.r) > len(self.l) + 1:
            heapq.heappush(self.l, -heapq.heappop(self.r))

    def findMedian(self):
        if len(self.l) > len(self.r):
            return -self.l[0]
        elif len(self.r) > len(self.l):
            return self.r[0]
        return (-self.l[0] + self.r[0]) / 2