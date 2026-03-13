from heapq import heappush, heappop
from typing import Optional


class MedianFinder:
    """
    Data structure to find median from a stream of integers.
    
    Uses two heaps to maintain the median efficiently:
    - max_heap: stores the smaller half of numbers
    - min_heap: stores the larger half of numbers
    """
    
    def __init__(self) -> None:
        """Initialize the MedianFinder data structure."""
        self.max_heap = []  # stores smaller half (negated for max behavior)
        self.min_heap = []  # stores larger half
    
    def addNum(self, num: int) -> None:
        """
        Add a number to the data structure.
        
        Args:
            num: Integer to add to the stream
        """
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
    
    def findMedian(self) -> float:
        """
        Find the median of all numbers added so far.
        
        Returns:
            The median as a float
            
        Raises:
            ValueError: If no numbers have been added
        """
        if not self.max_heap and not self.min_heap:
            raise ValueError("No numbers available to find median")
        
        total_elements = len(self.max_heap) + len(self.min_heap)
        
        # If odd number of elements, median is top of max_heap
        if total_elements % 2 == 1:
            return float(-self.max_heap[0])
        
        # If even number of elements, median is average of both heap tops
        smaller_half_max = -self.max_heap[0]
        larger_half_min = self.min_heap[0]
        return (smaller_half_max + larger_half_min) / 2.0