from collections import defaultdict, deque
from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Determines if all courses can be finished given prerequisites using topological sort.
        
        Args:
            numCourses: Total number of courses to take
            prerequisites: List of [course, prerequisite] pairs
            
        Returns:
            True if all courses can be finished, False if there's a cycle
        """
        if not prerequisites:
            return True
            
        # Build adjacency list and calculate in-degrees
        adjacency_graph = self._build_adjacency_graph(prerequisites)
        in_degree_counts = self._calculate_in_degrees(numCourses, prerequisites)
        
        # Perform topological sort using Kahn's algorithm
        return self._has_valid_topological_order(numCourses, adjacency_graph, in_degree_counts)
    
    def _build_adjacency_graph(self, prerequisites: List[List[int]]) -> defaultdict:
        """
        Builds adjacency list representation of the prerequisite graph.
        
        Args:
            prerequisites: List of [course, prerequisite] pairs
            
        Returns:
            Adjacency list where key is prerequisite, value is list of dependent courses
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
            prerequisites: List of [course, prerequisite] pairs
            
        Returns:
            List where index represents course and value represents in-degree count
        """
        in_degree_counts = [0] * numCourses
        
        for course, prerequisite in prerequisites:
            in_degree_counts[course] += 1  # course has one more prerequisite
            
        return in_degree_counts
    
    def _has_valid_topological_order(self, numCourses: int, adjacency_graph: defaultdict, 
                                   in_degree_counts: List[int]) -> bool:
        """
        Performs topological sort using Kahn's algorithm to detect cycles.
        
        Args:
            numCourses: Total number of courses
            adjacency_graph: Graph representation of prerequisites
            in_degree_counts: In-degree count for each course
            
        Returns:
            True if valid topological order exists (no cycles), False otherwise
        """
        processing_queue = deque()
        completed_courses_count = 0
        
        # Start with courses that have no prerequisites
        for course_id in range(numCourses):
            if in_degree_counts[course_id] == 0:
                processing_queue.append(course_id)
        
        # Process courses level by level
        while processing_queue:
            current_course = processing_queue.popleft()
            completed_courses_count += 1
            
            # Update dependent courses
            for dependent_course in adjacency_graph[current_course]:
                in_degree_counts[dependent_course] -= 1  # Remove current prerequisite
                
                if in_degree_counts[dependent_course] == 0:  # All prerequisites met
                    processing_queue.append(dependent_course)
        
        return completed_courses_count == numCourses  # All courses processed means no cycle