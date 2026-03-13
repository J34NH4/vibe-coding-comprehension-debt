from typing import List, Dict, Tuple

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Implements regular expression matching with support for '.' and '*'.
        
        Args:
            s: Input string to match against
            p: Pattern string containing regular expression
            
        Returns:
            bool: True if string matches pattern, False otherwise
        """
        string_length = len(s)
        pattern_length = len(p)
        
        # Memoization cache for dynamic programming
        memo_cache: Dict[Tuple[int, int], bool] = {}
        
        def match_helper(string_index: int, pattern_index: int) -> bool:
            """
            Recursive helper function with memoization to check pattern matching.
            
            Args:
                string_index: Current position in input string
                pattern_index: Current position in pattern string
                
            Returns:
                bool: True if remaining string matches remaining pattern
            """
            # Check memoization cache first
            if (string_index, pattern_index) in memo_cache:
                return memo_cache[(string_index, pattern_index)]
            
            # Base case: reached end of pattern
            if pattern_index >= pattern_length:
                result = string_index >= string_length
                memo_cache[(string_index, pattern_index)] = result
                return result
            
            # Check if current character matches (considering '.' wildcard)
            current_char_matches = (
                string_index < string_length and 
                (p[pattern_index] == s[string_index] or p[pattern_index] == '.')
            )
            
            # Handle '*' quantifier (zero or more of preceding character)
            if pattern_index + 1 < pattern_length and p[pattern_index + 1] == '*':
                # Two options: skip pattern (zero occurrences) or use pattern if current matches
                result = (
                    match_helper(string_index, pattern_index + 2) or  # Skip pattern
                    (current_char_matches and match_helper(string_index + 1, pattern_index))  # Use pattern
                )
            else:
                # No '*' quantifier: must match current character and continue
                result = current_char_matches and match_helper(string_index + 1, pattern_index + 1)
            
            # Cache result before returning
            memo_cache[(string_index, pattern_index)] = result
            return result
        
        return match_helper(0, 0)