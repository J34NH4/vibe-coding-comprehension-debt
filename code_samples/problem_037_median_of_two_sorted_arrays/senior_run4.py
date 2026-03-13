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
        half_length = (total_length + 1) // 2  # Account for odd/even total length
        
        left_boundary = 0
        right_boundary = array1_length
        
        while left_boundary <= right_boundary:
            partition1 = (left_boundary + right_boundary) // 2
            partition2 = half_length - partition1
            
            # Get boundary elements for comparison
            max_left1 = self._get_max_left_element(smaller_array, partition1)
            min_right1 = self._get_min_right_element(smaller_array, partition1)
            max_left2 = self._get_max_left_element(larger_array, partition2)
            min_right2 = self._get_min_right_element(larger_array, partition2)
            
            # Check if we found the correct partition
            if max_left1 <= min_right2 and max_left2 <= min_right1:
                return self._calculate_median(max_left1, max_left2, min_right1, min_right2, total_length)
            elif max_left1 > min_right2:
                right_boundary = partition1 - 1  # Move left in first array
            else:
                left_boundary = partition1 + 1  # Move right in first array
                
        raise RuntimeError("Unable to find median - arrays may not be sorted")
    
    def _get_max_left_element(self, array: List[int], partition_index: int) -> int:
        """
        Get the maximum element on the left side of the partition.
        
        Args:
            array: The array to partition
            partition_index: Index where partition occurs
            
        Returns:
            Maximum element on left side, or negative infinity if no elements
        """
        return float('-inf') if partition_index == 0 else array[partition_index - 1]
    
    def _get_min_right_element(self, array: List[int], partition_index: int) -> int:
        """
        Get the minimum element on the right side of the partition.
        
        Args:
            array: The array to partition
            partition_index: Index where partition occurs
            
        Returns:
            Minimum element on right side, or positive infinity if no elements
        """
        return float('inf') if partition_index == len(array) else array[partition_index]
    
    def _calculate_median(self, max_left1: int, max_left2: int, 
                         min_right1: int, min_right2: int, total_length: int) -> float:
        """
        Calculate the median based on the partition boundary elements.
        
        Args:
            max_left1: Maximum element on left of first array partition
            max_left2: Maximum element on left of second array partition
            min_right1: Minimum element on right of first array partition
            min_right2: Minimum element on right of second array partition
            total_length: Combined length of both arrays
            
        Returns:
            The calculated median value
        """
        if total_length % 2 == 1:
            # Odd total length - median is the max of left elements
            return float(max(max_left1, max_left2))
        else:
            # Even total length - median is average of middle two elements
            left_median = max(max_left1, max_left2)
            right_median = min(min_right1, min_right2)
            return (left_median + right_median) / 2.0