class AllOne:
    def __init__(self):
        self.c = {}
        self.b = {}
        self.h = self.t = None
        
    def inc(self, k):
        if k not in self.c:
            self.c[k] = 1
            if 1 not in self.b:
                n = {'v': 1, 'ks': {k}, 'p': None, 'n': self.h}
                self.b[1] = n
                if self.h: self.h['p'] = n
                self.h = n
                if not self.t: self.t = n
            else:
                self.b[1]['ks'].add(k)
        else:
            o, n = self.c[k], self.c[k] + 1
            self.c[k] = n
            self.b[o]['ks'].remove(k)
            if not self.b[o]['ks']:
                if self.b[o]['p']: self.b[o]['p']['n'] = self.b[o]['n']
                if self.b[o]['n']: self.b[o]['n']['p'] = self.b[o]['p']
                if self.h == self.b[o]: self.h = self.b[o]['n']
                if self.t == self.b[o]: self.t = self.b[o]['p']
                del self.b[o]
            if n not in self.b:
                nn = {'v': n, 'ks': {k}, 'p': None, 'n': None}
                self.b[n] = nn
                if o in self.b:
                    nn['p'] = self.b[o]['p']
                    nn['n'] = self.b[o]
                    if self.b[o]['p']: self.b[o]['p']['n'] = nn
                    else: self.h = nn
                    self.b[o]['p'] = nn
                else:
                    p = None
                    for x in [self.h] + ([self.h['n']] if self.h and self.h['n'] else []):
                        if not x: break
                        if x['v'] < n:
                            p = x
                            break
                        x = x['n']
                    if p:
                        nn['p'] = p['p']
                        nn['n'] = p
                        if p['p']: p['p']['n'] = nn
                        else: self.h = nn
                        p['p'] = nn
                    else:
                        nn['n'] = self.h
                        if self.h: self.h['p'] = nn
                        self.h = nn
                        if not self.t: self.t = nn
            else:
                self.b[n]['ks'].add(k)
                
    def dec(self, k):
        if k not in self.c: return
        o, n = self.c[k], self.c[k] - 1
        self.b[o]['ks'].remove(k)
        if not self.b[o]['ks']:
            if self.b[o]['p']: self.b[o]['p']['n'] = self.b[o]['n']
            if self.b[o]['n']: self.b[o]['n']['p'] = self.b[o]['p']
            if self.h == self.b[o]: self.h = self.b[o]['n']
            if self.t == self.b[o]: self.t = self.b[o]['p']
            del self.b[o]
        if n == 0:
            del self.c[k]
        else:
            self.c[k] = n
            if n not in self.b:
                nn = {'v': n, 'ks': {k}, 'p': None, 'n': None}
                self.b[n] = nn
                if o in self.b:
                    nn['p'] = self.b[o]['p']
                    nn['n'] = self.b[o]
                    if self.b[o]['p']: self.b[o]['p']['n'] = nn
                    else: self.h = nn
                    self.b[o]['p'] = nn
                else:
                    p = None
                    x = self.h
                    while x:
                        if x['v'] < n:
                            p = x
                            break
                        x = x['n']
                    if p:
                        nn['p'] = p['p']
                        nn['n'] = p
                        if p['p']: p['p']['n'] = nn
                        else: self.h = nn
                        p['p'] = nn
                    else:
                        nn['n'] = self.h
                        if self.h: self.h['p'] = nn
                        self.h = nn
                        if not self.t: self.t = nn
            else:
                self.b[n]['ks'].add(k)
                
    def getMaxKey(self):
        return next(iter(self.t['ks'])) if self.t else ""
        
    def getMinKey(self):
        return next(iter(self.h['ks'])) if self.h else ""