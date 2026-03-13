from typing import List, Dict
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        Groups anagrams together from an array of strings.
        
        Args:
            strs: List of strings to group by anagrams
            
        Returns:
            List of lists where each inner list contains anagrams
            
        Raises:
            TypeError: If input is not a list of strings
        """
        if not isinstance(strs, list):
            raise TypeError("Input must be a list of strings")
        
        # Handle edge case of empty input
        if not strs:
            return []
        
        anagram_groups = self._build_anagram_groups(strs)
        return self._extract_grouped_anagrams(anagram_groups)
    
    def _build_anagram_groups(self, strings: List[str]) -> Dict[tuple, List[str]]:
        """
        Builds a dictionary mapping sorted character tuples to anagram groups.
        
        Args:
            strings: List of strings to process
            
        Returns:
            Dictionary with sorted character tuples as keys and anagram lists as values
        """
        anagram_groups = defaultdict(list)
        
        for current_string in strings:
            # Sort characters to create anagram key
            sorted_characters = tuple(sorted(current_string))
            anagram_groups[sorted_characters].append(current_string)
        
        return anagram_groups
    
    def _extract_grouped_anagrams(self, anagram_groups: Dict[tuple, List[str]]) -> List[List[str]]:
        """
        Extracts the grouped anagrams from the dictionary into a list format.
        
        Args:
            anagram_groups: Dictionary mapping sorted character tuples to anagram groups
            
        Returns:
            List of anagram groups
        """
        return list(anagram_groups.values())