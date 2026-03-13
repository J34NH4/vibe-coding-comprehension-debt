from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find all unique combinations in candidates where the candidate numbers sum to target.
        
        Args:
            candidates: Array of distinct integers
            target: Target sum value
            
        Returns:
            List of all unique combinations that sum to target
        """
        if not candidates or target <= 0:
            return []
        
        result_combinations = []
        current_combination = []
        
        # Sort candidates to enable early termination optimization
        sorted_candidates = sorted(candidates)
        
        self._find_combinations(
            sorted_candidates, 
            target, 
            0, 
            current_combination, 
            result_combinations
        )
        
        return result_combinations
    
    def _find_combinations(
        self, 
        candidates: List[int], 
        remaining_target: int, 
        start_index: int, 
        current_combination: List[int], 
        result_combinations: List[List[int]]
    ) -> None:
        """
        Recursively find all valid combinations using backtracking.
        
        Args:
            candidates: Sorted array of candidate numbers
            remaining_target: Current remaining sum needed
            start_index: Starting index to avoid duplicate combinations
            current_combination: Current combination being built
            result_combinations: List to store all valid combinations
        """
        # Base case: found valid combination
        if remaining_target == 0:
            result_combinations.append(current_combination[:])  # Deep copy
            return
        
        # Early termination: remaining target is negative
        if remaining_target < 0:
            return
        
        for current_index in range(start_index, len(candidates)):
            current_candidate = candidates[current_index]
            
            # Early termination: candidate is larger than remaining target
            if current_candidate > remaining_target:
                break
            
            # Include current candidate in combination
            current_combination.append(current_candidate)
            
            # Recurse with same start_index to allow reusing same number
            self._find_combinations(
                candidates, 
                remaining_target - current_candidate, 
                current_index,  # Allow reusing current candidate
                current_combination, 
                result_combinations
            )
            
            # Backtrack: remove current candidate
            current_combination.pop()