from functools import lru_cache
from typing import Optional

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        """
        Determines if the entire input string matches the regular expression pattern.
        
        Args:
            s: Input string to match against pattern
            p: Pattern string containing '.' and '*' wildcards
            
        Returns:
            True if string matches pattern completely, False otherwise
            
        Raises:
            TypeError: If inputs are not strings
        """
        if not isinstance(s, str) or not isinstance(p, str):
            raise TypeError("Both s and p must be strings")
            
        return self._match_recursive(s, p, 0, 0)
    
    @lru_cache(maxsize=None)
    def _match_recursive(self, string: str, pattern: str, string_index: int, pattern_index: int) -> bool:
        """
        Recursively matches string against pattern using dynamic programming with memoization.
        
        Args:
            string: Input string to match
            pattern: Pattern to match against
            string_index: Current position in string
            pattern_index: Current position in pattern
            
        Returns:
            True if remaining string matches remaining pattern
        """
        # Base case: reached end of pattern
        if pattern_index == len(pattern):
            return string_index == len(string)
        
        # Check if current characters match
        current_char_matches = (
            string_index < len(string) and 
            (pattern[pattern_index] == string[string_index] or pattern[pattern_index] == '.')
        )
        
        # Handle star quantifier case
        if pattern_index + 1 < len(pattern) and pattern[pattern_index + 1] == '*':
            return self._handle_star_quantifier(string, pattern, string_index, pattern_index, current_char_matches)
        
        # No star quantifier - must match current character and continue
        return (
            current_char_matches and 
            self._match_recursive(string, pattern, string_index + 1, pattern_index + 1)
        )
    
    def _handle_star_quantifier(self, string: str, pattern: str, string_index: int, pattern_index: int, current_char_matches: bool) -> bool:
        """
        Handles the star quantifier logic for zero or more occurrences.
        
        Args:
            string: Input string to match
            pattern: Pattern to match against
            string_index: Current position in string
            pattern_index: Current position in pattern
            current_char_matches: Whether current characters match
            
        Returns:
            True if star quantifier matching succeeds
        """
        # Try zero occurrences - skip pattern character and star
        zero_matches = self._match_recursive(string, pattern, string_index, pattern_index + 2)
        
        # Try one or more occurrences if current character matches
        one_or_more_matches = (
            current_char_matches and 
            self._match_recursive(string, pattern, string_index + 1, pattern_index)
        )
        
        return zero_matches or one_or_more_matches