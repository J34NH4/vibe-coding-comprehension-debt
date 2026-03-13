from collections import defaultdict, deque
from typing import List


class Solution:
    """Solution for Course Schedule problem using topological sorting."""
    
    WHITE = 0  # Unvisited node
    GRAY = 1   # Currently being processed
    BLACK = 2  # Completely processed
    
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Determines if all courses can be finished given prerequisites.
        
        Args:
            numCourses: Total number of courses labeled from 0 to numCourses-1
            prerequisites: List of prerequisite pairs [course, prerequisite]
            
        Returns:
            True if all courses can be finished, False if cycle exists
        """
        if not prerequisites or numCourses <= 1:
            return True
            
        adjacency_graph = self._build_adjacency_graph(prerequisites)
        return self._detect_cycle_using_dfs(numCourses, adjacency_graph)
    
    def _build_adjacency_graph(self, prerequisites: List[List[int]]) -> defaultdict:
        """
        Builds adjacency list representation of prerequisite graph.
        
        Args:
            prerequisites: List of prerequisite pairs
            
        Returns:
            Adjacency graph as defaultdict
        """
        adjacency_graph = defaultdict(list)
        
        for course, prerequisite in prerequisites:
            adjacency_graph[prerequisite].append(course)  # prerequisite -> course
            
        return adjacency_graph
    
    def _detect_cycle_using_dfs(self, numCourses: int, adjacency_graph: defaultdict) -> bool:
        """
        Detects cycle in directed graph using DFS with three-color approach.
        
        Args:
            numCourses: Total number of courses
            adjacency_graph: Graph representation
            
        Returns:
            True if no cycle exists (courses can be finished)
        """
        node_colors = [self.WHITE] * numCourses
        
        for current_course in range(numCourses):
            if node_colors[current_course] == self.WHITE:
                if self._has_cycle_from_node(current_course, adjacency_graph, node_colors):
                    return False  # Cycle detected
                    
        return True  # No cycle found
    
    def _has_cycle_from_node(self, start_node: int, adjacency_graph: defaultdict, node_colors: List[int]) -> bool:
        """
        Performs DFS from given node to detect cycles.
        
        Args:
            start_node: Starting node for DFS
            adjacency_graph: Graph representation
            node_colors: Color state of each node
            
        Returns:
            True if cycle is detected from this node
        """
        node_colors[start_node] = self.GRAY  # Mark as currently processing
        
        for neighbor_course in adjacency_graph[start_node]:
            if node_colors[neighbor_course] == self.GRAY:
                return True  # Back edge found - cycle detected
            elif node_colors[neighbor_course] == self.WHITE:
                if self._has_cycle_from_node(neighbor_course, adjacency_graph, node_colors):
                    return True
                    
        node_colors[start_node] = self.BLACK  # Mark as completely processed
        return False