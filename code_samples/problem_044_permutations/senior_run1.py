from typing import List


class Solution:
    """Solution for generating all possible permutations of distinct integers."""
    
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Generate all possible permutations of the given array of distinct integers.
        
        Args:
            nums: List of distinct integers to permute
            
        Returns:
            List of all possible permutations as lists
            
        Raises:
            TypeError: If nums is not a list or contains non-integers
        """
        if not isinstance(nums, list):
            raise TypeError("Input must be a list")
        
        if not nums:  # Handle empty list edge case
            return [[]]
        
        all_permutations = []
        self._generate_permutations(nums, [], all_permutations)
        return all_permutations
    
    def _generate_permutations(self, remaining_numbers: List[int], 
                             current_permutation: List[int], 
                             all_permutations: List[List[int]]) -> None:
        """
        Recursively generate permutations using backtracking approach.
        
        Args:
            remaining_numbers: Numbers not yet used in current permutation
            current_permutation: Current partial permutation being built
            all_permutations: Collection of all complete permutations found
        """
        # Base case: no more numbers to choose from
        if not remaining_numbers:
            all_permutations.append(current_permutation.copy())  # Create copy to avoid reference issues
            return
        
        # Try each remaining number as the next element
        for index in range(len(remaining_numbers)):
            chosen_number = remaining_numbers[index]
            
            # Add chosen number to current permutation
            current_permutation.append(chosen_number)
            
            # Create new remaining list without the chosen number
            new_remaining = remaining_numbers[:index] + remaining_numbers[index + 1:]
            
            # Recursively generate permutations with updated state
            self._generate_permutations(new_remaining, current_permutation, all_permutations)
            
            # Backtrack: remove the chosen number for next iteration
            current_permutation.pop()