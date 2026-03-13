from collections import defaultdict, deque
from typing import List, Set, Dict

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Find all root nodes that result in minimum height trees.
        
        Args:
            n: Number of nodes in the tree
            edges: List of edges connecting nodes
            
        Returns:
            List of node labels that can serve as roots for minimum height trees
        """
        # Edge case: single node
        if n == 1:
            return [0]
            
        # Edge case: two nodes
        if n == 2:
            return [0, 1]
        
        # Build adjacency list representation
        adjacency_graph = self._build_adjacency_graph(n, edges)
        
        # Find minimum height tree roots using leaf removal approach
        return self._find_min_height_roots(n, adjacency_graph)
    
    def _build_adjacency_graph(self, node_count: int, edges: List[List[int]]) -> Dict[int, Set[int]]:
        """
        Build adjacency list representation of the tree.
        
        Args:
            node_count: Total number of nodes
            edges: List of edges connecting nodes
            
        Returns:
            Dictionary mapping each node to its set of neighbors
        """
        adjacency_graph = defaultdict(set)
        
        for node_a, node_b in edges:
            adjacency_graph[node_a].add(node_b)
            adjacency_graph[node_b].add(node_a)
            
        return adjacency_graph
    
    def _find_min_height_roots(self, node_count: int, adjacency_graph: Dict[int, Set[int]]) -> List[int]:
        """
        Find roots that result in minimum height trees using leaf removal.
        
        Args:
            node_count: Total number of nodes
            adjacency_graph: Graph represented as adjacency list
            
        Returns:
            List of nodes that can serve as roots for minimum height trees
        """
        remaining_nodes = node_count
        leaf_queue = deque()
        
        # Initialize leaf queue with all leaf nodes (degree 1)
        for node in range(node_count):
            if len(adjacency_graph[node]) == 1:
                leaf_queue.append(node)
        
        # Remove leaves layer by layer until 1 or 2 nodes remain
        while remaining_nodes > 2:
            current_leaf_count = len(leaf_queue)
            remaining_nodes -= current_leaf_count
            
            # Process current layer of leaves
            for _ in range(current_leaf_count):
                current_leaf = leaf_queue.popleft()
                
                # Remove leaf from its neighbor's adjacency list
                neighbor_node = next(iter(adjacency_graph[current_leaf]))
                adjacency_graph[neighbor_node].remove(current_leaf)
                
                # If neighbor becomes a leaf, add to queue
                if len(adjacency_graph[neighbor_node]) == 1:
                    leaf_queue.append(neighbor_node)
        
        # Remaining nodes are the minimum height tree roots
        return self._get_remaining_nodes(node_count, adjacency_graph)
    
    def _get_remaining_nodes(self, node_count: int, adjacency_graph: Dict[int, Set[int]]) -> List[int]:
        """
        Get all nodes that still have connections in the graph.
        
        Args:
            node_count: Total number of nodes
            adjacency_graph: Current state of adjacency graph
            
        Returns:
            List of nodes that still have neighbors
        """
        remaining_roots = []
        
        for node in range(node_count):
            if adjacency_graph[node]:  # Node still has neighbors
                remaining_roots.append(node)
                
        return remaining_roots