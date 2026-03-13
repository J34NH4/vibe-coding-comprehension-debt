class Solution:
    def numDecodings(self, s: str) -> int:
        """
        Calculate the number of ways to decode a string of digits.
        
        Uses dynamic programming to count valid decodings where:
        - Single digits 1-9 map to A-I
        - Two digits 10-26 map to J-Z
        
        Args:
            s: String containing only digits
            
        Returns:
            Number of possible decodings
            
        Raises:
            ValueError: If input string is empty or contains invalid characters
        """
        if not s or not s.isdigit():
            raise ValueError("Input must be a non-empty string of digits")
            
        string_length = len(s)
        
        # Handle edge case of empty string
        if string_length == 0:
            return 0
            
        # Handle edge case of string starting with '0'
        if s[0] == '0':
            return 0
            
        # dp[i] represents number of ways to decode s[:i]
        dp_array = [0] * (string_length + 1)
        dp_array[0] = 1  # Empty string has one way to decode
        dp_array[1] = 1  # First character (if not '0') has one way
        
        for current_index in range(2, string_length + 1):
            # Check single digit decoding
            single_digit = int(s[current_index - 1])
            if self._is_valid_single_digit(single_digit):
                dp_array[current_index] += dp_array[current_index - 1]
                
            # Check two digit decoding
            two_digit = int(s[current_index - 2:current_index])
            if self._is_valid_two_digit(two_digit):
                dp_array[current_index] += dp_array[current_index - 2]
                
        return dp_array[string_length]
    
    def _is_valid_single_digit(self, digit: int) -> bool:
        """
        Check if a single digit can be decoded (1-9).
        
        Args:
            digit: Single digit to validate
            
        Returns:
            True if digit can be decoded as single character
        """
        return 1 <= digit <= 9
    
    def _is_valid_two_digit(self, two_digit: int) -> bool:
        """
        Check if a two digit number can be decoded (10-26).
        
        Args:
            two_digit: Two digit number to validate
            
        Returns:
            True if two_digit can be decoded as single character
        """
        return 10 <= two_digit <= 26