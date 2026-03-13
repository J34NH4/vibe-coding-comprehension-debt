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
            
        Raises:
            ValueError: If input lists have different lengths
        """
        if not startTime or not endTime or not profit:
            return 0
            
        if len(startTime) != len(endTime) or len(startTime) != len(profit):
            raise ValueError("All input lists must have the same length")
            
        number_of_jobs = len(startTime)
        
        # Create job tuples and sort by end time for optimal substructure
        jobs = list(zip(startTime, endTime, profit))
        jobs.sort(key=lambda job: job[1])  # Sort by end time
        
        # Extract sorted arrays for easier access
        sorted_start_times = [job[0] for job in jobs]
        sorted_end_times = [job[1] for job in jobs]
        sorted_profits = [job[2] for job in jobs]
        
        return self._calculate_maximum_profit(sorted_start_times, sorted_end_times, sorted_profits)
    
    def _calculate_maximum_profit(self, start_times: List[int], end_times: List[int], profits: List[int]) -> int:
        """
        Calculate maximum profit using dynamic programming with memoization.
        
        Args:
            start_times: Sorted list of start times
            end_times: Sorted list of end times
            profits: Corresponding profits for each job
            
        Returns:
            Maximum profit achievable
        """
        number_of_jobs = len(start_times)
        
        # dp[i] represents maximum profit considering jobs 0 to i
        dynamic_programming_table = [0] * number_of_jobs
        dynamic_programming_table[0] = profits[0]
        
        for current_job_index in range(1, number_of_jobs):
            # Profit if we include current job
            profit_including_current = profits[current_job_index]
            
            # Find the latest job that doesn't conflict with current job
            latest_non_conflicting_index = self._find_latest_non_conflicting_job(
                end_times, start_times[current_job_index], current_job_index
            )
            
            if latest_non_conflicting_index != -1:
                profit_including_current += dynamic_programming_table[latest_non_conflicting_index]
            
            # Profit if we exclude current job
            profit_excluding_current = dynamic_programming_table[current_job_index - 1]
            
            # Take maximum of including or excluding current job
            dynamic_programming_table[current_job_index] = max(
                profit_including_current, 
                profit_excluding_current
            )
        
        return dynamic_programming_table[number_of_jobs - 1]
    
    def _find_latest_non_conflicting_job(self, end_times: List[int], current_start_time: int, current_index: int) -> int:
        """
        Find the latest job that ends before or at the current job's start time.
        
        Args:
            end_times: List of job end times (sorted)
            current_start_time: Start time of current job
            current_index: Index of current job
            
        Returns:
            Index of latest non-conflicting job, or -1 if none exists
        """
        # Use binary search to find rightmost job that ends <= current_start_time
        search_end_times = end_times[:current_index]  # Only search previous jobs
        
        if not search_end_times:
            return -1
            
        # Find rightmost position where end_time <= current_start_time
        insertion_point = bisect.bisect_right(search_end_times, current_start_time)
        
        return insertion_point - 1 if insertion_point > 0 else -1