from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        """
        Find the median of two sorted arrays in O(log(m+n)) time complexity.
        
        Args:
            nums1: First sorted array
            nums2: Second sorted array
            
        Returns:
            The median value as a float
            
        Raises:
            ValueError: If both arrays are empty
        """
        if not nums1 and not nums2:
            raise ValueError("Both arrays cannot be empty")
            
        # Ensure nums1 is the smaller array for optimization
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
            
        return self._binary_search_median(nums1, nums2)
    
    def _binary_search_median(self, smaller_array: List[int], larger_array: List[int]) -> float:
        """
        Use binary search to find the median by partitioning both arrays.
        
        Args:
            smaller_array: The array with fewer elements
            larger_array: The array with more elements
            
        Returns:
            The median value as a float
        """
        array1_length = len(smaller_array)
        array2_length = len(larger_array)
        total_length = array1_length + array2_length
        half_length = total_length // 2
        
        left_boundary = 0
        right_boundary = array1_length
        
        while left_boundary <= right_boundary:
            partition1 = (left_boundary + right_boundary) // 2  # Partition point in array1
            partition2 = half_length - partition1  # Corresponding partition in array2
            
            # Get boundary values for comparison
            max_left1 = float('-inf') if partition1 == 0 else smaller_array[partition1 - 1]
            min_right1 = float('inf') if partition1 == array1_length else smaller_array[partition1]
            
            max_left2 = float('-inf') if partition2 == 0 else larger_array[partition2 - 1]
            min_right2 = float('inf') if partition2 == array2_length else larger_array[partition2]
            
            # Check if we found the correct partition
            if max_left1 <= min_right2 and max_left2 <= min_right1:
                return self._calculate_median(max_left1, max_left2, min_right1, min_right2, total_length)
            elif max_left1 > min_right2:
                right_boundary = partition1 - 1  # Move partition1 left
            else:
                left_boundary = partition1 + 1  # Move partition1 right
                
        raise RuntimeError("Unable to find median - arrays may not be sorted")
    
    def _calculate_median(self, max_left1: float, max_left2: float, 
                         min_right1: float, min_right2: float, total_length: int) -> float:
        """
        Calculate the median based on the partition boundary values.
        
        Args:
            max_left1: Maximum value on left side of partition in array1
            max_left2: Maximum value on left side of partition in array2
            min_right1: Minimum value on right side of partition in array1
            min_right2: Minimum value on right side of partition in array2
            total_length: Combined length of both arrays
            
        Returns:
            The calculated median value
        """
        if total_length % 2 == 1:
            # Odd total length - median is the minimum of right side
            return min(min_right1, min_right2)
        else:
            # Even total length - median is average of max left and min right
            max_of_left = max(max_left1, max_left2)
            min_of_right = min(min_right1, min_right2)
            return (max_of_left + min_of_right) / 2.0