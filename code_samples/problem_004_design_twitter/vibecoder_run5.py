from collections import defaultdict, deque
import heapq

class Twitter:
    def __init__(self):
        self.t = 0
        self.tw = defaultdict(deque)
        self.fl = defaultdict(set)

    def postTweet(self, u, tw):
        self.tw[u].appendleft((self.t, tw))
        if len(self.tw[u]) > 10: self.tw[u].pop()
        self.t -= 1

    def getNewsFeed(self, u):
        h = []
        for t, tw in self.tw[u]: heapq.heappush(h, (t, tw))
        for f in self.fl[u]:
            for t, tw in self.tw[f]: heapq.heappush(h, (t, tw))
        return [heapq.heappop(h)[1] for _ in range(min(10, len(h)))]

    def follow(self, f, t):
        if f != t: self.fl[f].add(t)

    def unfollow(self, f, t):
        self.fl[f].discard(t)