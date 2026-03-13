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
            
        return self._calculate_edit_distance(word1, word2)
    
    def _calculate_edit_distance(self, source_word: str, target_word: str) -> int:
        """
        Helper method to calculate edit distance using dynamic programming.
        
        Args:
            source_word: The string to transform from
            target_word: The string to transform to
            
        Returns:
            Minimum edit distance between the two strings
        """
        source_length = len(source_word)
        target_length = len(target_word)
        
        # Handle edge cases
        if source_length == 0:
            return target_length
        if target_length == 0:
            return source_length
        
        # Initialize DP table with base cases
        distance_matrix = self._initialize_distance_matrix(source_length, target_length)
        
        # Fill the DP table
        for source_index in range(1, source_length + 1):
            for target_index in range(1, target_length + 1):
                if source_word[source_index - 1] == target_word[target_index - 1]:
                    # Characters match, no operation needed
                    distance_matrix[source_index][target_index] = distance_matrix[source_index - 1][target_index - 1]
                else:
                    # Characters don't match, consider all operations
                    insert_cost = distance_matrix[source_index][target_index - 1] + 1
                    delete_cost = distance_matrix[source_index - 1][target_index] + 1
                    replace_cost = distance_matrix[source_index - 1][target_index - 1] + 1
                    
                    distance_matrix[source_index][target_index] = min(insert_cost, delete_cost, replace_cost)
        
        return distance_matrix[source_length][target_length]
    
    def _initialize_distance_matrix(self, source_length: int, target_length: int) -> list[list[int]]:
        """
        Initialize the DP matrix with base cases.
        
        Args:
            source_length: Length of the source string
            target_length: Length of the target string
            
        Returns:
            Initialized 2D matrix for dynamic programming
        """
        distance_matrix = [[0] * (target_length + 1) for _ in range(source_length + 1)]
        
        # Base case: transforming empty string to target requires target_length insertions
        for target_index in range(target_length + 1):
            distance_matrix[0][target_index] = target_index
        
        # Base case: transforming source to empty string requires source_length deletions
        for source_index in range(source_length + 1):
            distance_matrix[source_index][0] = source_index
            
        return distance_matrix