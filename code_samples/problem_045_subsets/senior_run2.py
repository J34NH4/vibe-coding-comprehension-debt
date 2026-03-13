from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all possible subsets (power set) of the given array.
        
        Args:
            nums: List of unique integers
            
        Returns:
            List of all possible subsets
            
        Raises:
            TypeError: If nums is not a list
        """
        if not isinstance(nums, list):
            raise TypeError("Input must be a list")
        
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
        Generate subsets using backtracking approach.
        
        Args:
            nums: Original array of numbers
            start_index: Current index to consider in nums
            current_subset: Current subset being built
            result_subsets: Collection of all generated subsets
        """
        # Add current subset to results (base case)
        result_subsets.append(current_subset[:])  # Create copy to avoid reference issues
        
        # Generate subsets by including each remaining element
        for current_index in range(start_index, len(nums)):
            current_element = nums[current_index]
            
            # Include current element in subset
            current_subset.append(current_element)
            
            # Recursively generate subsets with current element included
            self._generate_subsets_backtrack(nums, current_index + 1, current_subset, result_subsets)
            
            # Backtrack: remove current element to try next possibility
            current_subset.pop()