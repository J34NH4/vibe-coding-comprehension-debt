from typing import List

class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        """
        Calculate the minimum edit distance between two strings using dynamic programming.
        
        Args:
            word1: The source string to transform
            word2: The target string to transform to
            
        Returns:
            The minimum number of operations (insert, delete, replace) needed
            
        Raises:
            TypeError: If inputs are not strings
        """
        if not isinstance(word1, str) or not isinstance(word2, str):
            raise TypeError("Both inputs must be strings")
            
        return self._calculate_edit_distance(word1, word2)
    
    def _calculate_edit_distance(self, source_word: str, target_word: str) -> int:
        """
        Internal method to calculate edit distance using dynamic programming.
        
        Args:
            source_word: The source string
            target_word: The target string
            
        Returns:
            The minimum edit distance
        """
        source_length = len(source_word)
        target_length = len(target_word)
        
        # Handle edge cases
        if source_length == 0:
            return target_length
        if target_length == 0:
            return source_length
        
        # Initialize DP table
        distance_matrix = self._initialize_dp_table(source_length, target_length)
        
        # Fill DP table
        for source_index in range(1, source_length + 1):
            for target_index in range(1, target_length + 1):
                distance_matrix[source_index][target_index] = self._calculate_cell_value(
                    distance_matrix, 
                    source_word, 
                    target_word, 
                    source_index, 
                    target_index
                )
        
        return distance_matrix[source_length][target_length]
    
    def _initialize_dp_table(self, source_length: int, target_length: int) -> List[List[int]]:
        """
        Initialize the dynamic programming table with base cases.
        
        Args:
            source_length: Length of source string
            target_length: Length of target string
            
        Returns:
            Initialized 2D DP table
        """
        distance_matrix = [[0] * (target_length + 1) for _ in range(source_length + 1)]
        
        # Initialize first row (empty string to target)
        for target_index in range(target_length + 1):
            distance_matrix[0][target_index] = target_index
            
        # Initialize first column (source to empty string)
        for source_index in range(source_length + 1):
            distance_matrix[source_index][0] = source_index
            
        return distance_matrix
    
    def _calculate_cell_value(
        self, 
        distance_matrix: List[List[int]], 
        source_word: str, 
        target_word: str, 
        source_index: int, 
        target_index: int
    ) -> int:
        """
        Calculate the value for a specific cell in the DP table.
        
        Args:
            distance_matrix: The DP table being filled
            source_word: The source string
            target_word: The target string
            source_index: Current position in source string (1-indexed)
            target_index: Current position in target string (1-indexed)
            
        Returns:
            The minimum operations needed for this subproblem
        """
        # Characters match, no operation needed
        if source_word[source_index - 1] == target_word[target_index - 1]:
            return distance_matrix[source_index - 1][target_index - 1]
        
        # Characters don't match, consider all three operations
        replace_cost = distance_matrix[source_index - 1][target_index - 1] + 1  # Replace
        insert_cost = distance_matrix[source_index][target_index - 1] + 1       # Insert
        delete_cost = distance_matrix[source_index - 1][target_index] + 1       # Delete
        
        return min(replace_cost, insert_cost, delete_cost)