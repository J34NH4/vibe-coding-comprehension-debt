from typing import Optional

class MinStack:
    """
    A stack data structure that supports push, pop, top, and getMin operations in O(1) time.
    
    Uses two stacks: one for actual values and another to track minimum values.
    """
    
    def __init__(self) -> None:
        """Initialize the MinStack with empty stacks."""
        self.main_stack = []  # Main stack to store all values
        self.min_stack = []   # Stack to track minimum values
    
    def push(self, val: int) -> None:
        """
        Push an element onto the stack.
        
        Args:
            val: The integer value to push onto the stack.
        """
        self.main_stack.append(val)
        
        # Push to min_stack if it's empty or val is <= current minimum
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        """
        Remove the element on the top of the stack.
        
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.main_stack:
            raise IndexError("pop from empty stack")
        
        popped_value = self.main_stack.pop()
        
        # Remove from min_stack if the popped value was the current minimum
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
            raise IndexError("top from empty stack")
        
        return self.main_stack[-1]
    
    def getMin(self) -> int:
        """
        Retrieve the minimum element in the stack.
        
        Returns:
            The minimum element in the stack.
            
        Raises:
            IndexError: If the stack is empty.
        """
        if not self.min_stack:
            raise IndexError("getMin from empty stack")
        
        return self.min_stack[-1]