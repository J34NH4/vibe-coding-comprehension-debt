from typing import List


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Find all unique combinations in candidates where the candidate numbers sum to target.
        
        Args:
            candidates: List of distinct positive integers
            target: Target sum value
            
        Returns:
            List of all unique combinations that sum to target
        """
        if not candidates or target <= 0:
            return []
        
        result_combinations = []
        current_combination = []
        
        # Sort candidates for optimization
        candidates.sort()
        
        self._find_combinations(
            candidates=candidates,
            target=target,
            current_combination=current_combination,
            result_combinations=result_combinations,
            start_index=0
        )
        
        return result_combinations
    
    def _find_combinations(
        self,
        candidates: List[int],
        target: int,
        current_combination: List[int],
        result_combinations: List[List[int]],
        start_index: int
    ) -> None:
        """
        Recursive helper function to find all valid combinations using backtracking.
        
        Args:
            candidates: List of candidate numbers
            target: Remaining target sum
            current_combination: Current combination being built
            result_combinations: List to store all valid combinations
            start_index: Starting index to avoid duplicate combinations
        """
        # Base case: found valid combination
        if target == 0:
            result_combinations.append(current_combination[:])  # Add copy of current combination
            return
        
        # Explore all candidates starting from start_index
        for current_index in range(start_index, len(candidates)):
            current_candidate = candidates[current_index]
            
            # Pruning: if current candidate exceeds target, skip remaining candidates
            if current_candidate > target:
                break
            
            # Include current candidate in combination
            current_combination.append(current_candidate)
            
            # Recursively search with reduced target
            # Use current_index (not current_index + 1) to allow reuse of same number
            self._find_combinations(
                candidates=candidates,
                target=target - current_candidate,
                current_combination=current_combination,
                result_combinations=result_combinations,
                start_index=current_index
            )
            
            # Backtrack: remove current candidate
            current_combination.pop()