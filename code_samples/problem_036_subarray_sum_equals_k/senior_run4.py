from typing import List, Dict

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        Find the total number of continuous subarrays whose sum equals k.
        
        Uses prefix sum with hash map to achieve O(n) time complexity.
        The key insight is that if prefix_sum[j] - prefix_sum[i] = k,
        then subarray from i+1 to j has sum k.
        
        Args:
            nums: List of integers
            k: Target sum value
            
        Returns:
            Total count of subarrays with sum equal to k
        """
        if not nums:
            return 0
            
        return self._count_subarrays_with_prefix_sum(nums, k)
    
    def _count_subarrays_with_prefix_sum(self, nums: List[int], target_sum: int) -> int:
        """
        Count subarrays using prefix sum technique with hash map.
        
        Args:
            nums: Input array of integers
            target_sum: Target sum to find
            
        Returns:
            Count of valid subarrays
        """
        prefix_sum_count: Dict[int, int] = {0: 1}  # Handle case where prefix sum equals target
        current_prefix_sum: int = 0
        subarray_count: int = 0
        
        for current_number in nums:
            current_prefix_sum += current_number
            
            # Check if there exists a previous prefix sum such that
            # current_prefix_sum - previous_prefix_sum = target_sum
            required_prefix_sum: int = current_prefix_sum - target_sum
            
            if required_prefix_sum in prefix_sum_count:
                subarray_count += prefix_sum_count[required_prefix_sum]
            
            # Update count of current prefix sum
            prefix_sum_count[current_prefix_sum] = prefix_sum_count.get(current_prefix_sum, 0) + 1
        
        return subarray_count