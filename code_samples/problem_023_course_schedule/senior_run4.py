from typing import List, Dict, Set
from collections import defaultdict, deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Determines if all courses can be finished given prerequisites using topological sort.
        
        Args:
            numCourses: Total number of courses labeled from 0 to numCourses - 1
            prerequisites: List of prerequisite pairs [course, prerequisite]
            
        Returns:
            True if all courses can be finished, False if there's a cycle
            
        Raises:
            ValueError: If numCourses is negative
        """
        if numCourses < 0:
            raise ValueError("Number of courses cannot be negative")
            
        if numCourses <= 1:
            return True
            
        # Build adjacency list and in-degree count
        adjacency_graph = self._build_graph(prerequisites)
        in_degree_count = self._calculate_in_degrees(numCourses, prerequisites)
        
        # Use Kahn's algorithm for topological sort
        return self._has_valid_topological_order(numCourses, adjacency_graph, in_degree_count)
    
    def _build_graph(self, prerequisites: List[List[int]]) -> Dict[int, List[int]]:
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
        Calculates in-degree (number of prerequisites) for each course.
        
        Args:
            numCourses: Total number of courses
            prerequisites: List of prerequisite pairs [course, prerequisite]
            
        Returns:
            List where index represents course and value represents in-degree count
        """
        in_degree_count = [0] * numCourses
        
        for course, prerequisite in prerequisites:
            in_degree_count[course] += 1  # course has one more prerequisite
            
        return in_degree_count
    
    def _has_valid_topological_order(self, numCourses: int, adjacency_graph: Dict[int, List[int]], 
                                   in_degree_count: List[int]) -> bool:
        """
        Determines if a valid topological ordering exists using Kahn's algorithm.
        
        Args:
            numCourses: Total number of courses
            adjacency_graph: Graph mapping prerequisites to dependent courses
            in_degree_count: In-degree count for each course
            
        Returns:
            True if valid topological order exists (no cycles), False otherwise
        """
        processing_queue = deque()
        completed_courses = 0
        
        # Find all courses with no prerequisites
        for course_id in range(numCourses):
            if in_degree_count[course_id] == 0:
                processing_queue.append(course_id)
        
        # Process courses level by level
        while processing_queue:
            current_course = processing_queue.popleft()
            completed_courses += 1
            
            # Reduce in-degree for all dependent courses
            for dependent_course in adjacency_graph[current_course]:
                in_degree_count[dependent_course] -= 1
                
                # If all prerequisites satisfied, add to queue
                if in_degree_count[dependent_course] == 0:
                    processing_queue.append(dependent_course)
        
        # All courses can be completed if no cycles exist
        return completed_courses == numCourses