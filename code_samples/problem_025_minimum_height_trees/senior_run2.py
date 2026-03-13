from typing import List
from collections import defaultdict, deque

class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        """
        Find all nodes that can be roots of minimum height trees.
        
        Args:
            n: Number of nodes in the tree
            edges: List of edges representing the tree structure
            
        Returns:
            List of node labels that result in minimum height trees
        """
        # Handle edge cases
        if n <= 2:
            return list(range(n))
        
        # Build adjacency list representation
        adjacency_graph = self._build_adjacency_graph(n, edges)
        
        # Find minimum height tree roots using topological approach
        return self._find_centroid_nodes(adjacency_graph, n)
    
    def _build_adjacency_graph(self, n: int, edges: List[List[int]]) -> defaultdict:
        """
        Build adjacency list representation of the tree.
        
        Args:
            n: Number of nodes
            edges: List of edges
            
        Returns:
            Adjacency list as defaultdict
        """
        adjacency_graph = defaultdict(set)
        
        for node_a, node_b in edges:
            adjacency_graph[node_a].add(node_b)
            adjacency_graph[node_b].add(node_a)
        
        return adjacency_graph
    
    def _find_centroid_nodes(self, adjacency_graph: defaultdict, n: int) -> List[int]:
        """
        Find centroid nodes by iteratively removing leaf nodes.
        
        Args:
            adjacency_graph: Adjacency list representation
            n: Number of nodes
            
        Returns:
            List of centroid node labels
        """
        remaining_nodes = n
        leaf_queue = deque()
        
        # Initialize leaf nodes (degree 1)
        for current_node in range(n):
            if len(adjacency_graph[current_node]) <= 1:
                leaf_queue.append(current_node)
        
        # Remove leaf nodes layer by layer until 1-2 nodes remain
        while remaining_nodes > 2:
            current_layer_size = len(leaf_queue)
            remaining_nodes -= current_layer_size
            
            # Process current layer of leaf nodes
            for _ in range(current_layer_size):
                leaf_node = leaf_queue.popleft()
                
                # Remove leaf node from its neighbor
                if adjacency_graph[leaf_node]:
                    neighbor_node = adjacency_graph[leaf_node].pop()
                    adjacency_graph[neighbor_node].remove(leaf_node)
                    
                    # Check if neighbor becomes new leaf
                    if len(adjacency_graph[neighbor_node]) == 1:
                        leaf_queue.append(neighbor_node)
        
        # Remaining nodes are the centroids
        centroid_nodes = []
        for node_index in range(n):
            if adjacency_graph[node_index]:  # Node still has connections
                centroid_nodes.append(node_index)
        
        return centroid_nodes if centroid_nodes else [0]