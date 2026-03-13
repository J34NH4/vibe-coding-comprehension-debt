from collections import deque
from typing import List, Set


class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        """Remove the minimum number of invalid parentheses to make the input string valid.
        
        Args:
            s: Input string containing parentheses and letters
            
        Returns:
            List of all possible valid strings after removing minimum invalid parentheses
        """
        if not s:
            return [""]
        
        # Find minimum removals needed using BFS
        return self._bfs_remove_parentheses(s)
    
    def _bfs_remove_parentheses(self, input_string: str) -> List[str]:
        """Use BFS to find all valid strings with minimum removals.
        
        Args:
            input_string: The input string to process
            
        Returns:
            List of valid strings with minimum parentheses removed
        """
        queue = deque([input_string])
        visited_strings: Set[str] = {input_string}
        valid_results: List[str] = []
        found_valid_level = False
        
        while queue and not found_valid_level:
            current_level_size = len(queue)
            
            # Process all strings at current level
            for _ in range(current_level_size):
                current_string = queue.popleft()
                
                if self._is_valid_parentheses(current_string):
                    valid_results.append(current_string)
                    found_valid_level = True
                else:
                    # Generate all possible strings by removing one character
                    self._generate_next_level_strings(current_string, queue, visited_strings)
        
        return valid_results if valid_results else [""]
    
    def _is_valid_parentheses(self, string_to_check: str) -> bool:
        """Check if a string has valid parentheses.
        
        Args:
            string_to_check: String to validate
            
        Returns:
            True if parentheses are valid, False otherwise
        """
        open_count = 0
        
        for character in string_to_check:
            if character == '(':
                open_count += 1
            elif character == ')':
                if open_count == 0:
                    return False  # More closing than opening
                open_count -= 1
        
        return open_count == 0  # All parentheses matched
    
    def _generate_next_level_strings(self, current_string: str, queue: deque, visited_strings: Set[str]) -> None:
        """Generate all possible strings by removing one parenthesis.
        
        Args:
            current_string: Current string to generate from
            queue: BFS queue to add new strings to
            visited_strings: Set to track visited strings
        """
        for index in range(len(current_string)):
            character_at_index = current_string[index]
            
            # Only remove parentheses, not letters
            if character_at_index in '()':
                new_string = current_string[:index] + current_string[index + 1:]
                
                # Add to queue if not visited
                if new_string not in visited_strings:
                    visited_strings.add(new_string)
                    queue.append(new_string)