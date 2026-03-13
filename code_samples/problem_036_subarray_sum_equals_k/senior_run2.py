from typing import List, Dict

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        Find the total number of continuous subarrays whose sum equals k.
        
        Uses prefix sum technique with hashmap to track cumulative sums.
        For each position, checks if (current_sum - k) exists in previous sums.
        
        Args:
            nums: List of integers representing the input array
            k: Target sum value for subarrays
            
        Returns:
            Integer count of subarrays with sum equal to k
            
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        if not nums:
            return 0
            
        subarray_count = 0
        cumulative_sum = 0
        
        # HashMap to store frequency of each prefix sum
        prefix_sum_frequency: Dict[int, int] = {0: 1}  # Initialize with sum 0
        
        for current_number in nums:
            cumulative_sum += current_number
            
            # Check if (cumulative_sum - k) exists in previous sums
            target_prefix_sum = cumulative_sum - k
            if target_prefix_sum in prefix_sum_frequency:
                subarray_count += prefix_sum_frequency[target_prefix_sum]
            
            # Update frequency of current cumulative sum
            prefix_sum_frequency[cumulative_sum] = prefix_sum_frequency.get(cumulative_sum, 0) + 1
            
        return subarray_count