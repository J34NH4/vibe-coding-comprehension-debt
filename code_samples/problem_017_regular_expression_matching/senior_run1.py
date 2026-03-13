from typing import Dict, Tuple

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Determines if the entire input string matches the regular expression pattern.
        
        Args:
            s: The input string to match against
            p: The pattern containing '.' and '*' wildcards
            
        Returns:
            True if the entire string matches the pattern, False otherwise
        """
        if not isinstance(s, str) or not isinstance(p, str):
            raise ValueError("Both input string and pattern must be strings")
            
        # Memoization cache for dynamic programming
        memo_cache: Dict[Tuple[int, int], bool] = {}
        
        def matches_character(string_index: int, pattern_index: int) -> bool:
            """
            Helper function to check if characters at given indices match.
            
            Args:
                string_index: Index in the input string
                pattern_index: Index in the pattern
                
            Returns:
                True if characters match or pattern has '.', False otherwise
            """
            if pattern_index >= len(p):
                return False
            if string_index >= len(s):
                return False
            return s[string_index] == p[pattern_index] or p[pattern_index] == '.'
        
        def solve_recursive(string_index: int, pattern_index: int) -> bool:
            """
            Recursive function with memoization to solve the matching problem.
            
            Args:
                string_index: Current position in the input string
                pattern_index: Current position in the pattern
                
            Returns:
                True if remaining string matches remaining pattern, False otherwise
            """
            # Check memoization cache
            cache_key = (string_index, pattern_index)
            if cache_key in memo_cache:
                return memo_cache[cache_key]
            
            # Base case: reached end of pattern
            if pattern_index >= len(p):
                result = string_index >= len(s)
                memo_cache[cache_key] = result
                return result
            
            # Check if current character matches
            first_character_matches = matches_character(string_index, pattern_index)
            
            # Handle '*' wildcard (zero or more of preceding character)
            if pattern_index + 1 < len(p) and p[pattern_index + 1] == '*':
                # Two options: use * for zero matches OR use * for one+ matches
                zero_matches = solve_recursive(string_index, pattern_index + 2)
                one_or_more_matches = (first_character_matches and 
                                     solve_recursive(string_index + 1, pattern_index))
                result = zero_matches or one_or_more_matches
            else:
                # No '*', must match current character and continue
                result = (first_character_matches and 
                         solve_recursive(string_index + 1, pattern_index + 1))
            
            memo_cache[cache_key] = result
            return result
        
        return solve_recursive(0, 0)