class Twitter:
    def __init__(self):
        self.t = 0
        self.tw = {}
        self.fo = {}
    
    def postTweet(self, u, tw):
        if u not in self.tw: self.tw[u] = []
        self.tw[u].append((self.t, tw))
        self.t += 1
    
    def getNewsFeed(self, u):
        import heapq
        h = []
        if u in self.tw:
            for t, tw in self.tw[u]: heapq.heappush(h, (-t, tw))
        if u in self.fo:
            for f in self.fo[u]:
                if f in self.tw:
                    for t, tw in self.tw[f]: heapq.heappush(h, (-t, tw))
        r = []
        for _ in range(min(10, len(h))): r.append(heapq.heappop(h)[1])
        return r
    
    def follow(self, fo, fe):
        if fo not in self.fo: self.fo[fo] = set()
        self.fo[fo].add(fe)
    
    def unfollow(self, fo, fe):
        if fo in self.fo: self.fo[fo].discard(fe)