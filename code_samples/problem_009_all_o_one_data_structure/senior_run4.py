from typing import Optional

class Node:
    """Represents a node in the doubly linked list containing keys with the same count."""
    
    def __init__(self, count: int) -> None:
        """Initialize a node with given count.
        
        Args:
            count: The frequency count for keys in this node
        """
        self.count = count
        self.keys = set()  # Set of keys with this count
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class AllOne:
    """Data structure supporting O(1) increment, decrement, max and min operations."""
    
    def __init__(self) -> None:
        """Initialize the data structure with sentinel nodes."""
        self.key_to_node = {}  # Maps key to its current node
        
        # Create sentinel nodes for easier list manipulation
        self.head = Node(0)  # Dummy head with count 0
        self.tail = Node(float('inf'))  # Dummy tail with infinite count
        self.head.next = self.tail
        self.tail.prev = self.head

    def _insert_after(self, prev_node: Node, count: int) -> Node:
        """Insert a new node with given count after the specified node.
        
        Args:
            prev_node: Node after which to insert the new node
            count: Count value for the new node
            
        Returns:
            The newly created and inserted node
        """
        new_node = Node(count)
        new_node.prev = prev_node
        new_node.next = prev_node.next
        prev_node.next.prev = new_node
        prev_node.next = new_node
        return new_node

    def _remove_node(self, node: Node) -> None:
        """Remove a node from the doubly linked list.
        
        Args:
            node: The node to remove
        """
        node.prev.next = node.next
        node.next.prev = node.prev

    def inc(self, key: str) -> None:
        """Increment the count of the given key by 1.
        
        Args:
            key: The key to increment
        """
        if key not in self.key_to_node:
            # Key doesn't exist, add to count 1
            if self.head.next.count != 1:
                # Need to create a node with count 1
                self._insert_after(self.head, 1)
            
            self.head.next.keys.add(key)
            self.key_to_node[key] = self.head.next
        else:
            # Key exists, move to next count
            current_node = self.key_to_node[key]
            current_count = current_node.count
            new_count = current_count + 1
            
            # Remove key from current node
            current_node.keys.remove(key)
            
            # Find or create node for new count
            if current_node.next.count != new_count:
                # Need to create a new node for new_count
                next_node = self._insert_after(current_node, new_count)
            else:
                next_node = current_node.next
            
            next_node.keys.add(key)
            self.key_to_node[key] = next_node
            
            # Remove current node if it's empty
            if not current_node.keys:
                self._remove_node(current_node)

    def dec(self, key: str) -> None:
        """Decrement the count of the given key by 1.
        
        Args:
            key: The key to decrement
        """
        if key not in self.key_to_node:
            return  # Key doesn't exist, nothing to do
        
        current_node = self.key_to_node[key]
        current_count = current_node.count
        
        # Remove key from current node
        current_node.keys.remove(key)
        
        if current_count == 1:
            # Count becomes 0, remove key entirely
            del self.key_to_node[key]
        else:
            # Move to previous count
            new_count = current_count - 1
            
            # Find or create node for new count
            if current_node.prev.count != new_count:
                # Need to create a new node for new_count
                prev_node = self._insert_after(current_node.prev, new_count)
            else:
                prev_node = current_node.prev
            
            prev_node.keys.add(key)
            self.key_to_node[key] = prev_node
        
        # Remove current node if it's empty
        if not current_node.keys:
            self._remove_node(current_node)

    def getMaxKey(self) -> str:
        """Get any key with the maximum count.
        
        Returns:
            A key with maximum count, or empty string if no keys exist
        """
        if self.tail.prev == self.head:
            return ""  # No keys exist
        
        # Return any key from the node with maximum count
        return next(iter(self.tail.prev.keys))

    def getMinKey(self) -> str:
        """Get any key with the minimum count.
        
        Returns:
            A key with minimum count, or empty string if no keys exist
        """
        if self.head.next == self.tail:
            return ""  # No keys exist
        
        # Return any key from the node with minimum count
        return next(iter(self.head.next.keys))