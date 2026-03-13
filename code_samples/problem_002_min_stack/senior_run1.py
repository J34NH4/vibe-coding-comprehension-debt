from typing import Optional

class MinStack:
    """
    A stack data structure that supports retrieving the minimum element in O(1) time.
    
    Uses an auxiliary stack to track minimum values at each level of the main stack.
    """
    
    def __init__(self) -> None:
        """Initialize the MinStack with empty main and minimum tracking stacks."""
        self.main_stack = []  # Main stack to store all elements
        self.min_stack = []   # Auxiliary stack to track minimum at each level
    
    def push(self, val: int) -> None:
        """
        Push an element onto the stack and update minimum tracking.
        
        Args:
            val: The integer value to push onto the stack
        """
        self.main_stack.append(val)
        
        # Update minimum stack with current minimum
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        """
        Remove the top element from the stack and update minimum tracking.
        
        Raises:
            IndexError: If stack is empty
        """
        if not self.main_stack:
            raise IndexError("Cannot pop from empty stack")
        
        popped_value = self.main_stack.pop()
        
        # Remove from min stack if it was the current minimum
        if self.min_stack and popped_value == self.min_stack[-1]:
            self.min_stack.pop()
    
    def top(self) -> int:
        """
        Get the top element of the stack without removing it.
        
        Returns:
            The top element of the stack
            
        Raises:
            IndexError: If stack is empty
        """
        if not self.main_stack:
            raise IndexError("Stack is empty")
        
        return self.main_stack[-1]
    
    def getMin(self) -> int:
        """
        Retrieve the minimum element in the stack in O(1) time.
        
        Returns:
            The minimum element currently in the stack
            
        Raises:
            IndexError: If stack is empty
        """
        if not self.min_stack:
            raise IndexError("Stack is empty")
        
        return self.min_stack[-1]