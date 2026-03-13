from typing import List, Set
from collections import deque

class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        """
        Remove the minimum number of invalid parentheses to make the input string valid.
        
        Args:
            s: Input string containing parentheses and letters
            
        Returns:
            List of all possible valid strings after removing minimum invalid parentheses
        """
        if not s:
            return [""]
        
        # Find minimum removals needed
        min_left_removals, min_right_removals = self._calculate_minimum_removals(s)
        
        result_set: Set[str] = set()
        self._backtrack(s, 0, min_left_removals, min_right_removals, 
                       0, 0, "", result_set)
        
        return list(result_set)
    
    def _calculate_minimum_removals(self, s: str) -> tuple[int, int]:
        """
        Calculate minimum number of left and right parentheses to remove.
        
        Args:
            s: Input string
            
        Returns:
            Tuple of (left_removals, right_removals)
        """
        left_removals = 0
        right_removals = 0
        
        # Count excess closing parentheses
        for char in s:
            if char == '(':
                left_removals += 1
            elif char == ')':
                if left_removals > 0:
                    left_removals -= 1  # Matched with opening
                else:
                    right_removals += 1  # Excess closing
        
        return left_removals, right_removals
    
    def _backtrack(self, s: str, current_index: int, left_removals: int, 
                   right_removals: int, open_count: int, close_count: int,
                   current_expression: str, result_set: Set[str]) -> None:
        """
        Backtrack to generate all valid expressions.
        
        Args:
            s: Original string
            current_index: Current position in string
            left_removals: Remaining left parentheses to remove
            right_removals: Remaining right parentheses to remove
            open_count: Current count of unmatched opening parentheses
            close_count: Current count of closing parentheses
            current_expression: Current valid expression being built
            result_set: Set to store valid results
        """
        # Base case: processed all characters
        if current_index == len(s):
            if left_removals == 0 and right_removals == 0 and open_count == close_count:
                result_set.add(current_expression)
            return
        
        current_char = s[current_index]
        
        # Option 1: Remove current character (if it's a parenthesis and we need to remove)
        if current_char == '(' and left_removals > 0:
            self._backtrack(s, current_index + 1, left_removals - 1, right_removals,
                           open_count, close_count, current_expression, result_set)
        
        if current_char == ')' and right_removals > 0:
            self._backtrack(s, current_index + 1, left_removals, right_removals - 1,
                           open_count, close_count, current_expression, result_set)
        
        # Option 2: Keep current character
        new_expression = current_expression + current_char
        
        if current_char == '(':
            # Add opening parenthesis
            self._backtrack(s, current_index + 1, left_removals, right_removals,
                           open_count + 1, close_count, new_expression, result_set)
        elif current_char == ')':
            # Add closing parenthesis only if it doesn't create invalid state
            if open_count > close_count:
                self._backtrack(s, current_index + 1, left_removals, right_removals,
                               open_count, close_count + 1, new_expression, result_set)
        else:
            # Regular character - always add
            self._backtrack(s, current_index + 1, left_removals, right_removals,
                           open_count, close_count, new_expression, result_set)