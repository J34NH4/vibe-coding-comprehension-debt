from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all possible subsets (power set) of the given array.
        
        Args:
            nums: List of unique integers
            
        Returns:
            List of all possible subsets including empty subset
            
        Raises:
            TypeError: If nums is not a list or contains non-integers
        """
        if not isinstance(nums, list):
            raise TypeError("Input must be a list")
        
        if not all(isinstance(num, int) for num in nums):
            raise TypeError("All elements must be integers")
        
        result_subsets = []
        current_subset = []
        
        self._generate_subsets_backtrack(nums, 0, current_subset, result_subsets)
        return result_subsets
    
    def _generate_subsets_backtrack(
        self, 
        nums: List[int], 
        start_index: int, 
        current_subset: List[int], 
        result_subsets: List[List[int]]
    ) -> None:
        """
        Helper method to generate subsets using backtracking approach.
        
        Args:
            nums: Original array of integers
            start_index: Current index to start considering elements from
            current_subset: Current subset being built
            result_subsets: List to store all generated subsets
        """
        # Add current subset to results (includes empty subset on first call)
        result_subsets.append(current_subset[:])  # Create copy to avoid reference issues
        
        # Generate subsets by including each remaining element
        for current_index in range(start_index, len(nums)):
            current_element = nums[current_index]
            
            # Include current element in subset
            current_subset.append(current_element)
            
            # Recursively generate subsets with current element included
            self._generate_subsets_backtrack(nums, current_index + 1, current_subset, result_subsets)
            
            # Backtrack: remove current element to try next possibilities
            current_subset.pop()