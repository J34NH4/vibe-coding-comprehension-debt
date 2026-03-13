from typing import List
from collections import deque, defaultdict

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Find all roots that result in minimum height trees.
        
        Args:
            n: Number of nodes in the tree
            edges: List of edges representing the tree
            
        Returns:
            List of node labels that can be roots for minimum height trees
        """
        # Handle edge cases
        if n <= 0:
            return []
        if n == 1:
            return [0]
        if n == 2:
            return [0, 1]
            
        # Build adjacency list representation of the tree
        adjacency_graph = self._build_adjacency_graph(n, edges)
        
        # Find minimum height tree roots using topological sort approach
        return self._find_minimum_height_roots(n, adjacency_graph)
    
    def _build_adjacency_graph(self, node_count: int, edge_list: List[List[int]]) -> defaultdict:
        """
        Build adjacency list representation of the tree.
        
        Args:
            node_count: Total number of nodes
            edge_list: List of edges in the tree
            
        Returns:
            Adjacency list as defaultdict
        """
        adjacency_graph = defaultdict(set)
        
        for source_node, target_node in edge_list:
            adjacency_graph[source_node].add(target_node)
            adjacency_graph[target_node].add(source_node)
            
        return adjacency_graph
    
    def _find_minimum_height_roots(self, node_count: int, adjacency_graph: defaultdict) -> List[int]:
        """
        Find roots that minimize tree height using leaf removal approach.
        
        Args:
            node_count: Total number of nodes
            adjacency_graph: Adjacency list representation
            
        Returns:
            List of root candidates for minimum height trees
        """
        remaining_nodes = node_count
        leaf_queue = deque()
        
        # Initialize queue with all leaf nodes (degree 1)
        for current_node in range(node_count):
            if len(adjacency_graph[current_node]) <= 1:
                leaf_queue.append(current_node)
        
        # Iteratively remove leaf nodes until 1 or 2 nodes remain
        while remaining_nodes > 2:
            current_leaf_count = len(leaf_queue)
            remaining_nodes -= current_leaf_count
            
            # Remove current layer of leaf nodes
            for _ in range(current_leaf_count):
                current_leaf = leaf_queue.popleft()
                
                # Remove leaf from its neighbor's adjacency list
                if adjacency_graph[current_leaf]:
                    neighbor_node = adjacency_graph[current_leaf].pop()
                    adjacency_graph[neighbor_node].remove(current_leaf)
                    
                    # If neighbor becomes a leaf, add to queue
                    if len(adjacency_graph[neighbor_node]) == 1:
                        leaf_queue.append(neighbor_node)
        
        # Return remaining nodes as minimum height tree roots
        return list(leaf_queue)