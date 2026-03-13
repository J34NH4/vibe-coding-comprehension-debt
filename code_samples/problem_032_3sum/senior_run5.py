from typing import List, Set, Tuple


class Solution:
    """Solution for the 3Sum problem using two-pointer approach."""
    
    TARGET_SUM: int = 0
    
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
            
        sorted_nums = sorted(nums)
        result_triplets = []
        array_length = len(sorted_nums)
        
        for first_index in range(array_length - 2):
            # Skip duplicate values for first element
            if first_index > 0 and sorted_nums[first_index] == sorted_nums[first_index - 1]:
                continue
                
            current_first_value = sorted_nums[first_index]
            
            # Early termination if smallest value is positive
            if current_first_value > self.TARGET_SUM:
                break
                
            found_triplets = self._find_two_sum_pairs(
                sorted_nums, first_index + 1, array_length - 1, -current_first_value
            )
            
            # Add first element to each valid pair
            for second_value, third_value in found_triplets:
                result_triplets.append([current_first_value, second_value, third_value])
                
        return result_triplets
    
    def _find_two_sum_pairs(
        self, 
        sorted_array: List[int], 
        left_pointer: int, 
        right_pointer: int, 
        target_sum: int
    ) -> List[Tuple[int, int]]:
        """
        Find all unique pairs in sorted array that sum to target using two pointers.
        
        Args:
            sorted_array: Sorted array to search in
            left_pointer: Starting left pointer index
            right_pointer: Starting right pointer index
            target_sum: Target sum for the two elements
            
        Returns:
            List of tuples containing pairs that sum to target
        """
        valid_pairs = []
        
        while left_pointer < right_pointer:
            left_value = sorted_array[left_pointer]
            right_value = sorted_array[right_pointer]
            current_sum = left_value + right_value
            
            if current_sum == target_sum:
                valid_pairs.append((left_value, right_value))
                
                # Skip duplicate values on both sides
                while left_pointer < right_pointer and sorted_array[left_pointer] == left_value:
                    left_pointer += 1
                while left_pointer < right_pointer and sorted_array[right_pointer] == right_value:
                    right_pointer -= 1
                    
            elif current_sum < target_sum:
                left_pointer += 1  # Need larger sum
            else:
                right_pointer -= 1  # Need smaller sum
                
        return valid_pairs