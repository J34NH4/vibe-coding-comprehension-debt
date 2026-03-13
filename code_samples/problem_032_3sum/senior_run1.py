from typing import List, Set, Tuple


class Solution:
    """Solution for the 3Sum problem using two-pointer technique."""
    
    TARGET_SUM = 0
    
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Find all unique triplets in the array that sum to zero.
        
        Args:
            nums: List of integers to search for triplets
            
        Returns:
            List of lists containing unique triplets that sum to zero
            
        Raises:
            ValueError: If input array is None
        """
        if nums is None:
            raise ValueError("Input array cannot be None")
            
        if len(nums) < 3:
            return []
            
        sorted_nums = sorted(nums)
        result_triplets = []
        
        for first_index in range(len(sorted_nums) - 2):
            # Skip duplicate values for first element
            if first_index > 0 and sorted_nums[first_index] == sorted_nums[first_index - 1]:
                continue
                
            current_triplets = self._find_triplets_with_first_element(
                sorted_nums, first_index
            )
            result_triplets.extend(current_triplets)
            
        return result_triplets
    
    def _find_triplets_with_first_element(
        self, sorted_nums: List[int], first_index: int
    ) -> List[List[int]]:
        """
        Find all triplets starting with the element at first_index.
        
        Args:
            sorted_nums: Sorted array of integers
            first_index: Index of the first element in triplet
            
        Returns:
            List of triplets starting with the first element
        """
        triplets = []
        first_element = sorted_nums[first_index]
        target_two_sum = self.TARGET_SUM - first_element
        
        left_pointer = first_index + 1
        right_pointer = len(sorted_nums) - 1
        
        while left_pointer < right_pointer:
            left_element = sorted_nums[left_pointer]
            right_element = sorted_nums[right_pointer]
            current_two_sum = left_element + right_element
            
            if current_two_sum == target_two_sum:
                triplets.append([first_element, left_element, right_element])
                
                # Skip duplicates for left pointer
                while (left_pointer < right_pointer and 
                       sorted_nums[left_pointer] == sorted_nums[left_pointer + 1]):
                    left_pointer += 1
                    
                # Skip duplicates for right pointer
                while (left_pointer < right_pointer and 
                       sorted_nums[right_pointer] == sorted_nums[right_pointer - 1]):
                    right_pointer -= 1
                    
                left_pointer += 1
                right_pointer -= 1
                
            elif current_two_sum < target_two_sum:
                left_pointer += 1  # Need larger sum
            else:
                right_pointer -= 1  # Need smaller sum
                
        return triplets