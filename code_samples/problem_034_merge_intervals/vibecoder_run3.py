class Solution:
    def merge(self, intervals):
        intervals.sort()
        r = [intervals[0]]
        for i in intervals[1:]:
            if i[0] <= r[-1][1]:
                r[-1][1] = max(r[-1][1], i[1])
            else:
                r.append(i)
        return r