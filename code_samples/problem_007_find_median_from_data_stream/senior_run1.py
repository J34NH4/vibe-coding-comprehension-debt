import heapq
from typing import Union

class MedianFinder:
    """
    Data structure to find median from a stream of integers.
    
    Uses two heaps: a max heap for the smaller half and a min heap for the larger half.
    Maintains the invariant that the max heap size is either equal to or one more than
    the min heap size.
    """
    
    def __init__(self) -> None:
        """Initialize the MedianFinder data structure."""
        self.small_half = []  # max heap (negated values for Python's min heap)
        self.large_half = []  # min heap
    
    def addNum(self, num: int) -> None:
        """
        Add a number to the data structure.
        
        Args:
            num: The integer to add to the data stream.
        """
        # Always add to small_half first (as negative for max heap behavior)
        heapq.heappush(self.small_half, -num)
        
        # Move the largest from small_half to large_half to maintain order
        if self.small_half and self.large_half and (-self.small_half[0] > self.large_half[0]):
            transferred_value = -heapq.heappop(self.small_half)
            heapq.heappush(self.large_half, transferred_value)
        
        # Balance the heaps - small_half can have at most one more element
        if len(self.small_half) > len(self.large_half) + 1:
            transferred_value = -heapq.heappop(self.small_half)
            heapq.heappush(self.large_half, transferred_value)
        elif len(self.large_half) > len(self.small_half):
            transferred_value = heapq.heappop(self.large_half)
            heapq.heappush(self.small_half, -transferred_value)
    
    def findMedian(self) -> float:
        """
        Find the median of all numbers added so far.
        
        Returns:
            The median value as a float.
            
        Raises:
            ValueError: If no numbers have been added to the data structure.
        """
        if not self.small_half and not self.large_half:
            raise ValueError("No numbers available to find median")
        
        # If odd number of elements, median is the top of small_half
        if len(self.small_half) > len(self.large_half):
            return float(-self.small_half[0])
        
        # If even number of elements, median is average of both heap tops
        small_max = -self.small_half[0]
        large_min = self.large_half[0]
        return (small_max + large_min) / 2.0