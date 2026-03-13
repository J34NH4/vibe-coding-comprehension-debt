from collections import defaultdict, deque
from typing import List, Set, Dict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Determines if all courses can be finished given prerequisite constraints.
        
        Uses topological sorting with Kahn's algorithm to detect cycles in the
        prerequisite dependency graph.
        
        Args:
            numCourses: Total number of courses (0 to numCourses-1)
            prerequisites: List of [course, prerequisite] pairs
            
        Returns:
            True if all courses can be finished, False if there's a cycle
            
        Raises:
            ValueError: If numCourses is negative
        """
        if numCourses < 0:
            raise ValueError("Number of courses cannot be negative")
            
        if numCourses <= 1:
            return True
            
        # Build adjacency list and calculate in-degrees
        adjacency_graph = self._build_adjacency_graph(prerequisites)
        in_degree_count = self._calculate_in_degrees(numCourses, prerequisites)
        
        # Perform topological sort using Kahn's algorithm
        return self._can_complete_topological_sort(numCourses, adjacency_graph, in_degree_count)
    
    def _build_adjacency_graph(self, prerequisites: List[List[int]]) -> Dict[int, List[int]]:
        """
        Builds adjacency list representation of the prerequisite graph.
        
        Args:
            prerequisites: List of [course, prerequisite] pairs
            
        Returns:
            Dictionary mapping prerequisite -> list of dependent courses
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
            List where index represents course and value represents in-degree
        """
        in_degree_count = [0] * numCourses
        
        for course, prerequisite in prerequisites:
            in_degree_count[course] += 1  # course has one more prerequisite
            
        return in_degree_count
    
    def _can_complete_topological_sort(self, numCourses: int, adjacency_graph: Dict[int, List[int]], 
                                     in_degree_count: List[int]) -> bool:
        """
        Performs topological sort to determine if all courses can be completed.
        
        Args:
            numCourses: Total number of courses
            adjacency_graph: Graph mapping prerequisites to dependent courses
            in_degree_count: Array of in-degrees for each course
            
        Returns:
            True if all courses can be processed (no cycles), False otherwise
        """
        # Initialize queue with courses that have no prerequisites
        zero_in_degree_queue = deque()
        for course_id in range(numCourses):
            if in_degree_count[course_id] == 0:
                zero_in_degree_queue.append(course_id)
        
        completed_courses_count = 0
        
        # Process courses with no remaining prerequisites
        while zero_in_degree_queue:
            current_course = zero_in_degree_queue.popleft()
            completed_courses_count += 1
            
            # Update dependent courses by reducing their in-degree
            for dependent_course in adjacency_graph[current_course]:
                in_degree_count[dependent_course] -= 1
                
                # If dependent course has no more prerequisites, add to queue
                if in_degree_count[dependent_course] == 0:
                    zero_in_degree_queue.append(dependent_course)
        
        # All courses can be finished if we processed all of them
        return completed_courses_count == numCourses