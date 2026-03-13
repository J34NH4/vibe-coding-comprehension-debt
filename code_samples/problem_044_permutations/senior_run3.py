from typing import List


class Solution:
    """Solution for generating all permutations of distinct integers."""
    
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all possible permutations of distinct integers.
        
        Args:
            nums: List of distinct integers to permute
            
        Returns:
            List of all possible permutations as lists
            
        Raises:
            ValueError: If nums is None
        """
        if nums is None:
            raise ValueError("Input cannot be None")
            
        if not nums:
            return [[]]
            
        all_permutations = []
        self._generate_permutations(nums, [], all_permutations)
        return all_permutations
    
    def _generate_permutations(self, remaining_numbers: List[int], 
                             current_permutation: List[int], 
                             all_permutations: List[List[int]]) -> None:
        """
        Recursively generate permutations using backtracking.
        
        Args:
            remaining_numbers: Numbers not yet used in current permutation
            current_permutation: Current permutation being built
            all_permutations: Collection of all completed permutations
        """
        # Base case: no more numbers to add
        if not remaining_numbers:
            all_permutations.append(current_permutation[:])  # Create copy
            return
        
        # Try each remaining number as next element
        for index in range(len(remaining_numbers)):
            chosen_number = remaining_numbers[index]
            
            # Choose: add number to current permutation
            current_permutation.append(chosen_number)
            new_remaining = remaining_numbers[:index] + remaining_numbers[index + 1:]
            
            # Explore: recursively generate with remaining numbers
            self._generate_permutations(new_remaining, current_permutation, all_permutations)
            
            # Unchoose: backtrack by removing the number
            current_permutation.pop()