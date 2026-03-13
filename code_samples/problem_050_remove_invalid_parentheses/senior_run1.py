from typing import List, Set
from collections import deque

class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        """
        Remove the minimum number of invalid parentheses to make the string valid.
        
        Args:
            s: Input string containing parentheses and letters
            
        Returns:
            List of all possible valid strings after minimum removals
        """
        if not s:
            return [""]
            
        # Find minimum removals needed
        left_remove, right_remove = self._calculate_minimum_removals(s)
        
        result_set: Set[str] = set()
        self._backtrack(s, 0, left_remove, right_remove, 0, "", result_set)
        
        return list(result_set)
    
    def _calculate_minimum_removals(self, s: str) -> tuple[int, int]:
        """
        Calculate minimum number of left and right parentheses to remove.
        
        Args:
            s: Input string
            
        Returns:
            Tuple of (left_removals, right_removals)
        """
        left_remove = 0  # Count of '(' to remove
        right_remove = 0  # Count of ')' to remove
        
        for char in s:
            if char == '(':
                left_remove += 1
            elif char == ')':
                if left_remove > 0:
                    left_remove -= 1  # Match with previous '('
                else:
                    right_remove += 1  # Unmatched ')'
        
        return left_remove, right_remove
    
    def _backtrack(self, s: str, index: int, left_remove: int, right_remove: int, 
                   open_count: int, current_string: str, result_set: Set[str]) -> None:
        """
        Backtrack to find all valid combinations after minimum removals.
        
        Args:
            s: Original string
            index: Current position in string
            left_remove: Remaining '(' to remove
            right_remove: Remaining ')' to remove
            open_count: Count of unmatched '(' so far
            current_string: Current valid string being built
            result_set: Set to store all valid results
        """
        # Base case: processed all characters
        if index == len(s):
            if left_remove == 0 and right_remove == 0 and open_count == 0:
                result_set.add(current_string)
            return
        
        current_char = s[index]
        
        # Option 1: Remove current character (if it's a parenthesis we need to remove)
        if (current_char == '(' and left_remove > 0) or (current_char == ')' and right_remove > 0):
            new_left_remove = left_remove - 1 if current_char == '(' else left_remove
            new_right_remove = right_remove - 1 if current_char == ')' else right_remove
            self._backtrack(s, index + 1, new_left_remove, new_right_remove, 
                          open_count, current_string, result_set)
        
        # Option 2: Keep current character
        if current_char == '(':
            # Always safe to add '('
            self._backtrack(s, index + 1, left_remove, right_remove, 
                          open_count + 1, current_string + current_char, result_set)
        elif current_char == ')':
            # Only add ')' if we have unmatched '('
            if open_count > 0:
                self._backtrack(s, index + 1, left_remove, right_remove, 
                              open_count - 1, current_string + current_char, result_set)
        else:
            # Regular character - always keep
            self._backtrack(s, index + 1, left_remove, right_remove, 
                          open_count, current_string + current_char, result_set)