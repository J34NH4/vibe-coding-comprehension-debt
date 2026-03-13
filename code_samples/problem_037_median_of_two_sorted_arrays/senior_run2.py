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
            return self.findMedianSortedArrays(nums2, nums1)
            
        first_array_length = len(nums1)
        second_array_length = len(nums2)
        total_length = first_array_length + second_array_length
        
        return self._binary_search_median(
            nums1, nums2, first_array_length, second_array_length, total_length
        )
    
    def _binary_search_median(
        self, 
        smaller_array: List[int], 
        larger_array: List[int],
        smaller_length: int,
        larger_length: int,
        total_length: int
    ) -> float:
        """
        Perform binary search to find the median partition point.
        
        Args:
            smaller_array: The smaller of the two arrays
            larger_array: The larger of the two arrays
            smaller_length: Length of smaller array
            larger_length: Length of larger array
            total_length: Combined length of both arrays
            
        Returns:
            The median value as a float
        """
        left_boundary = 0
        right_boundary = smaller_length
        
        while left_boundary <= right_boundary:
            # Partition points for both arrays
            smaller_partition = (left_boundary + right_boundary) // 2
            larger_partition = (total_length + 1) // 2 - smaller_partition
            
            # Elements on the left side of partition
            smaller_left_max = self._get_left_max(smaller_array, smaller_partition)
            larger_left_max = self._get_left_max(larger_array, larger_partition)
            
            # Elements on the right side of partition
            smaller_right_min = self._get_right_min(smaller_array, smaller_partition)
            larger_right_min = self._get_right_min(larger_array, larger_partition)
            
            # Check if we found the correct partition
            if smaller_left_max <= larger_right_min and larger_left_max <= smaller_right_min:
                return self._calculate_median(
                    smaller_left_max, larger_left_max,
                    smaller_right_min, larger_right_min,
                    total_length
                )
            elif smaller_left_max > larger_right_min:
                # Too many elements from smaller array on left side
                right_boundary = smaller_partition - 1
            else:
                # Too few elements from smaller array on left side
                left_boundary = smaller_partition + 1
                
        raise RuntimeError("Unable to find median - arrays may not be sorted")
    
    def _get_left_max(self, array: List[int], partition_index: int) -> float:
        """
        Get the maximum element on the left side of partition.
        
        Args:
            array: The array to check
            partition_index: Index of the partition
            
        Returns:
            Maximum element on left side, or negative infinity if no elements
        """
        return float('-inf') if partition_index == 0 else array[partition_index - 1]
    
    def _get_right_min(self, array: List[int], partition_index: int) -> float:
        """
        Get the minimum element on the right side of partition.
        
        Args:
            array: The array to check
            partition_index: Index of the partition
            
        Returns:
            Minimum element on right side, or positive infinity if no elements
        """
        return float('inf') if partition_index == len(array) else array[partition_index]
    
    def _calculate_median(
        self,
        smaller_left_max: float,
        larger_left_max: float,
        smaller_right_min: float,
        larger_right_min: float,
        total_length: int
    ) -> float:
        """
        Calculate the final median value based on partition elements.
        
        Args:
            smaller_left_max: Max element on left side of smaller array partition
            larger_left_max: Max element on left side of larger array partition
            smaller_right_min: Min element on right side of smaller array partition
            larger_right_min: Min element on right side of larger array partition
            total_length: Combined length of both arrays
            
        Returns:
            The calculated median value
        """
        if total_length % 2 == 1:
            # Odd total length - median is max of left side
            return max(smaller_left_max, larger_left_max)
        else:
            # Even total length - median is average of middle two elements
            left_median = max(smaller_left_max, larger_left_max)
            right_median = min(smaller_right_min, larger_right_min)
            return (left_median + right_median) / 2.0