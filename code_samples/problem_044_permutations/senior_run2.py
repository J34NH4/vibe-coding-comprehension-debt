from typing import List

class Solution:
    """Solution for generating all permutations of distinct integers."""
    
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all possible permutations of the given array.
        
        Args:
            nums: List of distinct integers
            
        Returns:
            List of all possible permutations
            
        Raises:
            ValueError: If input is None
        """
        if nums is None:
            raise ValueError("Input cannot be None")
            
        result_permutations = []
        self._generate_permutations(nums, [], result_permutations)
        return result_permutations
    
    def _generate_permutations(self, remaining_nums: List[int], 
                             current_permutation: List[int], 
                             result_permutations: List[List[int]]) -> None:
        """
        Recursively generate permutations using backtracking.
        
        Args:
            remaining_nums: Numbers not yet used in current permutation
            current_permutation: Current permutation being built
            result_permutations: List to store all valid permutations
        """
        # Base case: no more numbers to add
        if not remaining_nums:
            result_permutations.append(current_permutation.copy())  # Add copy to avoid reference issues
            return
        
        # Try each remaining number as next element
        for index in range(len(remaining_nums)):
            chosen_number = remaining_nums[index]
            
            # Choose: add number to current permutation
            current_permutation.append(chosen_number)
            
            # Explore: recurse with remaining numbers
            new_remaining = remaining_nums[:index] + remaining_nums[index + 1:]
            self._generate_permutations(new_remaining, current_permutation, result_permutations)
            
            # Unchoose: backtrack by removing the number
            current_permutation.pop()