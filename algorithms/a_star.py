"""
A* algorithm implementation for finding shortest paths with heuristic optimization.
"""
from typing import Dict, List, Tuple, Optional, Set
import heapq
import math
import time
import tracemalloc
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
        tracemalloc.start()

        # Reset stats for last run
        self.last_run_stats = {
            "nodes_expanded": 0,
            "nodes_generated": 0,
            "execution_time": 0,
            "path_cost": 0,
            "heuristic_calls": 0,
            "peak_memory_bytes": 0,
            "algorithm": "A*"
        }

        if source not in self.network.airports:
            raise ValueError(f"Source airport {source} not found in network")
        if destination not in self.network.airports:
            raise ValueError(f"Destination airport {destination} not found in network")

        if source == destination:
            return ([source], 0.0)

        g_score = {source: 0.0}
        h_score = {source: self._heuristic(source, destination, heuristic)}
        f_score = {source: h_score[source]}
        counter = 0
        open_set = [(f_score[source], counter, source)]
        came_from = {}
        closed_set = set()

        while open_set:
            current_h, _, current = heapq.heappop(open_set)
            if current in closed_set:
                continue

            if current == destination:
                path = self._reconstruct_path(came_from, current)
                self.last_run_stats["path_cost"] = g_score[current]
                self.last_run_stats["execution_time"] = time.time() - start_time
                self.last_run_stats["explored_nodes"] = closed_set.copy()
                self.last_run_stats["came_from"] = came_from.copy()
                current_mem, peak_mem = tracemalloc.get_traced_memory()
                self.last_run_stats["peak_memory_bytes"] = peak_mem
                tracemalloc.stop()

                return (path, g_score[current])
            
            closed_set.add(current)
            self.last_run_stats["nodes_expanded"] += 1
            neighbors = self.network.get_neighbors(current)

            for neighbor_code, edge_weight in neighbors:
                tentative_g_score = g_score[current] + edge_weight

                if tentative_g_score < g_score.get(neighbor_code, float("inf")):
                    came_from[neighbor_code] = current
                    g_score[neighbor_code] = tentative_g_score
                    h = self._heuristic(neighbor_code, destination, heuristic)
                    f = tentative_g_score + h
                    f_score[neighbor_code] = f
                    self.last_run_stats["nodes_generated"] += 1
                    counter += 1
                    heapq.heappush(open_set, (f_score[neighbor_code], counter, neighbor_code))

        self.last_run_stats["execution_time"] = time.time() - start_time
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        self.last_run_stats["peak_memory_bytes"] = peak_mem
        tracemalloc.stop()
        return ([], float('inf'))
            
    def _reconstruct_path(self, came_from: Dict[str, str], current: str) -> List[str]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]
    
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
        self.last_run_stats["heuristic_calls"] += 1

        # Check if heuristic is in cache
        cache_key = (airport1, airport2, heuristic_type)
        if cache_key in self.heuristic_cache:
            return self.heuristic_cache[cache_key]
        
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
        # Convert coordinates to radians
        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
        R = 6371.0

        # Calculate x,y,z coordinates
        x1 = R * math.cos(lat1_rad) * math.cos(lon1_rad)
        y1 = R * math.cos(lat1_rad) * math.sin(lon1_rad)
        z1 = R * math.sin(lat1_rad)

        x2 = R * math.cos(lat2_rad) * math.cos(lon2_rad)
        y2 = R * math.cos(lat2_rad) * math.sin(lon2_rad)
        z2 = R * math.sin(lat2_rad)

        distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
        return distance

    
    def _manhattan_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate Manhattan distance between two coordinates.
        
        Args:
            lat1, lon1: First point coordinates  
            lat2, lon2: Second point coordinates
        
        Returns:
            Manhattan distance
        """
        lat_diff = abs(lat2 - lat1) * 111.0
        lon_diff_raw = abs(lon2 - lon1)

        # Handle date line wraparound: take shorter path
        if lon_diff_raw > 180.0:
            lon_diff_raw = 360.0 - lon_diff_raw
        
        avg_lat = (lat1 + lat2) / 2
        lon_diff = lon_diff_raw * 111.0 * math.cos(math.radians(avg_lat))
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
        from algorithms.dijkstra import DijkstraPathFinder
        
        dijkstra = DijkstraPathFinder(self.network)
        
        # Run Dijkstra
        dijkstra_start = time.time()
        dijkstra_path, dijkstra_cost = dijkstra.find_shortest_path(source, destination)
        dijkstra_time = time.time() - dijkstra_start
        dijkstra_stats = dijkstra.get_algorithm_stats()
        
        # Run A* with haversine heuristic
        astar_start = time.time()
        astar_path, astar_cost = self.find_shortest_path(source, destination, heuristic="haversine")
        astar_time = time.time() - astar_start
        astar_stats = self.get_algorithm_stats()
        
        # Compare results
        paths_optimal = (dijkstra_cost == astar_cost) if (dijkstra_path and astar_path) else True
        
        comparison = {
            'source': source,
            'destination': destination,
            'dijkstra': {
                'path': dijkstra_path,
                'cost': dijkstra_cost,
                'execution_time': dijkstra_time,
                'nodes_expanded': dijkstra_stats.get('nodes_expanded', 0),
                'path_length': len(dijkstra_path)
            },
            'astar': {
                'path': astar_path,
                'cost': astar_cost,
                'execution_time': astar_time,
                'nodes_expanded': astar_stats.get('nodes_expanded', 0),
                'heuristic_calls': astar_stats.get('heuristic_calls', 0),
                'path_length': len(astar_path)
            },
            'comparison': {
                'paths_are_optimal': paths_optimal,
                'time_speedup': dijkstra_time / astar_time if astar_time > 0 else 0,
                'nodes_reduction_percent': ((dijkstra_stats.get('nodes_expanded', 0) - astar_stats.get('nodes_expanded', 0)) / 
                                           dijkstra_stats.get('nodes_expanded', 1) * 100) if dijkstra_stats.get('nodes_expanded', 0) > 0 else 0,
                'astar_faster': astar_time < dijkstra_time,
                'astar_fewer_nodes': astar_stats.get('nodes_expanded', 0) < dijkstra_stats.get('nodes_expanded', 0)
            }
        }
        
        return comparison
    
    def get_algorithm_stats(self) -> Dict[str, any]:
        """
        Get statistics about the last A* algorithm run.
        
        Returns:
            Dictionary with algorithm performance stats
        """
        return self.last_run_stats.copy()

