from typing import Optional, List

class MinStack:
    """
    A stack data structure that supports retrieving the minimum element in O(1) time.
    
    Uses an auxiliary stack to keep track of minimum values at each level.
    """
    
    def __init__(self) -> None:
        """Initialize the MinStack with empty main and minimum stacks."""
        self._main_stack: List[int] = []  # Main stack to store all elements
        self._min_stack: List[int] = []   # Auxiliary stack to track minimums
    
    def push(self, value: int) -> None:
        """
        Push an element onto the stack.
        
        Args:
            value: The integer value to push onto the stack.
        """
        self._main_stack.append(value)
        
        # Push to min_stack if it's empty or current value is <= current minimum
        if not self._min_stack or value <= self._min_stack[-1]:
            self._min_stack.append(value)
    
    def pop(self) -> None:
        """
        Remove the top element from the stack.
        
        Raises:
            IndexError: If the stack is empty.
        """
        if not self._main_stack:
            raise IndexError("Cannot pop from empty stack")
        
        popped_value = self._main_stack.pop()
        
        # Remove from min_stack if the popped value was the current minimum
        if self._min_stack and popped_value == self._min_stack[-1]:
            self._min_stack.pop()
    
    def top(self) -> int:
        """
        Get the top element of the stack without removing it.
        
        Returns:
            The top element of the stack.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if not self._main_stack:
            raise IndexError("Cannot get top of empty stack")
        
        return self._main_stack[-1]
    
    def getMin(self) -> int:
        """
        Retrieve the minimum element in the stack in O(1) time.
        
        Returns:
            The minimum element currently in the stack.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if not self._min_stack:
            raise IndexError("Cannot get minimum of empty stack")
        
        return self._min_stack[-1]