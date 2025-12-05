"""
Test suite for Dijkstra's algorithm implementation.
"""
import unittest
from unittest.mock import Mock
from algorithms.dijkstra import DijkstraPathFinder
from models.graph import FlightNetwork, Airport, Route


class TestDijkstraPathFinder(unittest.TestCase):
    """Test cases for Dijkstra's algorithm implementation."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.network = FlightNetwork()
        
        airports_data = [
            ("LAX", "Los Angeles", 33.9425, -118.408),
            ("JFK", "New York", 40.6413, -73.7781),
            ("ORD", "Chicago", 41.9742, -87.9073),
            ("DFW", "Dallas", 32.8998, -97.0403),
            ("ATL", "Atlanta", 33.6407, -84.4277),
        ]
        
        for code, city, lat, lon in airports_data:
            airport = Airport(
                code=code,
                name=f"{city} Airport",
                city=city,
                country="United States",
                latitude=lat,
                longitude=lon
            )
            self.network.add_airport(airport)
        
        routes_data = [
            ("LAX", "ORD", 1745),
            ("LAX", "DFW", 1235),
            ("ORD", "JFK", 740),
            ("ORD", "DFW", 800),
            ("DFW", "JFK", 1380),
            ("DFW", "ATL", 730),
            ("ATL", "JFK", 760),
        ]
        
        for source, dest, distance in routes_data:
            route = Route(source=source, destination=dest, distance=distance)
            self.network.add_route(route)
        
        self.pathfinder = DijkstraPathFinder(self.network)
    
    def test_shortest_path_direct_route(self):
        """Test shortest path for directly connected airports."""
        path, distance = self.pathfinder.find_shortest_path("LAX", "ORD")
        
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0], "LAX")
        self.assertEqual(path[-1], "ORD")
        self.assertEqual(distance, 1745)
    
    def test_shortest_path_multi_hop(self):
        """Test shortest path requiring multiple hops."""
        path, distance = self.pathfinder.find_shortest_path("LAX", "ATL")
        
        self.assertEqual(path, ["LAX", "DFW", "ATL"])
        self.assertEqual(distance, 1965)
    
    def test_no_path_exists(self):
        """Test behavior when no path exists between airports."""
        isolated_airport = Airport(
            code="XXX",
            name="Isolated Airport",
            city="Isolated",
            country="United States",
            latitude=0.0,
            longitude=0.0
        )
        self.network.add_airport(isolated_airport)
        
        path, distance = self.pathfinder.find_shortest_path("LAX", "XXX")
        
        self.assertEqual(path, [])
        self.assertEqual(distance, float('inf'))
    
    def test_same_source_destination(self):
        """Test pathfinding when source equals destination."""
        path, distance = self.pathfinder.find_shortest_path("LAX", "LAX")
        
        self.assertEqual(path, ["LAX"])
        self.assertEqual(distance, 0.0)
    
    def test_invalid_source_airport(self):
        """Test behavior with invalid source airport code."""
        with self.assertRaises(ValueError):
            self.pathfinder.find_shortest_path("INVALID", "LAX")
    
    def test_invalid_destination_airport(self):
        """Test behavior with invalid destination airport code."""
        with self.assertRaises(ValueError):
            self.pathfinder.find_shortest_path("LAX", "INVALID")
    
    def test_algorithm_optimality(self):
        """Test that Dijkstra finds truly optimal paths."""
        path, distance = self.pathfinder.find_shortest_path("LAX", "JFK")
        
        self.assertEqual(path, ["LAX", "ORD", "JFK"])
        self.assertEqual(distance, 2485)
    
    def test_algorithm_stats_tracking(self):
        """Test that algorithm statistics are properly tracked."""
        path, distance = self.pathfinder.find_shortest_path("LAX", "JFK")
        
        stats = self.pathfinder.get_algorithm_stats()
        
        self.assertIn("nodes_expanded", stats)
        self.assertIn("nodes_generated", stats)
        self.assertIn("execution_time", stats)
        self.assertIn("path_cost", stats)
        
        self.assertGreater(stats["nodes_expanded"], 0)
        self.assertGreater(stats["execution_time"], 0)
        self.assertEqual(stats["path_cost"], distance)
    
    def test_find_all_shortest_paths(self):
        """Test finding shortest paths to all destinations."""
        all_paths = self.pathfinder.find_all_shortest_paths("LAX")
        
        self.assertIn("JFK", all_paths)
        self.assertIn("ORD", all_paths)
        self.assertIn("DFW", all_paths)
        
        self.assertEqual(all_paths["ORD"][1], 1745)
        self.assertEqual(all_paths["JFK"][0], ["LAX", "ORD", "JFK"])
        self.assertEqual(all_paths["JFK"][1], 2485)
    
    def test_k_shortest_paths(self):
        """Test finding k shortest paths between airports."""
        k_paths = self.pathfinder.find_k_shortest_paths("LAX", "JFK", k=2)
        
        self.assertGreater(len(k_paths), 0)
        self.assertLessEqual(len(k_paths), 2)
        
        for i in range(len(k_paths) - 1):
            self.assertLessEqual(k_paths[i][1], k_paths[i + 1][1])
        
        self.assertEqual(k_paths[0][0], ["LAX", "ORD", "JFK"])
        self.assertEqual(k_paths[0][1], 2485)
    
    def test_k_shortest_paths_invalid_k(self):
        """Test k-shortest paths with invalid k value."""
        with self.assertRaises(ValueError):
            self.pathfinder.find_k_shortest_paths("LAX", "JFK", k=0)
        
        with self.assertRaises(ValueError):
            self.pathfinder.find_k_shortest_paths("LAX", "JFK", k=-1)


if __name__ == "__main__":
    unittest.main()
