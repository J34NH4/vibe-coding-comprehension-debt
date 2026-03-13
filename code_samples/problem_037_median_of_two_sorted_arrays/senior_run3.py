from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        """
        Find the median of two sorted arrays in O(log(min(m,n))) time.
        
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
        Perform binary search to find the optimal partition point.
        
        Args:
            smaller_array: The smaller of the two arrays
            larger_array: The larger of the two arrays
            
        Returns:
            The median value as a float
        """
        array1_length = len(smaller_array)
        array2_length = len(larger_array)
        total_length = array1_length + array2_length
        half_length = (total_length + 1) // 2  # +1 handles odd length case
        
        left_boundary = 0
        right_boundary = array1_length
        
        while left_boundary <= right_boundary:
            partition1 = (left_boundary + right_boundary) // 2  # Partition point in nums1
            partition2 = half_length - partition1  # Corresponding partition in nums2
            
            # Get boundary elements for comparison
            max_left1 = self._get_left_boundary_value(smaller_array, partition1)
            min_right1 = self._get_right_boundary_value(smaller_array, partition1)
            max_left2 = self._get_left_boundary_value(larger_array, partition2)
            min_right2 = self._get_right_boundary_value(larger_array, partition2)
            
            # Check if we found the correct partition
            if max_left1 <= min_right2 and max_left2 <= min_right1:
                return self._calculate_median(max_left1, max_left2, min_right1, min_right2, total_length)
            elif max_left1 > min_right2:
                right_boundary = partition1 - 1  # Move partition1 left
            else:
                left_boundary = partition1 + 1  # Move partition1 right
        
        raise ValueError("Unable to find median - invalid input arrays")
    
    def _get_left_boundary_value(self, array: List[int], partition_index: int) -> int:
        """
        Get the maximum value on the left side of the partition.
        
        Args:
            array: The array to get boundary from
            partition_index: The partition point
            
        Returns:
            The left boundary value or negative infinity if no elements
        """
        return float('-inf') if partition_index == 0 else array[partition_index - 1]
    
    def _get_right_boundary_value(self, array: List[int], partition_index: int) -> int:
        """
        Get the minimum value on the right side of the partition.
        
        Args:
            array: The array to get boundary from
            partition_index: The partition point
            
        Returns:
            The right boundary value or positive infinity if no elements
        """
        return float('inf') if partition_index == len(array) else array[partition_index]
    
    def _calculate_median(self, max_left1: int, max_left2: int, 
                         min_right1: int, min_right2: int, total_length: int) -> float:
        """
        Calculate the median based on the partition boundary values.
        
        Args:
            max_left1: Maximum value on left side of first array partition
            max_left2: Maximum value on left side of second array partition
            min_right1: Minimum value on right side of first array partition
            min_right2: Minimum value on right side of second array partition
            total_length: Total length of both arrays combined
            
        Returns:
            The calculated median value
        """
        if total_length % 2 == 1:
            # Odd total length - median is the max of left side
            return float(max(max_left1, max_left2))
        else:
            # Even total length - median is average of middle two elements
            left_median = max(max_left1, max_left2)
            right_median = min(min_right1, min_right2)
            return (left_median + right_median) / 2.0