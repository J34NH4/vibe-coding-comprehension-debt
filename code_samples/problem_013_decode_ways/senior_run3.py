class Solution:
    def numDecodings(self, s: str) -> int:
        """
        Calculate the number of ways to decode a string of digits.
        
        Args:
            s: String containing only digits
            
        Returns:
            Number of possible decodings
            
        Raises:
            ValueError: If input string is empty or contains invalid characters
        """
        if not s or s[0] == '0':
            return 0
            
        return self._decode_with_memoization(s, 0, {})
    
    def _decode_with_memoization(self, digit_string: str, current_index: int, memo_cache: dict) -> int:
        """
        Helper method to calculate decodings using memoization.
        
        Args:
            digit_string: The input string of digits
            current_index: Current position in the string
            memo_cache: Dictionary to store computed results
            
        Returns:
            Number of ways to decode from current index to end
        """
        if current_index in memo_cache:
            return memo_cache[current_index]
        
        if current_index == len(digit_string):
            return 1
        
        if digit_string[current_index] == '0':
            return 0
        
        # Single digit decode
        ways_count = self._decode_with_memoization(digit_string, current_index + 1, memo_cache)
        
        # Two digit decode if valid
        if current_index + 1 < len(digit_string):
            two_digit_number = int(digit_string[current_index:current_index + 2])
            if self._is_valid_two_digit_code(two_digit_number):
                ways_count += self._decode_with_memoization(digit_string, current_index + 2, memo_cache)
        
        memo_cache[current_index] = ways_count
        return ways_count
    
    def _is_valid_two_digit_code(self, number: int) -> bool:
        """
        Check if a two-digit number is a valid letter code (10-26).
        
        Args:
            number: Two-digit number to validate
            
        Returns:
            True if number represents a valid letter code
        """
        return 10 <= number <= 26