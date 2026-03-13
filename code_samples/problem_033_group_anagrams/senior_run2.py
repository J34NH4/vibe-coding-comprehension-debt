from typing import List, Dict
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        Groups anagrams together from a list of strings.
        
        Args:
            strs: List of strings to group by anagrams
            
        Returns:
            List of lists where each inner list contains anagram groups
            
        Raises:
            TypeError: If strs is not a list or contains non-string elements
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
            Dictionary with sorted chars as keys and anagram lists as values
        """
        anagram_groups: Dict[str, List[str]] = defaultdict(list)
        
        for current_string in strings:
            if not isinstance(current_string, str):
                raise TypeError("All elements must be strings")
                
            # Sort characters to create anagram signature
            sorted_signature = self._generate_anagram_signature(current_string)
            anagram_groups[sorted_signature].append(current_string)
            
        return anagram_groups
    
    def _generate_anagram_signature(self, word: str) -> str:
        """
        Generates a unique signature for anagram identification.
        
        Args:
            word: String to generate signature for
            
        Returns:
            Sorted character string as anagram signature
        """
        return ''.join(sorted(word))  # Sort chars to normalize anagrams
    
    def _extract_grouped_anagrams(self, anagram_groups: Dict[str, List[str]]) -> List[List[str]]:
        """
        Extracts anagram groups from the dictionary into result format.
        
        Args:
            anagram_groups: Dictionary mapping signatures to anagram lists
            
        Returns:
            List of anagram groups ready for output
        """
        return list(anagram_groups.values())