from functools import lru_cache
from typing import Dict, Tuple


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Determines if string s matches pattern p with '.' and '*' support.
        
        Args:
            s: Input string to match
            p: Pattern string with '.' (any char) and '*' (zero or more of preceding)
            
        Returns:
            True if s matches pattern p, False otherwise
        """
        if not isinstance(s, str) or not isinstance(p, str):
            raise ValueError("Input must be strings")
            
        return self._match_with_memoization(s, p)
    
    def _match_with_memoization(self, input_string: str, pattern: str) -> bool:
        """
        Uses memoization to efficiently match string against pattern.
        
        Args:
            input_string: String to match
            pattern: Pattern with wildcards
            
        Returns:
            True if match found, False otherwise
        """
        memo_cache: Dict[Tuple[int, int], bool] = {}
        
        def match_recursive(string_index: int, pattern_index: int) -> bool:
            """
            Recursively matches string against pattern with memoization.
            
            Args:
                string_index: Current position in input string
                pattern_index: Current position in pattern
                
            Returns:
                True if remaining portions match, False otherwise
            """
            # Check memoization cache
            cache_key = (string_index, pattern_index)
            if cache_key in memo_cache:
                return memo_cache[cache_key]
            
            # Base case: reached end of pattern
            if pattern_index >= len(pattern):
                result = string_index >= len(input_string)
                memo_cache[cache_key] = result
                return result
            
            # Check if current characters match
            current_chars_match = (
                string_index < len(input_string) and
                (pattern[pattern_index] == input_string[string_index] or 
                 pattern[pattern_index] == '.')
            )
            
            # Handle '*' wildcard (zero or more of preceding character)
            if pattern_index + 1 < len(pattern) and pattern[pattern_index + 1] == '*':
                # Two options: skip the pattern (zero occurrences) or use it if chars match
                result = (
                    match_recursive(string_index, pattern_index + 2) or  # Skip pattern
                    (current_chars_match and match_recursive(string_index + 1, pattern_index))  # Use pattern
                )
            else:
                # No wildcard: must match current character and continue
                result = current_chars_match and match_recursive(string_index + 1, pattern_index + 1)
            
            memo_cache[cache_key] = result
            return result
        
        return match_recursive(0, 0)