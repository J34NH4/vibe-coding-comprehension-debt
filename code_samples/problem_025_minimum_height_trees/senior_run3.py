from typing import List, Set, Dict
from collections import defaultdict, deque

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Find all nodes that can be roots to form minimum height trees.
        
        Args:
            n: Number of nodes in the tree
            edges: List of edges representing the tree structure
            
        Returns:
            List of node labels that can serve as roots for minimum height trees
        """
        # Handle edge cases
        if n <= 2:
            return list(range(n))
        
        # Build adjacency list representation
        adjacency_graph = self._build_adjacency_graph(edges)
        
        # Find minimum height tree roots using centroid approach
        return self._find_centroids(adjacency_graph, n)
    
    def _build_adjacency_graph(self, edges: List[List[int]]) -> Dict[int, Set[int]]:
        """
        Build adjacency list representation of the tree.
        
        Args:
            edges: List of edges in the tree
            
        Returns:
            Dictionary mapping each node to its set of neighbors
        """
        adjacency_graph = defaultdict(set)
        
        for source_node, target_node in edges:
            adjacency_graph[source_node].add(target_node)
            adjacency_graph[target_node].add(source_node)
            
        return adjacency_graph
    
    def _find_centroids(self, adjacency_graph: Dict[int, Set[int]], total_nodes: int) -> List[int]:
        """
        Find centroid nodes by iteratively removing leaf nodes.
        
        Args:
            adjacency_graph: Adjacency list representation of the tree
            total_nodes: Total number of nodes in the tree
            
        Returns:
            List of centroid nodes (1 or 2 nodes maximum)
        """
        remaining_nodes = total_nodes
        leaf_queue = deque()
        
        # Initialize leaf queue with all leaf nodes (degree = 1)
        for node_id, neighbors in adjacency_graph.items():
            if len(neighbors) == 1:
                leaf_queue.append(node_id)
        
        # Iteratively remove leaves until 1 or 2 nodes remain
        while remaining_nodes > 2:
            current_leaf_count = len(leaf_queue)
            remaining_nodes -= current_leaf_count
            
            # Process current level of leaf nodes
            for _ in range(current_leaf_count):
                leaf_node = leaf_queue.popleft()
                
                # Remove leaf from its neighbor's adjacency list
                neighbor_node = next(iter(adjacency_graph[leaf_node]))
                adjacency_graph[neighbor_node].remove(leaf_node)
                
                # If neighbor becomes a leaf, add to queue
                if len(adjacency_graph[neighbor_node]) == 1:
                    leaf_queue.append(neighbor_node)
        
        # Return remaining nodes as centroids
        return self._get_remaining_nodes(adjacency_graph)
    
    def _get_remaining_nodes(self, adjacency_graph: Dict[int, Set[int]]) -> List[int]:
        """
        Extract nodes that still have connections in the adjacency graph.
        
        Args:
            adjacency_graph: Current state of adjacency graph
            
        Returns:
            List of nodes that still have neighbors
        """
        remaining_centroids = []
        
        for node_id, neighbors in adjacency_graph.items():
            if neighbors:  # Node still has connections
                remaining_centroids.append(node_id)
                
        return remaining_centroids