from collections import defaultdict, deque
import heapq

class Twitter:
    def __init__(self):
        self.t = 0
        self.tw = defaultdict(deque)
        self.f = defaultdict(set)
    
    def postTweet(self, u, tw):
        self.tw[u].appendleft((self.t, tw))
        if len(self.tw[u]) > 10:
            self.tw[u].pop()
        self.t -= 1
    
    def getNewsFeed(self, u):
        h = []
        for t, tw in self.tw[u]:
            heapq.heappush(h, (t, tw))
        for fu in self.f[u]:
            for t, tw in self.tw[fu]:
                heapq.heappush(h, (t, tw))
        return [heapq.heappop(h)[1] for _ in range(min(10, len(h)))]
    
    def follow(self, fr, to):
        if fr != to:
            self.f[fr].add(to)
    
    def unfollow(self, fr, to):
        self.f[fr].discard(to)