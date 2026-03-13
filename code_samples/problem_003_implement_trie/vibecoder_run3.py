class Trie:
    def __init__(self):
        self.r = {}
    
    def insert(self, w):
        n = self.r
        for c in w:
            if c not in n: n[c] = {}
            n = n[c]
        n['#'] = True
    
    def search(self, w):
        n = self.r
        for c in w:
            if c not in n: return False
            n = n[c]
        return '#' in n
    
    def startsWith(self, p):
        n = self.r
        for c in p:
            if c not in n: return False
            n = n[c]
        return True