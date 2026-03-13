class Solution:
    def numDecodings(self, s: str) -> int:
        """
        Calculate the number of ways to decode a numeric string.
        
        Args:
            s: String containing only digits
            
        Returns:
            Number of possible decodings
            
        Raises:
            ValueError: If string contains invalid characters
        """
        if not s or not self._is_valid_input(s):
            return 0
            
        string_length = len(s)
        # dp[i] represents number of ways to decode s[:i]
        decode_ways = [0] * (string_length + 1)
        
        # Base cases
        decode_ways[0] = 1  # Empty string has one way to decode
        decode_ways[1] = 1 if self._is_valid_single_digit(s[0]) else 0
        
        for current_position in range(2, string_length + 1):
            single_digit = s[current_position - 1]
            double_digit = s[current_position - 2:current_position]
            
            # Check if single digit forms valid encoding
            if self._is_valid_single_digit(single_digit):
                decode_ways[current_position] += decode_ways[current_position - 1]
            
            # Check if double digit forms valid encoding
            if self._is_valid_double_digit(double_digit):
                decode_ways[current_position] += decode_ways[current_position - 2]
        
        return decode_ways[string_length]
    
    def _is_valid_input(self, s: str) -> bool:
        """
        Validate input string contains only digits.
        
        Args:
            s: Input string to validate
            
        Returns:
            True if string contains only digits, False otherwise
        """
        return s.isdigit()
    
    def _is_valid_single_digit(self, digit: str) -> bool:
        """
        Check if single digit can be decoded (1-9).
        
        Args:
            digit: Single character digit
            
        Returns:
            True if digit can be decoded as single character
        """
        return digit != '0'
    
    def _is_valid_double_digit(self, double_digit: str) -> bool:
        """
        Check if two digits can be decoded as single character (10-26).
        
        Args:
            double_digit: Two character string
            
        Returns:
            True if double digit can be decoded as single character
        """
        if len(double_digit) != 2:
            return False
        
        numeric_value = int(double_digit)
        return 10 <= numeric_value <= 26