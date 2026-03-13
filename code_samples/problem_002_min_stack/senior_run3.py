from typing import Optional

class MinStack:
    """A stack data structure that supports retrieving the minimum element in O(1) time.
    
    This implementation uses two stacks: one for the actual values and another
    to keep track of the minimum values at each level.
    """
    
    def __init__(self) -> None:
        """Initialize the MinStack with empty stacks."""
        self.main_stack: list[int] = []
        self.min_stack: list[int] = []
    
    def push(self, val: int) -> None:
        """Push element val onto stack.
        
        Args:
            val: The integer value to push onto the stack.
        """
        self.main_stack.append(val)
        
        # Push current minimum onto min_stack
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        """Remove the element on the top of the stack.
        
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.main_stack:
            raise IndexError("Cannot pop from empty stack")
        
        popped_value = self.main_stack.pop()
        
        # Remove from min_stack if it was the minimum
        if self.min_stack and popped_value == self.min_stack[-1]:
            self.min_stack.pop()
    
    def top(self) -> int:
        """Get the top element of the stack.
        
        Returns:
            The top element of the stack.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.main_stack:
            raise IndexError("Cannot get top of empty stack")
        
        return self.main_stack[-1]
    
    def getMin(self) -> int:
        """Retrieve the minimum element in the stack.
        
        Returns:
            The minimum element currently in the stack.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.min_stack:
            raise IndexError("Cannot get minimum of empty stack")
        
        return self.min_stack[-1]