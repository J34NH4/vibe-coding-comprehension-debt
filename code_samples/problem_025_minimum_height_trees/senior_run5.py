from typing import List
from collections import deque, defaultdict

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Find all roots that result in minimum height trees.
        
        Args:
            n: Number of nodes in the tree
            edges: List of edges representing the tree structure
            
        Returns:
            List of node labels that can serve as roots for minimum height trees
        """
        # Handle edge cases
        if n <= 0:
            return []
        if n == 1:
            return [0]
        if n == 2:
            return [0, 1]
            
        # Build adjacency list representation
        adjacency_list = self._build_adjacency_list(n, edges)
        
        # Find minimum height trees using topological sorting approach
        return self._find_centroids_using_leaf_removal(n, adjacency_list)
    
    def _build_adjacency_list(self, n: int, edges: List[List[int]]) -> defaultdict:
        """
        Build adjacency list from edge list.
        
        Args:
            n: Number of nodes
            edges: List of edges
            
        Returns:
            Adjacency list representation of the graph
        """
        adjacency_list = defaultdict(set)
        
        for source_node, target_node in edges:
            adjacency_list[source_node].add(target_node)
            adjacency_list[target_node].add(source_node)
            
        return adjacency_list
    
    def _find_centroids_using_leaf_removal(self, n: int, adjacency_list: defaultdict) -> List[int]:
        """
        Find centroids by iteratively removing leaf nodes.
        
        The centroid(s) of a tree are the nodes that minimize the maximum distance
        to any other node. In a tree, there can be at most 2 centroids.
        
        Args:
            n: Number of nodes
            adjacency_list: Graph representation
            
        Returns:
            List containing 1 or 2 centroid nodes
        """
        remaining_nodes = n
        leaf_queue = deque()
        
        # Find initial leaf nodes (degree = 1)
        for node_id in range(n):
            if len(adjacency_list[node_id]) <= 1:
                leaf_queue.append(node_id)
        
        # Keep removing leaf nodes until 1 or 2 nodes remain
        while remaining_nodes > 2:
            current_leaf_count = len(leaf_queue)
            remaining_nodes -= current_leaf_count
            
            # Process current batch of leaf nodes
            for _ in range(current_leaf_count):
                current_leaf = leaf_queue.popleft()
                
                # Remove leaf from its neighbor's adjacency list
                if adjacency_list[current_leaf]:
                    neighbor_node = adjacency_list[current_leaf].pop()
                    adjacency_list[neighbor_node].discard(current_leaf)
                    
                    # Check if neighbor becomes a new leaf
                    if len(adjacency_list[neighbor_node]) == 1:
                        leaf_queue.append(neighbor_node)
        
        # Return remaining nodes (centroids)
        return list(range(n)) if remaining_nodes == n else [node for node in range(n) if adjacency_list[node]]