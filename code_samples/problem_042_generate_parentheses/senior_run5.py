from typing import List


class Solution:
    def generateParentheses(self, n: int) -> List[str]:
        """
        Generate all combinations of well-formed parentheses for n pairs.
        
        Args:
            n: Number of pairs of parentheses to generate
            
        Returns:
            List of all valid parentheses combinations
        """
        if n <= 0:
            return []
        
        result_combinations = []
        self._generate_valid_combinations(
            current_combination="",
            open_count=0,
            close_count=0,
            max_pairs=n,
            result_list=result_combinations
        )
        return result_combinations
    
    def _generate_valid_combinations(
        self, 
        current_combination: str, 
        open_count: int, 
        close_count: int, 
        max_pairs: int, 
        result_list: List[str]
    ) -> None:
        """
        Recursively generate valid parentheses combinations using backtracking.
        
        Args:
            current_combination: Current string being built
            open_count: Number of opening parentheses used
            close_count: Number of closing parentheses used
            max_pairs: Maximum number of pairs allowed
            result_list: List to store valid combinations
        """
        # Base case: complete valid combination found
        if len(current_combination) == max_pairs * 2:
            result_list.append(current_combination)
            return
        
        # Add opening parenthesis if we haven't reached the limit
        if open_count < max_pairs:
            self._generate_valid_combinations(
                current_combination + "(",
                open_count + 1,
                close_count,
                max_pairs,
                result_list
            )
        
        # Add closing parenthesis if it maintains validity
        if close_count < open_count:
            self._generate_valid_combinations(
                current_combination + ")",
                open_count,
                close_count + 1,
                max_pairs,
                result_list
            )