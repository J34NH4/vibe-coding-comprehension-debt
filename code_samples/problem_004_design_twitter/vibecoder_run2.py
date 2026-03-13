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
        return [tw for t, tw in heapq.nsmallest(10, h)]
    
    def follow(self, f, fw):
        if f != fw:
            self.f[f].add(fw)
    
    def unfollow(self, f, fw):
        self.f[f].discard(fw)