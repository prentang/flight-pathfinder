"""
Standalone test suite for Dijkstra's algorithm implementation.
Tests various scenarios without external dependencies.
"""
import unittest
import sys
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass


# Define required classes inline to avoid import issues
@dataclass
class Airport:
    """Represents an airport node in the flight network."""
    code: str
    routes: List['Route'] = None
    
    def __post_init__(self):
        if self.routes is None:
            self.routes = []


@dataclass
class Route:
    """Represents a directed edge (route) between two airports."""
    destination: str
    weight: float


class FlightNetwork:
    """Graph representation of flight network."""
    
    def __init__(self):
        self.airports: Dict[str, str] = {}
        self._airport_objects: Dict[str, Airport] = {}
    
    def add_airport(self, code: str):
        self.airports[code] = code
        self._airport_objects[code] = Airport(code=code)
    
    def add_route(self, source: str, destination: str, weight: float):
        route = Route(destination=destination, weight=weight)
        self._airport_objects[source].routes.append(route)
    
    def get_airport(self, code: str) -> Airport:
        return self._airport_objects[code]


# Add the parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# Mock ALL the modules BEFORE importing anything from algorithms
import types

# Mock models.graph
models = types.ModuleType('models')
models.graph = types.ModuleType('models.graph')
models.graph.FlightNetwork = FlightNetwork
models.graph.Airport = Airport
models.graph.Route = Route
sys.modules['models'] = models
sys.modules['models.graph'] = models.graph

# Mock data.route_loader (needed by a_star which gets imported via algorithms/__init__.py)
def mock_calculate_distance(lat1, lon1, lat2, lon2):
    """Mock distance calculation"""
    import math
    return math.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)

data = types.ModuleType('data')
data.route_loader = types.ModuleType('data.route_loader')
data.route_loader.calculate_distance = mock_calculate_distance
sys.modules['data'] = data
sys.modules['data.route_loader'] = data.route_loader

# Mock data.airport_loader (also needed by a_star)
data.airport_loader = types.ModuleType('data.airport_loader')
data.airport_loader.load_airport_data = lambda: {}
data.airport_loader.get_us_airports = lambda: []
data.airport_loader.get_airport_coordinates = lambda x: (0.0, 0.0)
data.airport_loader.validate_airport_code = lambda x: True
sys.modules['data.airport_loader'] = data.airport_loader

# Now we can safely import DijkstraPathFinder
from algorithms.dijkstra import DijkstraPathFinder


class TestDijkstraPathFinder(unittest.TestCase):
    """Test cases for Dijkstra's algorithm implementation."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.network = FlightNetwork()
        
        # Add sample airports
        airports = ["LAX", "JFK", "CHI", "DFW", "ATL", "MIA", "SEA", "BOS"]
        for code in airports:
            self.network.add_airport(code)
        
        # Add sample routes with known distances
        routes_data = [
            ("LAX", "CHI", 1745),
            ("LAX", "DFW", 1235),
            ("LAX", "SEA", 954),
            ("CHI", "JFK", 740),
            ("CHI", "DFW", 800),
            ("DFW", "JFK", 1380),
            ("DFW", "ATL", 730),
            ("DFW", "MIA", 1110),
            ("ATL", "JFK", 760),
            ("ATL", "MIA", 595),
            ("SEA", "CHI", 1737),
            ("BOS", "JFK", 187),
        ]
        
        for source, dest, weight in routes_data:
            self.network.add_route(source, dest, weight)
        
        self.pathfinder = DijkstraPathFinder(self.network)
    
    def test_shortest_path_direct_route(self):
        """Test shortest path for directly connected airports."""
        path, distance = self.pathfinder.find_shortest_path("LAX", "CHI")
        
        self.assertEqual(len(path), 2)
        self.assertEqual(path[0], "LAX")
        self.assertEqual(path[-1], "CHI")
        self.assertEqual(distance, 1745)
        print("\n✓ Test 1 PASSED: Direct route (LAX -> CHI)")
    
    def test_shortest_path_multi_hop(self):
        """Test shortest path requiring multiple hops."""
        path, distance = self.pathfinder.find_shortest_path("LAX", "ATL")
        
        # LAX -> DFW -> ATL (1965) is shorter than LAX -> CHI -> DFW -> ATL
        self.assertEqual(path, ["LAX", "DFW", "ATL"])
        self.assertEqual(distance, 1965)
        print(f"✓ Test 2 PASSED: Multi-hop route (LAX -> ATL): {' -> '.join(path)}, distance: {distance}")
    
    def test_no_path_exists(self):
        """Test behavior when no path exists between airports."""
        # Add disconnected airport
        self.network.add_airport("ISOLATED")
        
        path, distance = self.pathfinder.find_shortest_path("LAX", "ISOLATED")
        
        self.assertEqual(path, [])
        self.assertEqual(distance, float('inf'))
        print("✓ Test 3 PASSED: No path exists")
    
    def test_same_source_destination(self):
        """Test pathfinding when source equals destination."""
        path, distance = self.pathfinder.find_shortest_path("LAX", "LAX")
        
        self.assertEqual(path, ["LAX"])
        self.assertEqual(distance, 0.0)
        print("✓ Test 4 PASSED: Source equals destination")
    
    def test_invalid_airports(self):
        """Test behavior with invalid airport codes."""
        # Test with non-existent source
        with self.assertRaises(ValueError) as context:
            self.pathfinder.find_shortest_path("INVALID", "LAX")
        self.assertIn("not found", str(context.exception))
        
        # Test with non-existent destination
        with self.assertRaises(ValueError) as context:
            self.pathfinder.find_shortest_path("LAX", "INVALID")
        self.assertIn("not found", str(context.exception))
        
        print("✓ Test 5 PASSED: Invalid airport handling")
    
    def test_algorithm_optimality(self):
        """Test that Dijkstra finds truly optimal paths."""
        # Path from LAX to JFK
        # Option 1: LAX -> CHI -> JFK = 1745 + 740 = 2485
        # Option 2: LAX -> DFW -> JFK = 1235 + 1380 = 2615
        # Option 3: LAX -> DFW -> ATL -> JFK = 1235 + 730 + 760 = 2725
        
        path, distance = self.pathfinder.find_shortest_path("LAX", "JFK")
        
        self.assertEqual(path, ["LAX", "CHI", "JFK"])
        self.assertEqual(distance, 2485)
        print(f"✓ Test 6 PASSED: Algorithm optimality (LAX -> JFK): {' -> '.join(path)}, distance: {distance}")
    
    def test_all_shortest_paths(self):
        """Test finding shortest paths to all destinations."""
        all_paths = self.pathfinder.find_all_shortest_paths("LAX")
        
        # Verify paths to reachable airports
        self.assertIn("JFK", all_paths)
        self.assertIn("CHI", all_paths)
        self.assertIn("DFW", all_paths)
        self.assertIn("ATL", all_paths)
        
        # Check specific path optimality
        self.assertEqual(all_paths["CHI"][1], 1745)
        self.assertEqual(all_paths["JFK"][0], ["LAX", "CHI", "JFK"])
        self.assertEqual(all_paths["JFK"][1], 2485)
        self.assertEqual(all_paths["ATL"][0], ["LAX", "DFW", "ATL"])
        self.assertEqual(all_paths["ATL"][1], 1965)
        
        print("✓ Test 7 PASSED: Find all shortest paths")
    
    def test_k_shortest_paths(self):
        """Test finding k shortest paths between airports."""
        k_paths = self.pathfinder.find_k_shortest_paths("LAX", "JFK", k=3)
        
        # Verify we got results
        self.assertGreater(len(k_paths), 0)
        
        # Verify paths are sorted by distance
        for i in range(len(k_paths) - 1):
            self.assertLessEqual(k_paths[i][1], k_paths[i + 1][1])
        
        # Verify all paths are different
        paths_only = [tuple(path) for path, _ in k_paths]
        self.assertEqual(len(paths_only), len(set(paths_only)))
        
        # First path should be the shortest
        self.assertEqual(k_paths[0][0], ["LAX", "CHI", "JFK"])
        self.assertEqual(k_paths[0][1], 2485)
        
        print(f"✓ Test 8 PASSED: K shortest paths (k=3)")
        for i, (path, dist) in enumerate(k_paths, 1):
            print(f"  Path {i}: {' -> '.join(path)}, distance: {dist}")
    
    def test_k_shortest_paths_invalid_k(self):
        """Test k-shortest paths with invalid k value."""
        with self.assertRaises(ValueError):
            self.pathfinder.find_k_shortest_paths("LAX", "JFK", k=0)
        
        with self.assertRaises(ValueError):
            self.pathfinder.find_k_shortest_paths("LAX", "JFK", k=-1)
        
        print("✓ Test 9 PASSED: Invalid k value handling")
    
    def test_path_reconstruction(self):
        """Test internal path reconstruction logic."""
        previous = {
            "B": "A",
            "C": "B",
            "D": "C"
        }
        
        path = self.pathfinder._reconstruct_path(previous, "D")
        self.assertEqual(path, ["A", "B", "C", "D"])
        print("✓ Test 10 PASSED: Path reconstruction")
    
    def test_algorithm_stats_tracking(self):
        """Test that algorithm statistics are properly tracked."""
        path, distance = self.pathfinder.find_shortest_path("LAX", "JFK")
        
        stats = self.pathfinder.get_algorithm_stats()
        
        # Verify all required stats are present
        required_stats = ["nodes_expanded", "nodes_generated", "execution_time", "path_cost"]
        for stat in required_stats:
            self.assertIn(stat, stats)
        
        # Verify stats have reasonable values
        self.assertGreater(stats["nodes_expanded"], 0)
        self.assertGreaterEqual(stats["nodes_generated"], 0)
        self.assertGreaterEqual(stats["execution_time"], 0)
        self.assertEqual(stats["path_cost"], distance)
        
        print(f"✓ Test 11 PASSED: Algorithm stats tracking")
        print(f"  Nodes expanded: {stats['nodes_expanded']}")
        print(f"  Nodes generated: {stats['nodes_generated']}")
        print(f"  Execution time: {stats['execution_time']*1000:.2f} ms")
        print(f"  Path cost: {stats['path_cost']}")
    
    def test_complex_network(self):
        """Test with more complex path scenarios."""
        # Add more airports and routes
        self.network.add_airport("SFO")
        self.network.add_airport("DEN")
        
        self.network.add_route("SFO", "LAX", 337)
        self.network.add_route("SFO", "SEA", 679)
        self.network.add_route("SFO", "DEN", 967)
        self.network.add_route("DEN", "CHI", 888)
        self.network.add_route("DEN", "DFW", 641)
        
        path, distance = self.pathfinder.find_shortest_path("SFO", "JFK")
        
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], "SFO")
        self.assertEqual(path[-1], "JFK")
        
        print(f"✓ Test 12 PASSED: Complex network (SFO -> JFK): {' -> '.join(path)}, distance: {distance}")
    
    def test_multiple_equal_paths(self):
        """Test behavior when multiple paths have equal cost."""
        # Create a diamond network
        self.network.add_airport("A")
        self.network.add_airport("B")
        self.network.add_airport("C")
        self.network.add_airport("D")
        
        # A -> B -> D and A -> C -> D both cost 10
        self.network.add_route("A", "B", 5)
        self.network.add_route("A", "C", 5)
        self.network.add_route("B", "D", 5)
        self.network.add_route("C", "D", 5)
        
        path, distance = self.pathfinder.find_shortest_path("A", "D")
        
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], "A")
        self.assertEqual(path[-1], "D")
        self.assertEqual(distance, 10)
        self.assertIn(path[1], ["B", "C"])  # Either path is valid
        
        print(f"✓ Test 13 PASSED: Multiple equal-cost paths: {' -> '.join(path)}, distance: {distance}")


class TestDijkstraEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def setUp(self):
        """Set up minimal test network."""
        self.network = FlightNetwork()
        self.network.add_airport("A")
        self.pathfinder = DijkstraPathFinder(self.network)
    
    def test_single_airport_network(self):
        """Test network with only one airport."""
        path, distance = self.pathfinder.find_shortest_path("A", "A")
        self.assertEqual(path, ["A"])
        self.assertEqual(distance, 0.0)
        print("\n✓ Edge Test 1 PASSED: Single airport network")
    
    def test_empty_stats_before_run(self):
        """Test getting stats before running algorithm."""
        stats = self.pathfinder.get_algorithm_stats()
        self.assertIsInstance(stats, dict)
        print("✓ Edge Test 2 PASSED: Empty stats before run")
    
    def test_zero_weight_edges(self):
        """Test handling of zero-weight edges."""
        self.network.add_airport("B")
        self.network.add_route("A", "B", 0)
        
        path, distance = self.pathfinder.find_shortest_path("A", "B")
        self.assertEqual(path, ["A", "B"])
        self.assertEqual(distance, 0)
        print("✓ Edge Test 3 PASSED: Zero-weight edges")


def run_comprehensive_tests():
    """Run all tests and display results."""
    print("\n" + "="*70)
    print(" DIJKSTRA'S ALGORITHM - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")
    print("="*70 + "\n")
    
    # Run main tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDijkstraPathFinder))
    suite.addTests(loader.loadTestsFromTestCase(TestDijkstraEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED")
    
    print("="*70 + "\n")
    
    return result


if __name__ == "__main__":
    result = run_comprehensive_tests()
    sys.exit(0 if result.wasSuccessful() else 1)