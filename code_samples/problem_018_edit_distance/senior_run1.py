from typing import List

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        """
        Calculate the minimum edit distance between two strings using dynamic programming.
        
        Args:
            word1: The source string to transform
            word2: The target string to transform into
            
        Returns:
            The minimum number of operations (insert, delete, replace) needed
            
        Raises:
            TypeError: If inputs are not strings
        """
        if not isinstance(word1, str) or not isinstance(word2, str):
            raise TypeError("Both inputs must be strings")
            
        return self._calculate_edit_distance_with_dp(word1, word2)
    
    def _calculate_edit_distance_with_dp(self, source_word: str, target_word: str) -> int:
        """
        Internal method to calculate edit distance using 2D dynamic programming.
        
        Args:
            source_word: The word to transform from
            target_word: The word to transform to
            
        Returns:
            Minimum edit distance as integer
        """
        source_length = len(source_word)
        target_length = len(target_word)
        
        # Handle edge cases
        if source_length == 0:
            return target_length  # Insert all characters from target
        if target_length == 0:
            return source_length  # Delete all characters from source
        
        # Initialize DP table with base cases
        edit_distance_table = self._initialize_dp_table(source_length, target_length)
        
        # Fill the DP table
        for source_index in range(1, source_length + 1):
            for target_index in range(1, target_length + 1):
                edit_distance_table[source_index][target_index] = self._calculate_minimum_operations(
                    edit_distance_table, 
                    source_word, 
                    target_word, 
                    source_index, 
                    target_index
                )
        
        return edit_distance_table[source_length][target_length]
    
    def _initialize_dp_table(self, source_length: int, target_length: int) -> List[List[int]]:
        """
        Initialize the DP table with base cases.
        
        Args:
            source_length: Length of source string
            target_length: Length of target string
            
        Returns:
            2D list initialized with base cases
        """
        edit_distance_table = [[0] * (target_length + 1) for _ in range(source_length + 1)]
        
        # Base case: transforming empty string to target requires insertions
        for target_index in range(target_length + 1):
            edit_distance_table[0][target_index] = target_index
        
        # Base case: transforming source to empty string requires deletions
        for source_index in range(source_length + 1):
            edit_distance_table[source_index][0] = source_index
        
        return edit_distance_table
    
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
            source_index: Current index in source (1-based for DP table)
            target_index: Current index in target (1-based for DP table)
            
        Returns:
            Minimum number of operations for this position
        """
        # Characters match - no operation needed
        if source_word[source_index - 1] == target_word[target_index - 1]:
            return dp_table[source_index - 1][target_index - 1]
        
        # Characters don't match - consider all three operations
        replace_cost = dp_table[source_index - 1][target_index - 1] + 1  # Replace operation
        insert_cost = dp_table[source_index][target_index - 1] + 1       # Insert operation
        delete_cost = dp_table[source_index - 1][target_index] + 1       # Delete operation
        
        return min(replace_cost, insert_cost, delete_cost)