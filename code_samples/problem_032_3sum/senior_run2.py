from typing import List


class Solution:
    """Solution for the 3Sum problem (LeetCode #15)."""
    
    TARGET_SUM = 0
    
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Find all unique triplets in the array that sum to zero.
        
        Args:
            nums: List of integers to search for triplets
            
        Returns:
            List of lists containing all unique triplets that sum to zero
            
        Raises:
            ValueError: If input array is None
        """
        if nums is None:
            raise ValueError("Input array cannot be None")
            
        if len(nums) < 3:
            return []
            
        sorted_nums = sorted(nums)  # Sort to enable two-pointer technique
        result_triplets = []
        
        for first_index in range(len(sorted_nums) - 2):
            # Skip duplicate values for first element
            if first_index > 0 and sorted_nums[first_index] == sorted_nums[first_index - 1]:
                continue
                
            # Early termination if smallest element is positive
            if sorted_nums[first_index] > self.TARGET_SUM:
                break
                
            remaining_triplets = self._find_two_sum_pairs(
                sorted_nums, 
                first_index, 
                self.TARGET_SUM - sorted_nums[first_index]
            )
            
            result_triplets.extend(remaining_triplets)
            
        return result_triplets
    
    def _find_two_sum_pairs(self, sorted_nums: List[int], first_index: int, target_sum: int) -> List[List[int]]:
        """
        Find all pairs in the remaining array that sum to target_sum.
        
        Args:
            sorted_nums: Sorted array of integers
            first_index: Index of the first element (already chosen)
            target_sum: Target sum for the remaining two elements
            
        Returns:
            List of triplets where the first element is sorted_nums[first_index]
        """
        pairs_found = []
        left_pointer = first_index + 1
        right_pointer = len(sorted_nums) - 1
        first_element = sorted_nums[first_index]
        
        while left_pointer < right_pointer:
            current_sum = sorted_nums[left_pointer] + sorted_nums[right_pointer]
            
            if current_sum == target_sum:
                # Found valid triplet
                triplet = [first_element, sorted_nums[left_pointer], sorted_nums[right_pointer]]
                pairs_found.append(triplet)
                
                # Skip duplicate values for second element
                while left_pointer < right_pointer and sorted_nums[left_pointer] == sorted_nums[left_pointer + 1]:
                    left_pointer += 1
                    
                # Skip duplicate values for third element
                while left_pointer < right_pointer and sorted_nums[right_pointer] == sorted_nums[right_pointer - 1]:
                    right_pointer -= 1
                    
                left_pointer += 1
                right_pointer -= 1
                
            elif current_sum < target_sum:
                left_pointer += 1  # Need larger sum
            else:
                right_pointer -= 1  # Need smaller sum
                
        return pairs_found