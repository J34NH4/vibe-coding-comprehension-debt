from typing import List, Set
from collections import deque

class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        """
        Remove the minimum number of invalid parentheses to make the input string valid.
        
        Args:
            s: Input string containing parentheses and letters
            
        Returns:
            List of all possible valid strings after minimum removals
        """
        if not s:
            return [""]
        
        # Find minimum number of left and right parentheses to remove
        left_to_remove, right_to_remove = self._calculate_removals(s)
        
        result_set: Set[str] = set()
        self._backtrack(s, 0, left_to_remove, right_to_remove, 0, "", result_set)
        
        return list(result_set)
    
    def _calculate_removals(self, s: str) -> tuple[int, int]:
        """
        Calculate minimum number of left and right parentheses to remove.
        
        Args:
            s: Input string
            
        Returns:
            Tuple of (left_removals, right_removals)
        """
        left_to_remove = 0
        right_to_remove = 0
        
        for char in s:
            if char == '(':
                left_to_remove += 1
            elif char == ')':
                if left_to_remove > 0:
                    left_to_remove -= 1  # Match with previous '('
                else:
                    right_to_remove += 1  # Extra ')' that needs removal
        
        return left_to_remove, right_to_remove
    
    def _backtrack(self, s: str, index: int, left_rem: int, right_rem: int, 
                   open_count: int, current_expression: str, result_set: Set[str]) -> None:
        """
        Backtrack to generate all valid expressions by removing minimum parentheses.
        
        Args:
            s: Original string
            index: Current position in string
            left_rem: Number of left parentheses still to remove
            right_rem: Number of right parentheses still to remove
            open_count: Count of unmatched open parentheses
            current_expression: Current valid expression being built
            result_set: Set to store valid results
        """
        # Base case: processed all characters
        if index == len(s):
            if left_rem == 0 and right_rem == 0 and open_count == 0:
                result_set.add(current_expression)
            return
        
        current_char = s[index]
        
        # Case 1: Skip current character if it's a parenthesis we need to remove
        if (current_char == '(' and left_rem > 0) or (current_char == ')' and right_rem > 0):
            # Remove current parenthesis
            new_left_rem = left_rem - 1 if current_char == '(' else left_rem
            new_right_rem = right_rem - 1 if current_char == ')' else right_rem
            self._backtrack(s, index + 1, new_left_rem, new_right_rem, 
                          open_count, current_expression, result_set)
        
        # Case 2: Keep current character
        new_expression = current_expression + current_char
        
        if current_char == '(':
            # Add opening parenthesis
            self._backtrack(s, index + 1, left_rem, right_rem, 
                          open_count + 1, new_expression, result_set)
        elif current_char == ')' and open_count > 0:
            # Add closing parenthesis only if there's a matching opening one
            self._backtrack(s, index + 1, left_rem, right_rem, 
                          open_count - 1, new_expression, result_set)
        elif current_char != ')':
            # Add regular character (letter)
            self._backtrack(s, index + 1, left_rem, right_rem, 
                          open_count, new_expression, result_set)