from typing import List, Tuple
import bisect

class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        """
        Find the maximum profit from scheduling non-overlapping jobs.
        
        Args:
            startTime: List of job start times
            endTime: List of job end times  
            profit: List of job profits
            
        Returns:
            Maximum profit achievable from non-overlapping jobs
        """
        if not startTime or not endTime or not profit:
            return 0
            
        number_of_jobs = len(startTime)
        jobs = self._create_job_list(startTime, endTime, profit)
        jobs.sort(key=lambda job: job[1])  # Sort by end time
        
        # Extract sorted end times for binary search
        sorted_end_times = [job[1] for job in jobs]
        
        # Dynamic programming array: dp[i] = max profit using jobs 0 to i
        max_profit_dp = [0] * number_of_jobs
        max_profit_dp[0] = jobs[0][2]  # First job profit
        
        for current_job_index in range(1, number_of_jobs):
            current_job_start, current_job_end, current_job_profit = jobs[current_job_index]
            
            # Find latest non-overlapping job
            latest_compatible_index = self._find_latest_compatible_job(
                sorted_end_times, current_job_start, current_job_index
            )
            
            # Calculate profit including current job
            profit_with_current = current_job_profit
            if latest_compatible_index != -1:
                profit_with_current += max_profit_dp[latest_compatible_index]
            
            # Take maximum of including or excluding current job
            max_profit_dp[current_job_index] = max(
                max_profit_dp[current_job_index - 1],  # Exclude current job
                profit_with_current  # Include current job
            )
        
        return max_profit_dp[number_of_jobs - 1]
    
    def _create_job_list(self, startTime: List[int], endTime: List[int], profit: List[int]) -> List[Tuple[int, int, int]]:
        """
        Create list of job tuples from separate arrays.
        
        Args:
            startTime: List of job start times
            endTime: List of job end times
            profit: List of job profits
            
        Returns:
            List of (start_time, end_time, profit) tuples
        """
        return list(zip(startTime, endTime, profit))
    
    def _find_latest_compatible_job(self, sorted_end_times: List[int], target_start_time: int, current_index: int) -> int:
        """
        Find the latest job that ends before or at target_start_time.
        
        Args:
            sorted_end_times: List of end times sorted in ascending order
            target_start_time: Start time of current job
            current_index: Current job index (exclusive upper bound)
            
        Returns:
            Index of latest compatible job, or -1 if none found
        """
        # Search only in jobs before current job
        search_space = sorted_end_times[:current_index]
        
        # Find rightmost position where end_time <= target_start_time
        insertion_point = bisect.bisect_right(search_space, target_start_time)
        
        return insertion_point - 1 if insertion_point > 0 else -1