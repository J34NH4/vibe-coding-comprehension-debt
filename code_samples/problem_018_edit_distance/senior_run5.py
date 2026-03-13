from typing import List

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        """
        Calculate the minimum edit distance between two strings using dynamic programming.
        
        Uses the Wagner-Fischer algorithm to compute the minimum number of single-character
        edits (insertions, deletions, or substitutions) required to change one word into another.
        
        Args:
            word1: The source string to transform
            word2: The target string to match
            
        Returns:
            The minimum number of operations needed to transform word1 into word2
            
        Raises:
            None - handles all valid string inputs including empty strings
        """
        return self._calculate_edit_distance_dp(word1, word2)
    
    def _calculate_edit_distance_dp(self, source_word: str, target_word: str) -> int:
        """
        Internal method to calculate edit distance using dynamic programming table.
        
        Args:
            source_word: The string to transform from
            target_word: The string to transform to
            
        Returns:
            Minimum edit distance as integer
        """
        source_length = len(source_word)
        target_length = len(target_word)
        
        # Handle edge cases where one string is empty
        if source_length == 0:
            return target_length
        if target_length == 0:
            return source_length
        
        # Initialize DP table with dimensions (source_length + 1) x (target_length + 1)
        dp_table = self._initialize_dp_table(source_length, target_length)
        
        # Fill the DP table using optimal substructure
        for source_index in range(1, source_length + 1):
            for target_index in range(1, target_length + 1):
                dp_table[source_index][target_index] = self._calculate_minimum_operations(
                    dp_table, source_word, target_word, source_index, target_index
                )
        
        return dp_table[source_length][target_length]
    
    def _initialize_dp_table(self, source_length: int, target_length: int) -> List[List[int]]:
        """
        Initialize the dynamic programming table with base cases.
        
        Args:
            source_length: Length of source string
            target_length: Length of target string
            
        Returns:
            2D list initialized with base case values
        """
        dp_table = [[0] * (target_length + 1) for _ in range(source_length + 1)]
        
        # Base case: transforming empty string to target requires target_length insertions
        for target_index in range(target_length + 1):
            dp_table[0][target_index] = target_index
        
        # Base case: transforming source to empty string requires source_length deletions
        for source_index in range(source_length + 1):
            dp_table[source_index][0] = source_index
        
        return dp_table
    
    def _calculate_minimum_operations(
        self, 
        dp_table: List[List[int]], 
        source_word: str, 
        target_word: str, 
        source_index: int, 
        target_index: int
    ) -> int:
        """
        Calculate minimum operations for current position in DP table.
        
        Args:
            dp_table: The dynamic programming table
            source_word: Source string
            target_word: Target string
            source_index: Current index in source string (1-based for DP table)
            target_index: Current index in target string (1-based for DP table)
            
        Returns:
            Minimum operations needed for this subproblem
        """
        # Check if characters match (convert to 0-based indexing for string access)
        characters_match = source_word[source_index - 1] == target_word[target_index - 1]
        
        if characters_match:
            # No operation needed, take diagonal value
            return dp_table[source_index - 1][target_index - 1]
        else:
            # Characters don't match, consider all three operations
            substitution_cost = dp_table[source_index - 1][target_index - 1] + 1  # Replace
            insertion_cost = dp_table[source_index][target_index - 1] + 1         # Insert
            deletion_cost = dp_table[source_index - 1][target_index] + 1          # Delete
            
            return min(substitution_cost, insertion_cost, deletion_cost)