"""
Dijkstra's algorithm implementation for finding shortest paths in flight network.
"""
from typing import Dict, List, Tuple, Optional, Set
import heapq
import math
import time
import tracemalloc
from models.graph import FlightNetwork, Airport, Route

class DijkstraPathFinder:
    """
    Implements Dijkstra's algorithm for finding shortest paths between airports.
    """
    
    def __init__(self, network: FlightNetwork):
        """
        Initialize pathfinder with flight network.
        
        Args:
            network: FlightNetwork graph to search
        """
        self.network = network
        self.last_run_stats = {}
    
    def find_shortest_path(self, source: str, destination: str) -> Tuple[List[str], float]:
        """
        Find shortest path between two airports using Dijkstra's algorithm.
        
        Args:
            source: Source airport code
            destination: Destination airport code
        
        Returns:
            Tuple of (path_as_list_of_airports, total_weight)
        """

        start_time = time.time()
        tracemalloc.start()
        self.last_run_stats = {
            "nodes_expanded": 0,
            "nodes_generated": 0,
            "execution_time": 0,
            "path_cost": 0,
            "heuristic_calls": 0,
            "peak_memory_bytes": 0,
            "algorithm": "Dijkstra"
        }

        if source not in self.network.airports:
            raise ValueError(f"Source airport {source} not found in network")
        if destination not in self.network.airports:
            raise ValueError(f"Destination airport {destination} not found in network")

        if source == destination:
            return ([source], 0.0)

        distances = {airport: (float('inf') if airport != source else 0) 
            for airport in self.network.airports}
        distances[source] = 0
        previous_nodes = {}
        priority_queue = [(0, source)]
        visited = set()
        
        while priority_queue:
            current_distance, current_airport = heapq.heappop(priority_queue)
            if current_airport in visited:
                continue
            visited.add(current_airport)
            self.last_run_stats["nodes_expanded"] += 1    

            if current_airport == destination:
                break
            
            neighbors = self.network.get_neighbors(current_airport)
            for neighbor_code, edge_weight in neighbors:
                new_distance = current_distance + edge_weight

                if new_distance < distances[neighbor_code]:
                    distances[neighbor_code] = new_distance
                    previous_nodes[neighbor_code] = current_airport
                    heapq.heappush(priority_queue, (new_distance, neighbor_code))
                    self.last_run_stats["nodes_generated"] += 1

        if destination not in previous_nodes and destination != source:
            self.last_run_stats["execution_time"] = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            self.last_run_stats["peak_memory_bytes"] = peak
            tracemalloc.stop()
            return ([], float('inf'))

        path = self._reconstruct_path(previous_nodes, destination)
        total_distance = distances[destination]
        self.last_run_stats["execution_time"] = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        self.last_run_stats["peak_memory_bytes"] = peak
        tracemalloc.stop()
        self.last_run_stats["path_cost"] = total_distance
        return (path, total_distance)
    
    def find_all_shortest_paths(self, source: str) -> Dict[str, Tuple[List[str], float]]:
        """
        Find shortest paths from source to all other airports.
    
        Args:
            source: Source airport code
        
        Returns:
            Dictionary mapping destination -> (path, distance)
        """
        # Run Dijkstra's from source to all destinations
        start_time = time.time()
        results = {}
        self.last_run_stats = {
            "nodes_expanded": 0,
            "nodes_generated": 0,
            "execution_time": 0,
            "path_cost": 0,
            "heuristic_calls": 0,
        }

        # Validate source
        if source not in self.network.airports:
            raise ValueError(f"Source airport {source} not found in network")

        # Initialize distance and previous dictionaries
        distances = {airport: float('inf') for airport in self.network.airports}
        distances[source] = 0
        previous_nodes = {airport: None for airport in self.network.airports}

        priority_queue = [(0, source)]
        visited = set()

        while priority_queue:
            current_distance, current_airport = heapq.heappop(priority_queue)
            if current_airport in visited:
                continue
            visited.add(current_airport)
            self.last_run_stats["nodes_expanded"] += 1

            neighbors = self.network.get_neighbors(current_airport)
            for neighbor_code, edge_weight in neighbors:
                new_distance = current_distance + edge_weight
                if new_distance < distances[neighbor_code]:
                    distances[neighbor_code] = new_distance
                    previous_nodes[neighbor_code] = current_airport
                    heapq.heappush(priority_queue, (new_distance, neighbor_code))
                    self.last_run_stats["nodes_generated"] += 1

        # Build paths to all destinations
        for airport in self.network.airports:
            if airport == source:
                results[airport] = ([source], 0.0)
            elif distances[airport] == float('inf'):
                results[airport] = ([], float('inf'))
            else:
                # Reconstruct path
                path = []
                curr = airport
                while curr is not None:
                    path.append(curr)
                    curr = previous_nodes[curr]
                path.reverse()
                results[airport] = (path, distances[airport])

        self.last_run_stats["execution_time"] = time.time() - start_time
        return results
        
        
    
    def find_k_shortest_paths(self, source: str, destination: str, k: int = 3) -> List[Tuple[List[str], float]]:
        """
        Find k shortest paths between two airports (Yen's algorithm or similar).
        
        Args:
            source: Source airport code
            destination: Destination airport code
            k: Number of shortest paths to find
        
        Returns:
            List of (path, distance) tuples, sorted by distance
        """
        if source not in self.network.airports:
            raise ValueError(f"Source airport {source} not found in network")
        if destination not in self.network.airports:
            raise ValueError(f"Destination airport {destination} not found in network")
        if k < 1:
            raise ValueError("k must be at least 1")

        # First shortest path
        first_path, first_dist = self.find_shortest_path(source, destination)
        if not first_path:
            return []

        shortest_paths: List[Tuple[List[str], float]] = [(first_path, first_dist)]
        candidates: List[Tuple[float, List[str]]] = []

        for _ in range(1, k):
            last_path, _ = shortest_paths[-1]

            # For each spur node in the last path
            for spur_idx in range(len(last_path) - 1):
                spur_node = last_path[spur_idx]
                root_path = last_path[:spur_idx + 1]

                removed_edges = []

                # Remove edges that would cause duplicate paths with same root
                for p, _ in shortest_paths:
                    if len(p) > spur_idx and p[:spur_idx + 1] == root_path:
                        from_node = p[spur_idx]
                        to_node = p[spur_idx + 1]
                        weight = self.network.remove_edge(from_node, to_node)
                        if weight is not None:
                            removed_edges.append((from_node, to_node, weight))

                # Optionally, remove outgoing edges from root_path nodes (except spur_node)
                root_nodes_to_block = root_path[:-1]
                for node in root_nodes_to_block:
                    neighbors = self.network.get_neighbors(node)[:]
                    for dest, weight in neighbors:
                        removed_weight = self.network.remove_edge(node, dest)
                        if removed_weight is not None:
                            removed_edges.append((node, dest, removed_weight))

                # Shortest path from spur_node to destination in modified graph
                spur_path, spur_dist = self.find_shortest_path(spur_node, destination)

                # Restore all removed edges
                for from_node, to_node, weight in removed_edges:
                    self.network.add_edge(from_node, to_node, weight)

                if spur_path:
                    # Combine root_path (without spur_node duplicate) and spur_path
                    total_path = root_path[:-1] + spur_path

                    # Compute root_path distance using current graph weights
                    root_dist = 0.0
                    for i in range(len(root_path) - 1):
                        edge_weight = self.network.get_edge_weight(root_path[i], root_path[i + 1])
                        if edge_weight is not None:
                            root_dist += edge_weight

                    total_dist = root_dist + spur_dist

                    # Avoid duplicates
                    if all(existing_path != total_path for existing_path, _ in shortest_paths):
                        heapq.heappush(candidates, (total_dist, total_path))

            if not candidates:
                break

            dist, path = heapq.heappop(candidates)
            shortest_paths.append((path, dist))

        return shortest_paths

    
    def _reconstruct_path(self, previous: Dict[str, str], destination: str) -> List[str]:
        """
        Reconstruct path from previous nodes dictionary.
        
        Args:
            previous: Dictionary mapping airport -> previous airport in path
            destination: Destination airport to trace back from
        
        Returns:
            List of airports from source to destination
        """
        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous.get(current)
        path.reverse()
        return path
    
    def get_algorithm_stats(self) -> Dict[str, any]:
        """
        Get statistics about the last algorithm run.
        
        Returns:
            Dictionary with algorithm performance stats
        """
        return self.last_run_stats.copy()


