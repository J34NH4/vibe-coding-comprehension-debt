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
            
        first_array_length = len(nums1)
        second_array_length = len(nums2)
        total_length = first_array_length + second_array_length
        
        return self._binary_search_median(nums1, nums2, first_array_length, 
                                        second_array_length, total_length)
    
    def _binary_search_median(self, smaller_array: List[int], larger_array: List[int],
                            smaller_length: int, larger_length: int, 
                            total_length: int) -> float:
        """
        Perform binary search to find the median partition point.
        
        Args:
            smaller_array: The smaller of the two arrays
            larger_array: The larger of the two arrays
            smaller_length: Length of smaller array
            larger_length: Length of larger array
            total_length: Combined length of both arrays
            
        Returns:
            The median value
        """
        left_boundary = 0
        right_boundary = smaller_length
        
        while left_boundary <= right_boundary:
            # Partition point in smaller array
            smaller_partition = (left_boundary + right_boundary) // 2
            
            # Corresponding partition point in larger array
            larger_partition = (total_length + 1) // 2 - smaller_partition
            
            # Get boundary values for comparison
            left_max_smaller = self._get_left_max(smaller_array, smaller_partition)
            right_min_smaller = self._get_right_min(smaller_array, smaller_partition, smaller_length)
            
            left_max_larger = self._get_left_max(larger_array, larger_partition)
            right_min_larger = self._get_right_min(larger_array, larger_partition, larger_length)
            
            # Check if we found the correct partition
            if left_max_smaller <= right_min_larger and left_max_larger <= right_min_smaller:
                return self._calculate_median(left_max_smaller, right_min_smaller,
                                            left_max_larger, right_min_larger, total_length)
            
            # Adjust search boundaries based on comparison
            elif left_max_smaller > right_min_larger:
                right_boundary = smaller_partition - 1  # Move left in smaller array
            else:
                left_boundary = smaller_partition + 1  # Move right in smaller array
                
        raise RuntimeError("Unable to find median - this should not happen with valid input")
    
    def _get_left_max(self, array: List[int], partition_index: int) -> int:
        """
        Get the maximum value on the left side of the partition.
        
        Args:
            array: The array to examine
            partition_index: The partition point
            
        Returns:
            Maximum value on left side, or negative infinity if no elements
        """
        return float('-inf') if partition_index == 0 else array[partition_index - 1]
    
    def _get_right_min(self, array: List[int], partition_index: int, array_length: int) -> int:
        """
        Get the minimum value on the right side of the partition.
        
        Args:
            array: The array to examine
            partition_index: The partition point
            array_length: Length of the array
            
        Returns:
            Minimum value on right side, or positive infinity if no elements
        """
        return float('inf') if partition_index == array_length else array[partition_index]
    
    def _calculate_median(self, left_max_smaller: int, right_min_smaller: int,
                         left_max_larger: int, right_min_larger: int, 
                         total_length: int) -> float:
        """
        Calculate the median based on the partition boundary values.
        
        Args:
            left_max_smaller: Max value on left of smaller array partition
            right_min_smaller: Min value on right of smaller array partition
            left_max_larger: Max value on left of larger array partition
            right_min_larger: Min value on right of larger array partition
            total_length: Total length of combined arrays
            
        Returns:
            The median value
        """
        if total_length % 2 == 1:
            # Odd total length - median is max of left side
            return float(max(left_max_smaller, left_max_larger))
        else:
            # Even total length - median is average of middle two elements
            left_median = max(left_max_smaller, left_max_larger)
            right_median = min(right_min_smaller, right_min_larger)
            return (left_median + right_median) / 2.0