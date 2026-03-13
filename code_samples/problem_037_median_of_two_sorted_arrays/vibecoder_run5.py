class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        l, r = 0, m
        while l <= r:
            p1 = (l + r) // 2
            p2 = (m + n + 1) // 2 - p1
            ml1 = float('-inf') if p1 == 0 else nums1[p1 - 1]
            ml2 = float('-inf') if p2 == 0 else nums2[p2 - 1]
            mr1 = float('inf') if p1 == m else nums1[p1]
            mr2 = float('inf') if p2 == n else nums2[p2]
            if ml1 <= mr2 and ml2 <= mr1:
                return max(ml1, ml2) if (m + n) % 2 else (max(ml1, ml2) + min(mr1, mr2)) / 2
            elif ml1 > mr2:
                r = p1 - 1
            else:
                l = p1 + 1