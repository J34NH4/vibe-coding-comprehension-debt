class Solution:
    def groupAnagrams(self, strs):
        d = {}
        for s in strs:
            k = ''.join(sorted(s))
            d[k] = d.get(k, []) + [s]
        return list(d.values())