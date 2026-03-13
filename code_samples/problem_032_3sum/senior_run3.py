from typing import List, Set, Tuple

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """
        Find all unique triplets in the array that sum to zero.
        
        Args:
            nums: List of integers to search for triplets
            
        Returns:
            List of lists containing all unique triplets that sum to zero
        """
        if not nums or len(nums) < 3:
            return []
        
        sorted_nums = sorted(nums)  # Sort to enable two-pointer approach
        result_triplets = []
        array_length = len(sorted_nums)
        
        for first_index in range(array_length - 2):
            # Skip duplicate values for first element
            if first_index > 0 and sorted_nums[first_index] == sorted_nums[first_index - 1]:
                continue
            
            # Early termination if smallest element is positive
            if sorted_nums[first_index] > 0:
                break
            
            target_sum = -sorted_nums[first_index]  # Target for remaining two elements
            left_pointer = first_index + 1
            right_pointer = array_length - 1
            
            while left_pointer < right_pointer:
                current_sum = sorted_nums[left_pointer] + sorted_nums[right_pointer]
                
                if current_sum == target_sum:
                    # Found valid triplet
                    result_triplets.append([
                        sorted_nums[first_index],
                        sorted_nums[left_pointer],
                        sorted_nums[right_pointer]
                    ])
                    
                    # Skip duplicates for second element
                    while left_pointer < right_pointer and sorted_nums[left_pointer] == sorted_nums[left_pointer + 1]:
                        left_pointer += 1
                    
                    # Skip duplicates for third element
                    while left_pointer < right_pointer and sorted_nums[right_pointer] == sorted_nums[right_pointer - 1]:
                        right_pointer -= 1
                    
                    left_pointer += 1
                    right_pointer -= 1
                    
                elif current_sum < target_sum:
                    left_pointer += 1  # Need larger sum
                else:
                    right_pointer -= 1  # Need smaller sum
        
        return result_triplets