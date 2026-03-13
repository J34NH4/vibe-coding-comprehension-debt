from typing import List, Dict

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        Find the total number of continuous subarrays whose sum equals k.
        
        Uses prefix sum with hash map to achieve O(n) time complexity.
        For each position, checks if (current_prefix_sum - k) exists in previous sums.
        
        Args:
            nums: List of integers representing the input array
            k: Target sum value for subarrays
            
        Returns:
            Integer count of subarrays with sum equal to k
            
        Raises:
            None - handles all valid inputs including empty arrays
        """
        if not nums:  # Handle edge case of empty array
            return 0
            
        total_count = 0
        current_prefix_sum = 0
        prefix_sum_frequencies: Dict[int, int] = {0: 1}  # Initialize with sum 0 occurring once
        
        for current_number in nums:
            current_prefix_sum += current_number
            
            # Check if there's a previous prefix sum that creates target subarray
            target_previous_sum = current_prefix_sum - k
            if target_previous_sum in prefix_sum_frequencies:
                total_count += prefix_sum_frequencies[target_previous_sum]
            
            # Update frequency map with current prefix sum
            prefix_sum_frequencies[current_prefix_sum] = prefix_sum_frequencies.get(current_prefix_sum, 0) + 1
        
        return total_count