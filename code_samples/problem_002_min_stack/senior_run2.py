from typing import Optional, List, Tuple

class MinStack:
    """
    A stack data structure that supports push, pop, top, and getMin operations in O(1) time.
    
    Uses an auxiliary stack to keep track of minimum values at each level.
    """
    
    def __init__(self) -> None:
        """Initialize the MinStack with empty main and minimum stacks."""
        self.main_stack: List[int] = []
        self.min_stack: List[int] = []  # Stores minimum value at each level
    
    def push(self, value: int) -> None:
        """
        Push an element onto the stack.
        
        Args:
            value: The integer value to push onto the stack.
        """
        self.main_stack.append(value)
        
        # Update minimum stack with current minimum
        if not self.min_stack or value <= self.min_stack[-1]:
            self.min_stack.append(value)
    
    def pop(self) -> None:
        """
        Remove the element on the top of the stack.
        
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.main_stack:
            raise IndexError("Cannot pop from empty stack")
        
        popped_value = self.main_stack.pop()
        
        # Remove from min_stack if it was the current minimum
        if self.min_stack and popped_value == self.min_stack[-1]:
            self.min_stack.pop()
    
    def top(self) -> int:
        """
        Get the top element of the stack.
        
        Returns:
            The top element of the stack.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.main_stack:
            raise IndexError("Cannot get top of empty stack")
        
        return self.main_stack[-1]
    
    def getMin(self) -> int:
        """
        Retrieve the minimum element in the stack in constant time.
        
        Returns:
            The minimum element currently in the stack.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.min_stack:
            raise IndexError("Cannot get minimum of empty stack")
        
        return self.min_stack[-1]