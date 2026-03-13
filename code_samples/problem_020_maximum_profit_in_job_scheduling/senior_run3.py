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
            
        return self._calculate_maximum_profit(startTime, endTime, profit)
    
    def _calculate_maximum_profit(self, start_times: List[int], end_times: List[int], profits: List[int]) -> int:
        """
        Calculate maximum profit using dynamic programming with binary search optimization.
        
        Args:
            start_times: List of job start times
            end_times: List of job end times
            profits: List of job profits
            
        Returns:
            Maximum achievable profit
        """
        job_count = len(start_times)
        
        # Create jobs list and sort by end time
        jobs_list = self._create_and_sort_jobs(start_times, end_times, profits)
        
        # Extract sorted end times for binary search
        sorted_end_times = [job[1] for job in jobs_list]
        
        # DP array where dp[i] represents max profit using jobs 0 to i
        dynamic_programming_array = [0] * job_count
        dynamic_programming_array[0] = jobs_list[0][2]  # First job profit
        
        for current_job_index in range(1, job_count):
            current_job_start, current_job_end, current_job_profit = jobs_list[current_job_index]
            
            # Profit including current job
            profit_with_current_job = current_job_profit
            
            # Find latest non-overlapping job using binary search
            latest_compatible_job_index = self._find_latest_compatible_job(
                sorted_end_times, current_job_start, current_job_index
            )
            
            if latest_compatible_job_index != -1:
                profit_with_current_job += dynamic_programming_array[latest_compatible_job_index]
            
            # Profit excluding current job
            profit_without_current_job = dynamic_programming_array[current_job_index - 1]
            
            # Take maximum of including or excluding current job
            dynamic_programming_array[current_job_index] = max(
                profit_with_current_job, 
                profit_without_current_job
            )
        
        return dynamic_programming_array[job_count - 1]
    
    def _create_and_sort_jobs(self, start_times: List[int], end_times: List[int], profits: List[int]) -> List[tuple]:
        """
        Create job tuples and sort them by end time.
        
        Args:
            start_times: List of job start times
            end_times: List of job end times
            profits: List of job profits
            
        Returns:
            List of job tuples sorted by end time
        """
        jobs_list = list(zip(start_times, end_times, profits))
        jobs_list.sort(key=lambda job_tuple: job_tuple[1])  # Sort by end time
        return jobs_list
    
    def _find_latest_compatible_job(self, sorted_end_times: List[int], target_start_time: int, current_index: int) -> int:
        """
        Find the latest job that ends before or at the target start time using binary search.
        
        Args:
            sorted_end_times: List of end times sorted in ascending order
            target_start_time: Start time of current job
            current_index: Current job index (exclusive upper bound)
            
        Returns:
            Index of latest compatible job, or -1 if none found
        """
        # Use bisect_right to find insertion point for target_start_time
        insertion_point = bisect.bisect_right(sorted_end_times, target_start_time, hi=current_index)
        
        # Return index of latest compatible job (insertion_point - 1)
        return insertion_point - 1 if insertion_point > 0 else -1