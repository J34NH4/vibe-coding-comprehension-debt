from typing import List, Dict


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        Find the total number of continuous subarrays whose sum equals k.
        
        Uses prefix sum technique with hashmap to achieve O(n) time complexity.
        For each position, checks if (current_sum - k) exists in previous sums.
        
        Args:
            nums: List of integers representing the input array
            k: Target sum value for subarrays
            
        Returns:
            Total count of subarrays with sum equal to k
            
        Raises:
            None - handles empty arrays gracefully
        """
        if not nums:
            return 0
            
        return self._count_subarrays_with_target_sum(nums, k)
    
    def _count_subarrays_with_target_sum(self, numbers: List[int], target_sum: int) -> int:
        """
        Helper method to count subarrays using prefix sum approach.
        
        Args:
            numbers: Input array of integers
            target_sum: Target sum to find
            
        Returns:
            Count of valid subarrays
        """
        subarray_count = 0
        current_prefix_sum = 0
        
        # Map to store frequency of each prefix sum encountered
        prefix_sum_frequency: Dict[int, int] = {0: 1}  # Initialize with sum 0 occurring once
        
        for current_number in numbers:
            current_prefix_sum += current_number
            
            # Check if (current_sum - target) exists in previous sums
            required_prefix_sum = current_prefix_sum - target_sum
            
            if required_prefix_sum in prefix_sum_frequency:
                subarray_count += prefix_sum_frequency[required_prefix_sum]
            
            # Update frequency map with current prefix sum
            prefix_sum_frequency[current_prefix_sum] = prefix_sum_frequency.get(current_prefix_sum, 0) + 1
            
        return subarray_count