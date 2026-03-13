from heapq import heappush, heappop
from typing import Union


class MedianFinder:
    """
    A data structure that efficiently finds the median from a stream of integers.
    
    Uses two heaps to maintain the median:
    - max_heap: stores the smaller half of numbers (using negative values for max behavior)
    - min_heap: stores the larger half of numbers
    """
    
    def __init__(self) -> None:
        """Initialize the MedianFinder with two empty heaps."""
        self.max_heap = []  # stores smaller half (negated for max heap behavior)
        self.min_heap = []  # stores larger half
    
    def addNum(self, num: int) -> None:
        """
        Add a number to the data structure.
        
        Args:
            num: The integer to add to the data stream
            
        Raises:
            TypeError: If num is not an integer
        """
        if not isinstance(num, int):
            raise TypeError("Input must be an integer")
            
        # Always add to max_heap first (smaller half)
        heappush(self.max_heap, -num)
        
        # Move the largest from max_heap to min_heap to maintain order
        if self.max_heap:
            largest_from_smaller_half = -heappop(self.max_heap)
            heappush(self.min_heap, largest_from_smaller_half)
        
        # Balance the heaps - max_heap should have at most one more element
        if len(self.min_heap) > len(self.max_heap):
            smallest_from_larger_half = heappop(self.min_heap)
            heappush(self.max_heap, -smallest_from_larger_half)

    def findMedian(self) -> Union[int, float]:
        """
        Find the median of all numbers added so far.
        
        Returns:
            The median value as an integer or float
            
        Raises:
            ValueError: If no numbers have been added
        """
        total_elements = len(self.max_heap) + len(self.min_heap)
        
        if total_elements == 0:
            raise ValueError("Cannot find median of empty data stream")
        
        # If odd number of elements, median is the top of max_heap
        if len(self.max_heap) > len(self.min_heap):
            return float(-self.max_heap[0])
        
        # If even number of elements, median is average of both heap tops
        smaller_half_max = -self.max_heap[0]
        larger_half_min = self.min_heap[0]
        return (smaller_half_max + larger_half_min) / 2.0