from collections import deque
from typing import List, Set


class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        """
        Remove minimum number of invalid parentheses to make string valid.
        
        Uses BFS to find all valid strings with minimum removals.
        
        Args:
            s: Input string containing parentheses and letters
            
        Returns:
            List of all valid strings with minimum parentheses removed
        """
        if not s:
            return [""]
        
        result_set: Set[str] = set()
        queue: deque = deque([s])
        visited_strings: Set[str] = {s}
        found_valid: bool = False
        
        while queue and not found_valid:
            current_level_size = len(queue)
            
            for _ in range(current_level_size):
                current_string = queue.popleft()
                
                if self._is_valid_parentheses(current_string):
                    result_set.add(current_string)
                    found_valid = True
                
                if not found_valid:
                    # Generate next level candidates by removing one character
                    self._generate_next_candidates(
                        current_string, queue, visited_strings
                    )
        
        return list(result_set) if result_set else [""]
    
    def _is_valid_parentheses(self, string: str) -> bool:
        """
        Check if string has valid parentheses structure.
        
        Args:
            string: String to validate
            
        Returns:
            True if parentheses are valid, False otherwise
        """
        open_count: int = 0
        
        for character in string:
            if character == '(':
                open_count += 1
            elif character == ')':
                if open_count == 0:
                    return False  # More closing than opening
                open_count -= 1
        
        return open_count == 0  # All parentheses matched
    
    def _generate_next_candidates(
        self, 
        current_string: str, 
        queue: deque, 
        visited_strings: Set[str]
    ) -> None:
        """
        Generate next level candidates by removing one parenthesis.
        
        Args:
            current_string: Current string to generate candidates from
            queue: BFS queue to add new candidates
            visited_strings: Set of already processed strings
        """
        for index in range(len(current_string)):
            character = current_string[index]
            
            # Only remove parentheses, not letters
            if character in '()':
                next_candidate = (
                    current_string[:index] + current_string[index + 1:]
                )
                
                if next_candidate not in visited_strings:
                    visited_strings.add(next_candidate)
                    queue.append(next_candidate)