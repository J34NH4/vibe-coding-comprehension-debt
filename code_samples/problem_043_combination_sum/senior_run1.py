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
        result_combinations = []
        
        def backtrack_combinations(current_combination: List[int], remaining_target: int, start_index: int) -> None:
            """
            Recursively find combinations using backtracking.
            
            Args:
                current_combination: Current combination being built
                remaining_target: Remaining sum needed to reach target
                start_index: Index to start searching from to avoid duplicates
            """
            # Base case: found valid combination
            if remaining_target == 0:
                result_combinations.append(current_combination[:])  # Create copy
                return
            
            # Base case: exceeded target or no more candidates
            if remaining_target < 0:
                return
            
            # Try each candidate starting from start_index
            for current_index in range(start_index, len(candidates)):
                current_candidate = candidates[current_index]
                
                # Skip if candidate is larger than remaining target
                if current_candidate > remaining_target:
                    continue
                
                # Include current candidate in combination
                current_combination.append(current_candidate)
                
                # Recursively search with updated target and same start_index (allow reuse)
                backtrack_combinations(
                    current_combination, 
                    remaining_target - current_candidate, 
                    current_index
                )
                
                # Backtrack: remove current candidate
                current_combination.pop()
        
        # Handle edge cases
        if not candidates or target <= 0:
            return result_combinations
        
        # Sort candidates for potential optimization
        candidates.sort()
        
        # Start backtracking
        backtrack_combinations([], target, 0)
        
        return result_combinations