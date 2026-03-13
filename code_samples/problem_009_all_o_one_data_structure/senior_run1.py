from collections import defaultdict
from typing import Optional

class Node:
    """Doubly linked list node containing count and set of keys with that count."""
    
    def __init__(self, count: int = 0) -> None:
        """Initialize node with given count.
        
        Args:
            count: The frequency count for this node
        """
        self.count = count
        self.keys = set()  # Keys that have this count
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class AllOne:
    """Data structure supporting O(1) increment, decrement, and min/max key operations."""
    
    def __init__(self) -> None:
        """Initialize the data structure with sentinel nodes."""
        self.key_to_count = defaultdict(int)  # Maps key to its current count
        self.count_to_node = {}  # Maps count to its node in linked list
        
        # Create sentinel nodes for easier list manipulation
        self.head = Node(0)  # Dummy head
        self.tail = Node(float('inf'))  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def inc(self, key: str) -> None:
        """Increment the count of the key by 1.
        
        Args:
            key: The key to increment
        """
        current_count = self.key_to_count[key]
        new_count = current_count + 1
        self.key_to_count[key] = new_count
        
        # Remove key from current count node if it exists
        if current_count > 0:
            current_node = self.count_to_node[current_count]
            current_node.keys.remove(key)
            if not current_node.keys:  # Remove empty node
                self._remove_node(current_node)
                del self.count_to_node[current_count]
        
        # Add key to new count node
        if new_count not in self.count_to_node:
            new_node = Node(new_count)
            self.count_to_node[new_count] = new_node
            
            # Find correct position to insert new node
            if current_count == 0:
                insert_after = self.head
            else:
                insert_after = self.count_to_node.get(current_count, self.head)
                if current_count not in self.count_to_node:
                    # Find the node with count less than new_count
                    insert_after = self.head
                    current = self.head.next
                    while current != self.tail and current.count < new_count:
                        insert_after = current
                        current = current.next
            
            self._insert_after(insert_after, new_node)
        
        self.count_to_node[new_count].keys.add(key)

    def dec(self, key: str) -> None:
        """Decrement the count of the key by 1.
        
        Args:
            key: The key to decrement
        """
        if key not in self.key_to_count:
            return
        
        current_count = self.key_to_count[key]
        new_count = current_count - 1
        
        # Remove key from current count node
        current_node = self.count_to_node[current_count]
        current_node.keys.remove(key)
        if not current_node.keys:  # Remove empty node
            self._remove_node(current_node)
            del self.count_to_node[current_count]
        
        if new_count == 0:
            # Remove key entirely
            del self.key_to_count[key]
        else:
            # Update key count and add to appropriate node
            self.key_to_count[key] = new_count
            
            if new_count not in self.count_to_node:
                new_node = Node(new_count)
                self.count_to_node[new_count] = new_node
                
                # Find correct position to insert new node
                insert_after = self.head
                current = self.head.next
                while current != self.tail and current.count < new_count:
                    insert_after = current
                    current = current.next
                
                self._insert_after(insert_after, new_node)
            
            self.count_to_node[new_count].keys.add(key)

    def getMaxKey(self) -> str:
        """Return one of the keys with maximal count.
        
        Returns:
            A key with maximum count, or empty string if no keys exist
        """
        if self.tail.prev == self.head:  # No keys exist
            return ""
        
        max_node = self.tail.prev
        return next(iter(max_node.keys))  # Return any key from the set

    def getMinKey(self) -> str:
        """Return one of the keys with minimal count.
        
        Returns:
            A key with minimum count, or empty string if no keys exist
        """
        if self.head.next == self.tail:  # No keys exist
            return ""
        
        min_node = self.head.next
        return next(iter(min_node.keys))  # Return any key from the set

    def _insert_after(self, prev_node: Node, new_node: Node) -> None:
        """Insert new_node after prev_node in the doubly linked list.
        
        Args:
            prev_node: The node after which to insert
            new_node: The node to insert
        """
        next_node = prev_node.next
        prev_node.next = new_node
        new_node.prev = prev_node
        new_node.next = next_node
        next_node.prev = new_node

    def _remove_node(self, node: Node) -> None:
        """Remove node from the doubly linked list.
        
        Args:
            node: The node to remove
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node