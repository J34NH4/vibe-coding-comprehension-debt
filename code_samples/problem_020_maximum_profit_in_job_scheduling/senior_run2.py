from typing import List
import bisect

class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        """
        Find the maximum profit from non-overlapping jobs using dynamic programming.
        
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
        job_list = self._create_sorted_jobs(startTime, endTime, profit)
        
        # dp[i] represents max profit from jobs 0 to i
        dynamic_programming_table = [0] * number_of_jobs
        dynamic_programming_table[0] = job_list[0][2]  # First job profit
        
        for current_job_index in range(1, number_of_jobs):
            current_job_profit = job_list[current_job_index][2]
            
            # Find latest non-overlapping job
            latest_compatible_job_index = self._find_latest_compatible_job(
                job_list, current_job_index
            )
            
            # Calculate profit including current job
            profit_with_current_job = current_job_profit
            if latest_compatible_job_index != -1:
                profit_with_current_job += dynamic_programming_table[latest_compatible_job_index]
            
            # Take maximum of including or excluding current job
            dynamic_programming_table[current_job_index] = max(
                dynamic_programming_table[current_job_index - 1],  # Exclude current job
                profit_with_current_job  # Include current job
            )
        
        return dynamic_programming_table[number_of_jobs - 1]
    
    def _create_sorted_jobs(self, startTime: List[int], endTime: List[int], profit: List[int]) -> List[tuple]:
        """
        Create and sort jobs by end time for optimal scheduling.
        
        Args:
            startTime: List of job start times
            endTime: List of job end times
            profit: List of job profits
            
        Returns:
            List of tuples (start_time, end_time, profit) sorted by end_time
        """
        job_list = list(zip(startTime, endTime, profit))
        job_list.sort(key=lambda job: job[1])  # Sort by end time
        return job_list
    
    def _find_latest_compatible_job(self, job_list: List[tuple], current_job_index: int) -> int:
        """
        Find the latest job that doesn't overlap with the current job using binary search.
        
        Args:
            job_list: List of jobs sorted by end time
            current_job_index: Index of current job being considered
            
        Returns:
            Index of latest compatible job, or -1 if none found
        """
        current_job_start_time = job_list[current_job_index][0]
        
        # Extract end times for binary search
        end_times = [job[1] for job in job_list[:current_job_index]]
        
        # Find rightmost position where end_time <= current_start_time
        compatible_job_index = bisect.bisect_right(end_times, current_job_start_time) - 1
        
        return compatible_job_index if compatible_job_index >= 0 else -1