import heapq
from typing import Union


class MedianFinder:
    """
    Data structure to find median from a stream of integers.
    
    Uses two heaps: a max heap for smaller half and min heap for larger half.
    Maintains balance such that heaps differ by at most 1 element.
    """
    
    def __init__(self) -> None:
        """Initialize the MedianFinder data structure."""
        self.small_half = []  # max heap (negated values)
        self.large_half = []  # min heap
    
    def addNum(self, num: int) -> None:
        """
        Add a number to the data structure.
        
        Args:
            num: Integer to add to the stream
        """
        # Always add to small_half first (as max heap using negated values)
        heapq.heappush(self.small_half, -num)
        
        # Ensure max of small_half <= min of large_half
        if (self.small_half and self.large_half and 
            -self.small_half[0] > self.large_half[0]):
            max_from_small = -heapq.heappop(self.small_half)
            heapq.heappush(self.large_half, max_from_small)
        
        # Balance the heaps - small_half can have at most 1 extra element
        if len(self.small_half) > len(self.large_half) + 1:
            max_from_small = -heapq.heappop(self.small_half)
            heapq.heappush(self.large_half, max_from_small)
        elif len(self.large_half) > len(self.small_half) + 1:
            min_from_large = heapq.heappop(self.large_half)
            heapq.heappush(self.small_half, -min_from_large)
    
    def findMedian(self) -> Union[int, float]:
        """
        Find the median of all elements added so far.
        
        Returns:
            The median value as float or int
            
        Raises:
            ValueError: If no numbers have been added
        """
        if not self.small_half and not self.large_half:
            raise ValueError("No numbers in stream")
        
        # If odd number of elements, return from the larger heap
        if len(self.small_half) > len(self.large_half):
            return float(-self.small_half[0])
        elif len(self.large_half) > len(self.small_half):
            return float(self.large_half[0])
        else:
            # Even number of elements, return average of both tops
            small_max = -self.small_half[0]
            large_min = self.large_half[0]
            return (small_max + large_min) / 2.0