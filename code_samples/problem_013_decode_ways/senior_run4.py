class Solution:
    def numDecodings(self, s: str) -> int:
        """
        Calculates the number of ways to decode a string of digits.
        
        Args:
            s: String containing only digits
            
        Returns:
            Number of possible decodings
            
        Raises:
            ValueError: If string contains invalid characters
        """
        if not s or not self._is_valid_input(s):
            return 0
            
        return self._decode_with_memoization(s)
    
    def _is_valid_input(self, s: str) -> bool:
        """
        Validates that input string contains only digits.
        
        Args:
            s: Input string to validate
            
        Returns:
            True if string is valid, False otherwise
        """
        return s.isdigit()
    
    def _decode_with_memoization(self, s: str) -> int:
        """
        Uses dynamic programming with memoization to count decodings.
        
        Args:
            s: String of digits to decode
            
        Returns:
            Number of possible decodings
        """
        memo_cache = {}
        return self._decode_recursive(s, 0, memo_cache)
    
    def _decode_recursive(self, s: str, current_index: int, memo_cache: dict) -> int:
        """
        Recursively calculates number of decodings from current position.
        
        Args:
            s: String of digits
            current_index: Current position in string
            memo_cache: Memoization cache
            
        Returns:
            Number of decodings from current position
        """
        # Base case: reached end of string
        if current_index == len(s):
            return 1
        
        # Check memoization cache
        if current_index in memo_cache:
            return memo_cache[current_index]
        
        # Invalid case: leading zero
        if s[current_index] == '0':
            memo_cache[current_index] = 0
            return 0
        
        total_decodings = 0
        
        # Try single digit decoding (1-9)
        total_decodings += self._decode_recursive(s, current_index + 1, memo_cache)
        
        # Try two digit decoding (10-26)
        if self._is_valid_two_digit_code(s, current_index):
            total_decodings += self._decode_recursive(s, current_index + 2, memo_cache)
        
        memo_cache[current_index] = total_decodings
        return total_decodings
    
    def _is_valid_two_digit_code(self, s: str, start_index: int) -> bool:
        """
        Checks if two digits starting at index form a valid code (10-26).
        
        Args:
            s: String of digits
            start_index: Starting position to check
            
        Returns:
            True if valid two-digit code, False otherwise
        """
        if start_index + 1 >= len(s):
            return False
        
        two_digit_number = int(s[start_index:start_index + 2])
        return 10 <= two_digit_number <= 26