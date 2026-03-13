from typing import List, Dict

class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """
        Find the total number of continuous subarrays whose sum equals k.
        
        Uses prefix sum approach with hash map to track cumulative sums.
        For each position, checks if (current_sum - k) exists in previous sums.
        
        Args:
            nums: List of integers representing the input array
            k: Target sum value to find in subarrays
            
        Returns:
            Total count of subarrays with sum equal to k
            
        Time Complexity: O(n) where n is length of nums
        Space Complexity: O(n) for the prefix sum hash map
        """
        if not nums:
            return 0
            
        subarray_count = 0
        current_prefix_sum = 0
        prefix_sum_frequencies = self._initialize_prefix_sum_map()
        
        for current_number in nums:
            current_prefix_sum += current_number
            
            # Check if there's a previous prefix sum that when subtracted gives k
            target_prefix_sum = current_prefix_sum - k
            subarray_count += prefix_sum_frequencies.get(target_prefix_sum, 0)
            
            # Add current prefix sum to frequency map
            self._update_prefix_sum_frequency(prefix_sum_frequencies, current_prefix_sum)
            
        return subarray_count
    
    def _initialize_prefix_sum_map(self) -> Dict[int, int]:
        """
        Initialize the prefix sum frequency map with base case.
        
        The key insight is that prefix_sum[0] = 0 represents the empty prefix,
        which allows us to count subarrays starting from index 0.
        
        Returns:
            Dictionary mapping prefix sums to their frequencies
        """
        return {0: 1}  # Base case: empty prefix has sum 0
    
    def _update_prefix_sum_frequency(self, frequency_map: Dict[int, int], prefix_sum: int) -> None:
        """
        Update the frequency count for a given prefix sum.
        
        Args:
            frequency_map: Dictionary tracking prefix sum frequencies
            prefix_sum: Current cumulative sum to add/update
        """
        frequency_map[prefix_sum] = frequency_map.get(prefix_sum, 0) + 1