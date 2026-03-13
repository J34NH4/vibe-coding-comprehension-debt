from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """
        Generate all possible letter combinations for given phone number digits.
        
        Args:
            digits: String containing digits from 2-9
            
        Returns:
            List of all possible letter combinations
        """
        if not digits:
            return []
            
        # Define digit to letters mapping
        DIGIT_TO_LETTERS = {
            '2': 'abc',
            '3': 'def',
            '4': 'ghi',
            '5': 'jkl',
            '6': 'mno',
            '7': 'pqrs',
            '8': 'tuv',
            '9': 'wxyz'
        }
        
        result_combinations = []
        
        def generate_combinations(current_index: int, current_combination: str) -> None:
            """
            Recursively generate letter combinations using backtracking.
            
            Args:
                current_index: Current position in digits string
                current_combination: Current combination being built
            """
            # Base case: reached end of digits
            if current_index == len(digits):
                result_combinations.append(current_combination)
                return
            
            current_digit = digits[current_index]
            
            # Handle invalid digits
            if current_digit not in DIGIT_TO_LETTERS:
                return
            
            possible_letters = DIGIT_TO_LETTERS[current_digit]
            
            # Try each possible letter for current digit
            for letter in possible_letters:
                generate_combinations(current_index + 1, current_combination + letter)
        
        generate_combinations(0, "")
        return result_combinations