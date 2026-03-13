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
            
        job_count = len(startTime)
        jobs = self._create_sorted_jobs(startTime, endTime, profit)
        
        # dp[i] represents max profit from jobs[i:] onwards
        dynamic_programming_table = [0] * (job_count + 1)
        
        # Fill DP table from right to left
        for current_job_index in range(job_count - 1, -1, -1):
            current_job = jobs[current_job_index]
            
            # Option 1: Skip current job
            profit_without_current = dynamic_programming_table[current_job_index + 1]
            
            # Option 2: Take current job + best profit from non-overlapping jobs
            next_compatible_job_index = self._find_next_compatible_job(jobs, current_job_index)
            profit_with_current = current_job.profit + dynamic_programming_table[next_compatible_job_index]
            
            # Take maximum of both options
            dynamic_programming_table[current_job_index] = max(profit_without_current, profit_with_current)
        
        return dynamic_programming_table[0]
    
    def _create_sorted_jobs(self, startTime: List[int], endTime: List[int], profit: List[int]) -> List['Job']:
        """
        Create Job objects and sort by end time for optimal DP processing.
        
        Args:
            startTime: List of job start times
            endTime: List of job end times
            profit: List of job profits
            
        Returns:
            List of Job objects sorted by end time
        """
        jobs = []
        for start, end, prof in zip(startTime, endTime, profit):
            jobs.append(self.Job(start, end, prof))
        
        # Sort by end time to enable efficient binary search
        jobs.sort(key=lambda job: job.end_time)
        return jobs
    
    def _find_next_compatible_job(self, jobs: List['Job'], current_job_index: int) -> int:
        """
        Find the next job that doesn't overlap with the current job using binary search.
        
        Args:
            jobs: List of jobs sorted by end time
            current_job_index: Index of current job
            
        Returns:
            Index of next compatible job, or len(jobs) if none found
        """
        current_job_end_time = jobs[current_job_index].end_time
        
        # Extract start times for binary search
        start_times = [job.start_time for job in jobs[current_job_index + 1:]]
        
        # Find first job that starts at or after current job ends
        compatible_job_offset = bisect.bisect_left(start_times, current_job_end_time)
        
        return current_job_index + 1 + compatible_job_offset
    
    class Job:
        """Represents a job with start time, end time, and profit."""
        
        def __init__(self, start_time: int, end_time: int, profit: int):
            """
            Initialize a job.
            
            Args:
                start_time: Job start time
                end_time: Job end time
                profit: Job profit value
            """
            self.start_time = start_time
            self.end_time = end_time
            self.profit = profit