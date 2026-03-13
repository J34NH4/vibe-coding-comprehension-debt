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
            TypeError: If input is not a list of strings
        """
        if not isinstance(strs, list):
            raise TypeError("Input must be a list of strings")
        
        # Handle empty input
        if not strs:
            return []
        
        anagram_groups = self._build_anagram_groups(strs)
        return self._convert_groups_to_list(anagram_groups)
    
    def _build_anagram_groups(self, strings: List[str]) -> Dict[str, List[str]]:
        """
        Builds a dictionary mapping sorted characters to list of anagrams.
        
        Args:
            strings: List of strings to process
            
        Returns:
            Dictionary with sorted string as key and anagrams as values
        """
        anagram_groups = defaultdict(list)
        
        for current_string in strings:
            if not isinstance(current_string, str):
                raise TypeError("All elements must be strings")
            
            # Sort characters to create anagram key
            sorted_key = self._generate_anagram_key(current_string)
            anagram_groups[sorted_key].append(current_string)
            
        return anagram_groups
    
    def _generate_anagram_key(self, string: str) -> str:
        """
        Generates a unique key for anagrams by sorting characters.
        
        Args:
            string: Input string to generate key for
            
        Returns:
            Sorted string that serves as anagram identifier
        """
        return ''.join(sorted(string))
    
    def _convert_groups_to_list(self, anagram_groups: Dict[str, List[str]]) -> List[List[str]]:
        """
        Converts anagram groups dictionary to list of lists format.
        
        Args:
            anagram_groups: Dictionary mapping anagram keys to string lists
            
        Returns:
            List of lists containing grouped anagrams
        """
        return list(anagram_groups.values())