from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs):
        d = defaultdict(list)
        for s in strs:
            d[''.join(sorted(s))].append(s)
        return list(d.values())