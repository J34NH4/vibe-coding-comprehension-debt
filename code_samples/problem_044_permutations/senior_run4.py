from typing import List


class Solution:
    """Solution for generating all possible permutations of distinct integers."""
    
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all possible permutations of the given array of distinct integers.
        
        Args:
            nums: List of distinct integers to permute
            
        Returns:
            List of all possible permutations as lists of integers
            
        Raises:
            TypeError: If nums is not a list or contains non-integer values
        """
        if not isinstance(nums, list):
            raise TypeError("Input must be a list")
        
        if not all(isinstance(num, int) for num in nums):
            raise TypeError("All elements must be integers")
        
        result_permutations: List[List[int]] = []
        
        if not nums:  # Handle empty array edge case
            return [[]]
        
        self._generate_permutations(nums, [], result_permutations)
        return result_permutations
    
    def _generate_permutations(
        self, 
        remaining_nums: List[int], 
        current_permutation: List[int], 
        result_permutations: List[List[int]]
    ) -> None:
        """
        Recursively generate permutations using backtracking approach.
        
        Args:
            remaining_nums: Numbers still available to add to current permutation
            current_permutation: Current permutation being built
            result_permutations: List to store completed permutations
        """
        # Base case: no more numbers to add, permutation is complete
        if not remaining_nums:
            result_permutations.append(current_permutation[:])  # Add copy to avoid reference issues
            return
        
        # Try each remaining number as the next element
        for current_index in range(len(remaining_nums)):
            selected_number: int = remaining_nums[current_index]
            
            # Add selected number to current permutation
            current_permutation.append(selected_number)
            
            # Create new remaining list without the selected number
            new_remaining: List[int] = remaining_nums[:current_index] + remaining_nums[current_index + 1:]
            
            # Recursively generate permutations with updated state
            self._generate_permutations(new_remaining, current_permutation, result_permutations)
            
            # Backtrack: remove the selected number to try next option
            current_permutation.pop()