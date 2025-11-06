"""
A* algorithm implementation for finding shortest paths with heuristic optimization.
"""
from typing import Dict, List, Tuple, Optional, Set
import heapq
import math
import time
from models.graph import FlightNetwork, Airport, Route
from data.route_loader import calculate_distance


class AStarPathFinder:
    """
    Implements A* algorithm for finding shortest paths between airports using heuristics.
    """
    
    def __init__(self, network: FlightNetwork):
        """
        Initialize A* pathfinder with flight network.
        
        Args:
            network: FlightNetwork graph to search
        """
        # TODO: Store reference to flight network
        # TODO: Initialize heuristic caching
        self.network = network
        self.heuristic_cache = {}

        self.last_run_stats = {}
        
        
    def find_shortest_path(self, source: str, destination: str, heuristic: str = "euclidean") -> Tuple[List[str], float]:
        """
        Find shortest path using A* algorithm with heuristic.
        
        Args:
            source: Source airport code
            destination: Destination airport code
            heuristic: Heuristic function type ("euclidean", "haversine", "manhattan")
        
        Returns:
            Tuple of (path_as_list_of_airports, total_weight)
        """
        # Track execution time
        start_time = time.time()

        # Reset stats for last run
        self.last_run_stats = {
            "nodes_expanded": 0,
            "nodes_generated": 0,
            "execution_time": 0,
            "path_cost": 0,
            "heuristic_calls": 0,
        }

        # TODO: Validate source and destination airports exist
        if source not in self.network.airports:
            raise ValueError(f"Source airport {source} not found in network")
        if destination not in self.network.airports:
            raise ValueError(f"Destination airport {destination} not found in network")

        # TODO: Handle case where source == destination
        if source == destination:
            return ([source], 0.0)

        # TODO: Initialize g_score (actual distance from start)
        g_score = {source: 0.0}

        # TODO: Initialize f_score (g_score + heuristic)
        h_score = {source: self._heuristic(source, destination, heuristic)}
        f_score = {source: h_score[source]}

        # TODO: Initialize open_set (priority queue) with source
        counter = 0
        open_set = [(f_score[source], counter, source)]

        # TODO: Initialize came_from dictionary for path reconstruction

        came_from = {}
        
        # TODO: Initialize closed_set for visited nodes
        closed_set = set()


        # TODO: Main A* algorithm loop:
        # TODO: - While open_set is not empty:
        # TODO: - Pop node with lowest f_score
        # TODO: - If destination reached, reconstruct and return path
        # TODO: - Add current to closed_set
        # TODO: - For each neighbor:
        # TODO:   - Skip if in closed_set
        # TODO:   - Calculate tentative g_score
        # TODO:   - If neighbor not in open_set or new g_score is better:
        # TODO:     - Update came_from, g_score, f_score
        # TODO:     - Add neighbor to open_set
        
        # TODO: Return empty path if no solution found
        while open_set:
            # Pop node with lowest f_score
            current_h, _, current = heapq.heappop(open_set) # (current_node_f_score, counter, current_node)
            if current in closed_set:
                continue

            # If destination reached, reconstruct and return path
            if current == destination:
                path = self._reconstruct_path(came_from, current)
                self.last_run_stats["path_cost"] = g_score[current]
                self.last_run_stats["execution_time"] = time.time() - start_time

                return (path, g_score[current])
            
            # Add current to closed_set
            closed_set.add(current)
            self.last_run_stats["nodes_expanded"] += 1

            # Get each neighbor of current
            neighbors = self.network.get_neighbors(current)

            for neighbor_code, edge_weight in neighbors:
                if neighbor_code in closed_set:
                    continue
                
                # Calculate tentative g_score through current
                tentative_g_score = g_score[current] + edge_weight

                # If neighbor not in open_set or new g_score is better:
                if neighbor_code not in g_score or tentative_g_score < g_score[neighbor_code]:
                    # Update came_from, g_score, f_score
                    came_from[neighbor_code] = current
                    g_score[neighbor_code] = tentative_g_score
                    f = self._heuristic(neighbor_code, destination, heuristic)
                    f_score[neighbor_code] = tentative_g_score + f

                    # Add neighbor to open_set
                    self.last_run_stats["nodes_generated"] += 1
                    counter += 1
                    heapq.heappush(open_set, (f_score[neighbor_code], counter, neighbor_code))

        # Return empty path if no solution found
        self.last_run_stats["execution_time"] = time.time() - start_time
        return ([], float('inf'))
            
    def _reconstruct_path(self, came_from: Dict[str, str], current: str) -> List[str]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1] # Reverse path to get source -> destination order
    
    def _heuristic(self, airport1: str, airport2: str, heuristic_type: str = "euclidean") -> float:
        """
        Calculate heuristic distance between two airports.
        
        Args:
            airport1: First airport code
            airport2: Second airport code
            heuristic_type: Type of heuristic function
        
        Returns:
            Heuristic distance estimate
        """
        # TODO: Get coordinates for both airports
        # TODO: Implement euclidean distance heuristic
        # TODO: Implement haversine distance heuristic (great circle)
        # TODO: Implement manhattan  distance heuristic
        # TODO: Ensure heuristic is admissible (never overestimates)
        # TODO: Return heuristic distance
        self.last_run_stats["heuristic_calls"] += 1

        # Check if heuristic is in cache
        cache_key = (airport1, airport2, heuristic_type)
        if cache_key in self.heuristic_cache:
            return self.heuristic_cache[cache_key]
        
        # Getting coordinates for both airports
        airport1 = self.network.airports[airport1]
        airport2 = self.network.airports[airport2]

        lat1, long1 = airport1.latitude, airport1.longitude
        lat2, long2 = airport2.latitude, airport2.longitude

        if heuristic_type == "euclidean":
            distance = self._euclidean_distance(lat1, long1, lat2, long2)
        elif heuristic_type == "haversine":
            distance = calculate_distance(lat1, long1, lat2, long2)
        elif heuristic_type == "manhattan":
            distance = self._manhattan_distance(lat1, long1, lat2, long2)
        else:
            raise ValueError(f"Invalid heuristic type: {heuristic_type}")
    
        # Cache result
        self.heuristic_cache[cache_key] = distance

        return distance

    
    def _euclidean_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate Euclidean distance between two coordinates.
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
        
        Returns:
            Euclidean distance
        """
        # TODO: Calculate straight-line distance using Euclidean formula
        # TODO: Convert coordinates to appropriate scale/units
        # TODO: Return distance in same units as edge weights

        # Convert coordinates to radians
        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
        
        R = 6371.0 # Earth's radius in kilometers

        # Calculate x,y,z coordinates
        x1 = R * math.cos(lat1_rad) * math.cos(lon1_rad)
        y1 = R * math.cos(lat1_rad) * math.sin(lon1_rad)
        z1 = R * math.sin(lat1_rad)

        x2 = R * math.cos(lat2_rad) * math.cos(lon2_rad)
        y2 = R * math.cos(lat2_rad) * math.sin(lon2_rad)
        z2 = R * math.sin(lat2_rad)

        # Calculate Euclidean distance
        distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)

        return distance # Return distance in kilometers

    
    def _manhattan_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate Manhattan distance between two coordinates.
        
        Args:
            lat1, lon1: First point coordinates  
            lat2, lon2: Second point coordinates
        
        Returns:
            Manhattan distance
        """
        # TODO: Calculate Manhattan distance |x1-x2| + |y1-y2|
        # TODO: Convert to appropriate units
        # TODO: Ensure admissibility for flight paths

        lat_diff = abs(lat2 - lat1) * 111.0
        
        # Average latitude for longitude calculation
        avg_lat = (lat1 + lat2) / 2
        lon_diff = abs(lon2 - lon1) * 111.0 * math.cos(math.radians(avg_lat))
        
        # Manhattan distance
        distance = lat_diff + lon_diff
        
        return distance
    
    def compare_with_dijkstra(self, source: str, destination: str) -> Dict[str, any]:
        """
        Compare A* performance with Dijkstra's algorithm.
        
        Args:
            source: Source airport
            destination: Destination airport
        
        Returns:
            Dictionary with comparison metrics
        """
        # TODO: Run both A* and Dijkstra on same source/destination
        # TODO: Compare execution time, nodes visited, path length
        # TODO: Verify both algorithms find same optimal path
        # TODO: Calculate performance improvement of A*
        # TODO: Return comparison statistics
        pass
    
    def get_algorithm_stats(self) -> Dict[str, any]:
        """
        Get statistics about the last A* algorithm run.
        
        Returns:
            Dictionary with algorithm performance stats
        """
        # TODO: Track and return A* performance metrics:
        # TODO: - Nodes expanded vs nodes generated
        # TODO: - Heuristic effectiveness (reduction in search space)
        # TODO: - Execution time compared to uninformed search
        # TODO: - Memory usage
        # TODO: - Path optimality verification
        pass

