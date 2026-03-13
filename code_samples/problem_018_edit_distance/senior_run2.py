class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        """
        Calculate the minimum edit distance between two strings using dynamic programming.
        
        Uses the Wagner-Fischer algorithm (Levenshtein distance) to find the minimum
        number of single-character edits (insertions, deletions, or substitutions)
        required to change one word into another.
        
        Args:
            word1: The source string to transform
            word2: The target string to transform into
            
        Returns:
            The minimum number of operations needed to transform word1 into word2
            
        Raises:
            TypeError: If either input is not a string
        """
        if not isinstance(word1, str) or not isinstance(word2, str):
            raise TypeError("Both inputs must be strings")
            
        return self._calculate_edit_distance_dp(word1, word2)
    
    def _calculate_edit_distance_dp(self, source_word: str, target_word: str) -> int:
        """
        Calculate edit distance using bottom-up dynamic programming approach.
        
        Args:
            source_word: The source string
            target_word: The target string
            
        Returns:
            Minimum edit distance between the two strings
        """
        source_length = len(source_word)
        target_length = len(target_word)
        
        # Handle edge cases
        if source_length == 0:
            return target_length  # Insert all characters from target
        if target_length == 0:
            return source_length  # Delete all characters from source
        
        # Initialize DP table with base cases
        distance_matrix = self._initialize_dp_table(source_length, target_length)
        
        # Fill the DP table
        for source_index in range(1, source_length + 1):
            for target_index in range(1, target_length + 1):
                distance_matrix[source_index][target_index] = self._calculate_min_operations(
                    distance_matrix, 
                    source_word, 
                    target_word, 
                    source_index, 
                    target_index
                )
        
        return distance_matrix[source_length][target_length]
    
    def _initialize_dp_table(self, source_length: int, target_length: int) -> list[list[int]]:
        """
        Initialize the dynamic programming table with base cases.
        
        Args:
            source_length: Length of the source string
            target_length: Length of the target string
            
        Returns:
            Initialized 2D DP table with base cases filled
        """
        distance_matrix = [[0] * (target_length + 1) for _ in range(source_length + 1)]
        
        # Base case: transforming empty string to target requires insertions
        for target_index in range(target_length + 1):
            distance_matrix[0][target_index] = target_index
        
        # Base case: transforming source to empty string requires deletions
        for source_index in range(source_length + 1):
            distance_matrix[source_index][0] = source_index
            
        return distance_matrix
    
    def _calculate_min_operations(
        self, 
        distance_matrix: list[list[int]], 
        source_word: str, 
        target_word: str, 
        source_index: int, 
        target_index: int
    ) -> int:
        """
        Calculate minimum operations for current position in DP table.
        
        Args:
            distance_matrix: The DP table being filled
            source_word: The source string
            target_word: The target string
            source_index: Current position in source string (1-indexed for DP)
            target_index: Current position in target string (1-indexed for DP)
            
        Returns:
            Minimum operations needed at this position
        """
        # Characters match, no operation needed
        if source_word[source_index - 1] == target_word[target_index - 1]:
            return distance_matrix[source_index - 1][target_index - 1]
        
        # Characters don't match, consider all three operations
        substitution_cost = distance_matrix[source_index - 1][target_index - 1] + 1  # Replace
        insertion_cost = distance_matrix[source_index][target_index - 1] + 1         # Insert
        deletion_cost = distance_matrix[source_index - 1][target_index] + 1          # Delete
        
        return min(substitution_cost, insertion_cost, deletion_cost)