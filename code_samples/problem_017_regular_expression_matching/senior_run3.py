class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Determines if string s matches pattern p with '.' and '*' support.
        
        Args:
            s: Input string to match
            p: Pattern string with '.' (any char) and '*' (zero or more) support
            
        Returns:
            bool: True if s matches pattern p, False otherwise
        """
        if not isinstance(s, str) or not isinstance(p, str):
            raise TypeError("Both s and p must be strings")
            
        return self._match_with_memoization(s, p)
    
    def _match_with_memoization(self, string: str, pattern: str) -> bool:
        """
        Uses dynamic programming with memoization for efficient matching.
        
        Args:
            string: Input string to match
            pattern: Pattern to match against
            
        Returns:
            bool: True if string matches pattern
        """
        memo_cache = {}
        
        def _helper(string_index: int, pattern_index: int) -> bool:
            """
            Recursive helper with memoization for pattern matching.
            
            Args:
                string_index: Current position in input string
                pattern_index: Current position in pattern
                
            Returns:
                bool: True if remaining string matches remaining pattern
            """
            if (string_index, pattern_index) in memo_cache:
                return memo_cache[(string_index, pattern_index)]
            
            # Base case: reached end of pattern
            if pattern_index >= len(pattern):
                result = string_index >= len(string)
                memo_cache[(string_index, pattern_index)] = result
                return result
            
            # Check if current characters match
            current_char_matches = (
                string_index < len(string) and 
                (pattern[pattern_index] == string[string_index] or 
                 pattern[pattern_index] == '.')
            )
            
            # Handle '*' wildcard (zero or more of preceding character)
            if pattern_index + 1 < len(pattern) and pattern[pattern_index + 1] == '*':
                result = (
                    # Case 1: Use '*' as zero occurrences (skip current pattern char and '*')
                    _helper(string_index, pattern_index + 2) or
                    # Case 2: Use '*' as one or more occurrences (current char matches and advance string)
                    (current_char_matches and _helper(string_index + 1, pattern_index))
                )
            else:
                # No '*' wildcard: must match current character exactly
                result = current_char_matches and _helper(string_index + 1, pattern_index + 1)
            
            memo_cache[(string_index, pattern_index)] = result
            return result
        
        return _helper(0, 0)