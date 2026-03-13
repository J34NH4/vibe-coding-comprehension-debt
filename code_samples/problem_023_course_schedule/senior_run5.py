from typing import List
from collections import defaultdict, deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Determines if all courses can be finished given prerequisites using topological sort.
        
        Args:
            numCourses: Total number of courses labeled from 0 to numCourses-1
            prerequisites: List of prerequisite pairs [course, prerequisite]
            
        Returns:
            True if all courses can be finished, False if there's a cycle
        """
        if numCourses <= 0:
            return False
            
        if not prerequisites:
            return True
            
        # Build adjacency list and calculate in-degrees
        adjacency_graph = self._build_adjacency_graph(prerequisites)
        in_degree_count = self._calculate_in_degrees(numCourses, prerequisites)
        
        # Perform topological sort using Kahn's algorithm
        return self._has_valid_topological_order(numCourses, adjacency_graph, in_degree_count)
    
    def _build_adjacency_graph(self, prerequisites: List[List[int]]) -> defaultdict:
        """
        Builds adjacency list representation of the prerequisite graph.
        
        Args:
            prerequisites: List of prerequisite pairs [course, prerequisite]
            
        Returns:
            Dictionary mapping each prerequisite to list of dependent courses
        """
        adjacency_graph = defaultdict(list)
        
        for course, prerequisite in prerequisites:
            adjacency_graph[prerequisite].append(course)  # prerequisite -> course
            
        return adjacency_graph
    
    def _calculate_in_degrees(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Calculates in-degree for each course (number of prerequisites).
        
        Args:
            numCourses: Total number of courses
            prerequisites: List of prerequisite pairs [course, prerequisite]
            
        Returns:
            List where index represents course and value represents in-degree
        """
        in_degree_count = [0] * numCourses
        
        for course, prerequisite in prerequisites:
            in_degree_count[course] += 1  # course has one more prerequisite
            
        return in_degree_count
    
    def _has_valid_topological_order(self, numCourses: int, adjacency_graph: defaultdict, 
                                   in_degree_count: List[int]) -> bool:
        """
        Determines if valid topological ordering exists using Kahn's algorithm.
        
        Args:
            numCourses: Total number of courses
            adjacency_graph: Graph mapping prerequisites to dependent courses
            in_degree_count: In-degree count for each course
            
        Returns:
            True if valid topological order exists (no cycles), False otherwise
        """
        # Initialize queue with courses having no prerequisites
        zero_in_degree_queue = deque()
        for course_id in range(numCourses):
            if in_degree_count[course_id] == 0:
                zero_in_degree_queue.append(course_id)
        
        completed_courses_count = 0
        
        # Process courses in topological order
        while zero_in_degree_queue:
            current_course = zero_in_degree_queue.popleft()
            completed_courses_count += 1
            
            # Update in-degrees of dependent courses
            for dependent_course in adjacency_graph[current_course]:
                in_degree_count[dependent_course] -= 1
                
                # Add course to queue if all prerequisites are satisfied
                if in_degree_count[dependent_course] == 0:
                    zero_in_degree_queue.append(dependent_course)
        
        # All courses can be completed if no cycles exist
        return completed_courses_count == numCourses