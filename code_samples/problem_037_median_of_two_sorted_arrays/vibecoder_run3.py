class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        m, n = len(nums1), len(nums2)
        l, r = 0, m
        while l <= r:
            i = (l + r) // 2
            j = (m + n + 1) // 2 - i
            ml = float('-inf') if i == 0 else nums1[i-1]
            mr = float('inf') if i == m else nums1[i]
            nl = float('-inf') if j == 0 else nums2[j-1]
            nr = float('inf') if j == n else nums2[j]
            if ml <= nr and nl <= mr:
                return max(ml, nl) if (m + n) % 2 else (max(ml, nl) + min(mr, nr)) / 2
            elif ml > nr:
                r = i - 1
            else:
                l = i + 1