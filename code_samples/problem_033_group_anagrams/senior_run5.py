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
            raise TypeError("Input must be a list")
        
        # Handle edge cases
        if not strs:
            return []
        
        return self._group_anagrams_by_sorted_key(strs)
    
    def _group_anagrams_by_sorted_key(self, string_list: List[str]) -> List[List[str]]:
        """
        Groups anagrams using sorted characters as the grouping key.
        
        Args:
            string_list: List of strings to process
            
        Returns:
            List of grouped anagrams
        """
        anagram_groups: Dict[str, List[str]] = defaultdict(list)
        
        for current_string in string_list:
            if not isinstance(current_string, str):
                raise TypeError("All elements must be strings")
            
            # Sort characters to create canonical form for anagram detection
            sorted_characters = ''.join(sorted(current_string))
            anagram_groups[sorted_characters].append(current_string)
        
        return list(anagram_groups.values())