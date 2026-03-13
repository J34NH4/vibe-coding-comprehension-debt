from collections import defaultdict, deque

class Twitter:
    def __init__(self):
        self.t = 0
        self.tw = defaultdict(deque)
        self.f = defaultdict(set)

    def postTweet(self, u, tw):
        self.tw[u].appendleft((self.t, tw))
        if len(self.tw[u]) > 10:
            self.tw[u].pop()
        self.t += 1

    def getNewsFeed(self, u):
        h = []
        for t, tw in self.tw[u]:
            h.append((-t, tw))
        for fu in self.f[u]:
            for t, tw in self.tw[fu]:
                h.append((-t, tw))
        h.sort()
        return [tw for _, tw in h[:10]]

    def follow(self, f, fe):
        if f != fe:
            self.f[f].add(fe)

    def unfollow(self, f, fe):
        self.f[f].discard(fe)