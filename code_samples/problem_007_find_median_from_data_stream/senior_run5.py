from typing import List, Optional
import heapq

class MedianFinder:
    """
    Data structure to find median from a stream of integers.
    
    Uses two heaps to maintain the median efficiently:
    - max_heap: stores the smaller half of numbers (as negative values for max behavior)
    - min_heap: stores the larger half of numbers
    """
    
    def __init__(self) -> None:
        """Initialize the MedianFinder with two empty heaps."""
        self.max_heap: List[int] = []  # Stores smaller half (negated for max heap)
        self.min_heap: List[int] = []  # Stores larger half
    
    def addNum(self, num: int) -> None:
        """
        Add a number to the data structure.
        
        Args:
            num: Integer to add to the stream
        """
        # Always add to max_heap first (smaller half)
        heapq.heappush(self.max_heap, -num)
        
        # Move the largest from max_heap to min_heap to maintain order
        if self.max_heap:
            largest_from_smaller_half = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, largest_from_smaller_half)
        
        # Balance the heaps - max_heap should have at most one more element
        if len(self.min_heap) > len(self.max_heap):
            smallest_from_larger_half = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -smallest_from_larger_half)
    
    def findMedian(self) -> float:
        """
        Find the median of all numbers added so far.
        
        Returns:
            The median as a float value
            
        Raises:
            ValueError: If no numbers have been added
        """
        if not self.max_heap and not self.min_heap:
            raise ValueError("No numbers available to find median")
        
        # If max_heap has more elements, its top is the median
        if len(self.max_heap) > len(self.min_heap):
            return float(-self.max_heap[0])
        
        # Equal sizes - median is average of both tops
        smaller_half_max = -self.max_heap[0]
        larger_half_min = self.min_heap[0]
        return (smaller_half_max + larger_half_min) / 2.0