from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """
        Generate all possible letter combinations from phone number digits.
        
        Args:
            digits: String containing digits from 2-9
            
        Returns:
            List of all possible letter combinations
            
        Raises:
            ValueError: If digits contain invalid characters
        """
        if not digits:
            return []
            
        # Phone keypad mapping
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
        
        # Validate input digits
        for digit in digits:
            if digit not in DIGIT_TO_LETTERS:
                raise ValueError(f"Invalid digit: {digit}")
        
        result_combinations = []
        current_combination = []
        
        self._generate_combinations(
            digits, 
            0, 
            current_combination, 
            result_combinations, 
            DIGIT_TO_LETTERS
        )
        
        return result_combinations
    
    def _generate_combinations(
        self,
        digits: str,
        current_index: int,
        current_combination: List[str],
        result_combinations: List[str],
        digit_to_letters: dict
    ) -> None:
        """
        Recursively generate all letter combinations using backtracking.
        
        Args:
            digits: Input digit string
            current_index: Current position in digits string
            current_combination: Current combination being built
            result_combinations: List to store all valid combinations
            digit_to_letters: Mapping of digits to their letters
        """
        # Base case: reached end of digits string
        if current_index == len(digits):
            result_combinations.append(''.join(current_combination))
            return
        
        current_digit = digits[current_index]
        possible_letters = digit_to_letters[current_digit]
        
        # Try each letter for current digit
        for letter in possible_letters:
            current_combination.append(letter)  # Choose
            self._generate_combinations(
                digits,
                current_index + 1,
                current_combination,
                result_combinations,
                digit_to_letters
            )  # Explore
            current_combination.pop()  # Backtrack