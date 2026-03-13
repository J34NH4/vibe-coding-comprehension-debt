from typing import List, Dict
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        Groups anagrams together from a list of strings.
        
        Args:
            strs: List of strings to group by anagrams
            
        Returns:
            List of lists where each inner list contains anagrams
            
        Raises:
            TypeError: If input is not a list or contains non-string elements
        """
        if not isinstance(strs, list):
            raise TypeError("Input must be a list")
            
        if not strs:  # Handle empty input
            return []
            
        anagram_groups = self._build_anagram_groups(strs)
        return self._extract_grouped_anagrams(anagram_groups)
    
    def _build_anagram_groups(self, strings: List[str]) -> Dict[str, List[str]]:
        """
        Builds a dictionary mapping sorted character signatures to anagram groups.
        
        Args:
            strings: List of strings to process
            
        Returns:
            Dictionary mapping sorted signatures to lists of anagrams
            
        Raises:
            TypeError: If any element in strings is not a string
        """
        anagram_groups: Dict[str, List[str]] = defaultdict(list)
        
        for current_string in strings:
            if not isinstance(current_string, str):
                raise TypeError("All elements must be strings")
                
            sorted_signature = self._generate_sorted_signature(current_string)
            anagram_groups[sorted_signature].append(current_string)  # Group by signature
            
        return anagram_groups
    
    def _generate_sorted_signature(self, input_string: str) -> str:
        """
        Generates a sorted character signature for anagram detection.
        
        Args:
            input_string: String to generate signature for
            
        Returns:
            String with characters sorted alphabetically
        """
        return ''.join(sorted(input_string))  # Sort characters to create signature
    
    def _extract_grouped_anagrams(self, anagram_groups: Dict[str, List[str]]) -> List[List[str]]:
        """
        Extracts anagram groups from the mapping dictionary.
        
        Args:
            anagram_groups: Dictionary mapping signatures to anagram lists
            
        Returns:
            List of anagram groups
        """
        return list(anagram_groups.values())  # Return all grouped anagrams