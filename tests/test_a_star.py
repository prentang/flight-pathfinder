"""
Test suite for A* algorithm implementation.
"""
import unittest
from algorithms.a_star import AStarPathFinder
from algorithms.dijkstra import DijkstraPathFinder
from models.graph import FlightNetwork, Airport, Route


class TestAStarPathFinder(unittest.TestCase):
    """Test cases for A* algorithm implementation."""
    
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
        
        self.pathfinder = AStarPathFinder(self.network)
    
    def test_shortest_path_with_euclidean_heuristic(self):
        """Test A* with Euclidean heuristic."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="euclidean")
        
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], "LAX")
        self.assertEqual(path[-1], "JFK")
        self.assertGreater(cost, 0)
    
    def test_shortest_path_with_haversine_heuristic(self):
        """Test A* with Haversine heuristic."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="haversine")
        
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], "LAX")
        self.assertEqual(path[-1], "JFK")
    
    def test_shortest_path_with_manhattan_heuristic(self):
        """Test A* with Manhattan heuristic."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="manhattan")
        
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], "LAX")
        self.assertEqual(path[-1], "JFK")
    
    def test_same_source_destination(self):
        """Test case where source and destination are the same."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "LAX")
        
        self.assertEqual(path, ["LAX"])
        self.assertEqual(cost, 0.0)
    
    def test_invalid_source_airport(self):
        """Test with invalid source airport code."""
        with self.assertRaises(ValueError):
            self.pathfinder.find_shortest_path("INVALID", "JFK")
    
    def test_invalid_destination_airport(self):
        """Test with invalid destination airport code."""
        with self.assertRaises(ValueError):
            self.pathfinder.find_shortest_path("LAX", "INVALID")
    
    def test_invalid_heuristic_type(self):
        """Test with invalid heuristic type."""
        with self.assertRaises(ValueError):
            self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="invalid")
    
    def test_no_path_available(self):
        """Test case where no route exists between airports."""
        isolated_airport = Airport(
            code="XXX",
            name="Isolated Airport",
            city="Isolated",
            country="United States",
            latitude=0.0,
            longitude=0.0
        )
        self.network.add_airport(isolated_airport)
        
        path, cost = self.pathfinder.find_shortest_path("LAX", "XXX")
        
        self.assertEqual(path, [])
        self.assertEqual(cost, float('inf'))
    
    def test_algorithm_stats(self):
        """Test that algorithm statistics are tracked correctly."""
        self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="euclidean")
        stats = self.pathfinder.get_algorithm_stats()
        
        self.assertIn("nodes_expanded", stats)
        self.assertIn("nodes_generated", stats)
        self.assertIn("execution_time", stats)
        self.assertIn("path_cost", stats)
        self.assertIn("heuristic_calls", stats)
        
        self.assertGreater(stats["nodes_expanded"], 0)
        self.assertGreater(stats["execution_time"], 0)
        self.assertGreater(stats["heuristic_calls"], 0)
    
    def test_heuristic_caching(self):
        """Test that heuristic values are cached properly."""
        self.pathfinder.heuristic_cache.clear()
        
        self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="euclidean")
        cache_size_after_first = len(self.pathfinder.heuristic_cache)
        
        self.assertGreater(cache_size_after_first, 0)
    
    def test_path_optimality_vs_dijkstra(self):
        """Test that A* finds optimal paths like Dijkstra."""
        dijkstra = DijkstraPathFinder(self.network)
        
        dijkstra_path, dijkstra_cost = dijkstra.find_shortest_path("LAX", "JFK")
        astar_path, astar_cost = self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="haversine")
        
        self.assertEqual(dijkstra_cost, astar_cost)
    
    def test_heuristic_effectiveness(self):
        """Test that A* explores fewer nodes than Dijkstra."""
        dijkstra = DijkstraPathFinder(self.network)
        
        dijkstra.find_shortest_path("LAX", "JFK")
        dijkstra_stats = dijkstra.get_algorithm_stats()
        
        self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="haversine")
        astar_stats = self.pathfinder.get_algorithm_stats()
        
        self.assertLessEqual(
            astar_stats["nodes_expanded"],
            dijkstra_stats["nodes_expanded"]
        )
    
    def test_compare_with_dijkstra(self):
        """Test the compare_with_dijkstra method."""
        comparison = self.pathfinder.compare_with_dijkstra("LAX", "JFK")
        
        self.assertIn("source", comparison)
        self.assertIn("destination", comparison)
        self.assertIn("dijkstra", comparison)
        self.assertIn("astar", comparison)
        self.assertIn("comparison", comparison)
        
        self.assertEqual(comparison["source"], "LAX")
        self.assertEqual(comparison["destination"], "JFK")
        
        self.assertTrue(comparison["comparison"]["paths_are_optimal"])
    
    def test_explored_nodes_field_populated(self):
        """Test that explored_nodes field is correctly populated in last_run_stats."""
        path, _ = self.pathfinder.find_shortest_path("LAX", "JFK")
        stats = self.pathfinder.last_run_stats
        
        # Check explored_nodes exists and is a set
        self.assertIn("explored_nodes", stats)
        self.assertIsInstance(stats["explored_nodes"], set)
        
        # Check it's not empty for valid path
        self.assertGreater(len(stats["explored_nodes"]), 0)
        
        # Check that source and destination are in explored nodes
        self.assertIn("LAX", stats["explored_nodes"])
        
        # Check nodes_expanded matches explored_nodes length
        self.assertEqual(stats["nodes_expanded"], len(stats["explored_nodes"]))
    
    def test_came_from_field_populated(self):
        """Test that came_from field is correctly populated in last_run_stats."""
        path, _ = self.pathfinder.find_shortest_path("LAX", "JFK")
        stats = self.pathfinder.last_run_stats
        
        # Check came_from exists and is a dict
        self.assertIn("came_from", stats)
        self.assertIsInstance(stats["came_from"], dict)
        
        # Check it's not empty for multi-hop path
        self.assertGreater(len(stats["came_from"]), 0)
        
        # Check that destination has a parent (unless direct route)
        if len(path) > 2:  # Multi-hop path
            self.assertIn("JFK", stats["came_from"])
        
        # Verify parent-child relationships are valid
        for child, parent in stats["came_from"].items():
            self.assertIn(child, self.network.airports)
            self.assertIn(parent, self.network.airports)
    
    def test_explored_nodes_same_source_destination(self):
        """Test explored_nodes when source equals destination."""
        path, _ = self.pathfinder.find_shortest_path("LAX", "LAX")
        stats = self.pathfinder.last_run_stats
        
        # Should return immediately without exploration
        self.assertEqual(path, ["LAX"])
        
        # Stats might not be populated for trivial case
        # This is implementation-dependent, just verify it doesn't crash
        self.assertIsInstance(stats, dict)
    
    def test_explored_nodes_no_path_exists(self):
        """Test explored_nodes when no path exists between airports."""
        # Create isolated airport with no connections
        isolated = Airport(
            code="ISO",
            name="Isolated Airport",
            city="Nowhere",
            country="United States",
            latitude=0.0,
            longitude=0.0
        )
        self.network.add_airport(isolated)
        
        path, cost = self.pathfinder.find_shortest_path("LAX", "ISO")
        stats = self.pathfinder.last_run_stats
        
        # Should return empty path and infinite cost
        self.assertEqual(path, [])
        self.assertEqual(cost, float('inf'))
        
        # explored_nodes should still be tracked
        if "explored_nodes" in stats:
            self.assertIsInstance(stats["explored_nodes"], set)
            # Should have explored some nodes trying to find path
            self.assertGreater(len(stats["explored_nodes"]), 0)
    
    def test_came_from_reflects_actual_path(self):
        """Test that came_from can reconstruct the found path."""
        path, _ = self.pathfinder.find_shortest_path("LAX", "JFK")
        stats = self.pathfinder.last_run_stats
        
        if len(path) > 1:
            came_from = stats["came_from"]
            
            # Reconstruct path from came_from
            reconstructed = []
            current = "JFK"
            while current is not None:
                reconstructed.insert(0, current)
                current = came_from.get(current)
            
            # Reconstructed path should match found path
            self.assertEqual(reconstructed, path)


if __name__ == "__main__":
    unittest.main()
