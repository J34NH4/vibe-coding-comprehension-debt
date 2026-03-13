from typing import List

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """
        Generate all possible letter combinations from phone number digits.
        
        Args:
            digits: String containing digits from 2-9
            
        Returns:
            List of all possible letter combinations
        """
        if not digits:
            return []
        
        # Phone number to letters mapping
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
        
        self._generate_combinations(
            digits=digits,
            current_index=0,
            current_combination="",
            digit_mapping=DIGIT_TO_LETTERS,
            result_list=result_combinations
        )
        
        return result_combinations
    
    def _generate_combinations(
        self,
        digits: str,
        current_index: int,
        current_combination: str,
        digit_mapping: dict,
        result_list: List[str]
    ) -> None:
        """
        Recursively generate all letter combinations using backtracking.
        
        Args:
            digits: Input digit string
            current_index: Current position in digits string
            current_combination: Current combination being built
            digit_mapping: Dictionary mapping digits to letters
            result_list: List to store final combinations
        """
        # Base case: reached end of digits string
        if current_index == len(digits):
            result_list.append(current_combination)
            return
        
        current_digit = digits[current_index]
        possible_letters = digit_mapping[current_digit]
        
        # Try each possible letter for current digit
        for letter in possible_letters:
            self._generate_combinations(
                digits=digits,
                current_index=current_index + 1,
                current_combination=current_combination + letter,
                digit_mapping=digit_mapping,
                result_list=result_list
            )