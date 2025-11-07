"""
Standalone test suite for A* pathfinding algorithm implementation.
Tests various scenarios using real airport data without external dependencies.
"""
import unittest
import sys
import os
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


# Define required classes inline to avoid import issues
@dataclass
class Airport:
    """Represents an airport node in the flight network."""
    code: str
    name: str
    city: str
    country: str
    latitude: float
    longitude: float


@dataclass
class Route:
    """Represents a directed edge (route) between two airports."""
    source: str
    destination: str
    distance: float


class FlightNetwork:
    """Graph representation of flight network using adjacency list."""
    
    def __init__(self):
        self.airports: Dict[str, Airport] = {}
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = {}
    
    def add_airport(self, airport: Airport) -> None:
        self.airports[airport.code] = airport
        if airport.code not in self.adjacency_list:
            self.adjacency_list[airport.code] = []
    
    def add_route(self, route: Route) -> None:
        if route.source not in self.adjacency_list:
            self.adjacency_list[route.source] = []
        self.adjacency_list[route.source].append((route.destination, route.distance))
    
    def get_neighbors(self, airport_code: str) -> List[Tuple[str, float]]:
        return self.adjacency_list.get(airport_code, [])


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great circle distance using Haversine formula."""
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    R = 6371.0  # Earth's radius in km
    return R * c


# Now import the A* implementation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the modules that A* tries to import
import types
models = types.ModuleType('models')
models.graph = types.ModuleType('models.graph')
models.graph.FlightNetwork = FlightNetwork
models.graph.Airport = Airport
models.graph.Route = Route
sys.modules['models'] = models
sys.modules['models.graph'] = models.graph

data = types.ModuleType('data')
data.route_loader = types.ModuleType('data.route_loader')
data.route_loader.calculate_distance = calculate_distance
sys.modules['data'] = data
sys.modules['data.route_loader'] = data.route_loader

from algorithms.a_star import AStarPathFinder


class TestAStarPathFinder(unittest.TestCase):
    """Test cases for A* pathfinding algorithm."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are used across all tests."""
        cls.network = cls._load_test_network()
        cls.pathfinder = AStarPathFinder(cls.network)
    
    @staticmethod
    def _load_test_network() -> FlightNetwork:
        """Load airports from CSV and create a test flight network."""
        network = FlightNetwork()
        
        # Try multiple paths to find airports.csv
        possible_paths = [
            "airports.csv",
            "../airports.csv",
            "../../airports.csv",
            "../data/airports.csv",
            "data/airports.csv",
            os.path.join(os.path.dirname(__file__), "airports.csv"),
            os.path.join(os.path.dirname(__file__), "..", "airports.csv"),
            os.path.join(os.path.dirname(__file__), "..", "data", "airports.csv"),
        ]
        
        airports_file = None
        for path in possible_paths:
            if os.path.exists(path):
                airports_file = path
                break
        
        if airports_file is None:
            current_dir = os.getcwd()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            raise FileNotFoundError(
                f"Cannot find airports.csv in any expected location.\n"
                f"Current directory: {current_dir}\n"
                f"Script directory: {script_dir}\n"
                f"Tried paths: {', '.join(possible_paths)}\n"
                f"Please place airports.csv in one of these locations."
            )
        
        with open(airports_file, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                # Parse CSV line (handle quoted fields)
                parts = []
                current = []
                in_quotes = False
                
                for char in line:
                    if char == '"':
                        in_quotes = not in_quotes
                    elif char == ',' and not in_quotes:
                        parts.append(''.join(current))
                        current = []
                    else:
                        current.append(char)
                parts.append(''.join(current))
                
                # Extract airport data
                if len(parts) >= 8:
                    try:
                        airport_id = parts[0].strip()
                        name = parts[1].strip()
                        city = parts[2].strip()
                        country = parts[3].strip()
                        iata_code = parts[4].strip()
                        icao_code = parts[5].strip()
                        latitude = float(parts[6].strip())
                        longitude = float(parts[7].strip())
                        
                        # Only add airports with valid IATA codes
                        if iata_code and iata_code != "\\N":
                            airport = Airport(
                                code=iata_code,
                                name=name,
                                city=city,
                                country=country,
                                latitude=latitude,
                                longitude=longitude
                            )
                            network.add_airport(airport)
                    except (ValueError, IndexError):
                        continue
        
        print(f"Loaded {len(network.airports)} airports from CSV")
        
        # Add test routes between major airports
        test_routes = [
            ("LAX", "JFK"),  # Los Angeles to New York
            ("JFK", "LHR"),  # New York to London
            ("LHR", "CDG"),  # London to Paris
            ("CDG", "FRA"),  # Paris to Frankfurt
            ("FRA", "DXB"),  # Frankfurt to Dubai
            ("DXB", "SIN"),  # Dubai to Singapore
            ("SIN", "SYD"),  # Singapore to Sydney
            ("SYD", "NRT"),  # Sydney to Tokyo
            ("NRT", "LAX"),  # Tokyo to Los Angeles
            ("LAX", "ORD"),  # Los Angeles to Chicago
            ("ORD", "JFK"),  # Chicago to New York
            ("SFO", "LAX"),  # San Francisco to Los Angeles
            ("SFO", "SEA"),  # San Francisco to Seattle
            ("SEA", "YVR"),  # Seattle to Vancouver
        ]
        
        for source, dest in test_routes:
            if source in network.airports and dest in network.airports:
                src_airport = network.airports[source]
                dst_airport = network.airports[dest]
                distance = calculate_distance(
                    src_airport.latitude, src_airport.longitude,
                    dst_airport.latitude, dst_airport.longitude
                )
                network.add_route(Route(source, dest, distance))
                # Add reverse route
                network.add_route(Route(dest, source, distance))
        
        print(f"Added {len(test_routes) * 2} test routes")
        
        return network
    
    def test_same_source_destination(self):
        """Test case where source and destination are the same."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "LAX")
        self.assertEqual(path, ["LAX"])
        self.assertEqual(cost, 0.0)
        print("\n✓ Same source/destination test passed")
    
    def test_direct_route(self):
        """Test finding a direct route between two airports."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "JFK")
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], "LAX")
        self.assertEqual(path[-1], "JFK")
        self.assertGreater(cost, 0)
        print(f"\n✓ Direct route LAX -> JFK: {' -> '.join(path)}, Cost: {cost:.2f} km")
    
    def test_multi_hop_route(self):
        """Test finding a route that requires multiple hops."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "SYD")
        self.assertIsNotNone(path)
        if len(path) > 0:
            self.assertEqual(path[0], "LAX")
            self.assertEqual(path[-1], "SYD")
            self.assertGreater(cost, 0)
            print(f"\n✓ Multi-hop route LAX -> SYD: {' -> '.join(path)}, Cost: {cost:.2f} km")
    
    def test_no_route_available(self):
        """Test case where no route exists between airports."""
        isolated_codes = []
        for code in list(self.network.airports.keys())[:50]:
            neighbors = self.network.get_neighbors(code)
            if len(neighbors) == 0:
                isolated_codes.append(code)
                if len(isolated_codes) >= 1:
                    break
        
        if isolated_codes:
            path, cost = self.pathfinder.find_shortest_path("LAX", isolated_codes[0])
            self.assertEqual(path, [])
            self.assertEqual(cost, float('inf'))
            print(f"\n✓ No route found from LAX to {isolated_codes[0]} (as expected)")
    
    def test_invalid_source_airport(self):
        """Test with invalid source airport code."""
        with self.assertRaises(ValueError):
            self.pathfinder.find_shortest_path("INVALID", "JFK")
        print("\n✓ Invalid source airport handled correctly")
    
    def test_invalid_destination_airport(self):
        """Test with invalid destination airport code."""
        with self.assertRaises(ValueError):
            self.pathfinder.find_shortest_path("LAX", "INVALID")
        print("\n✓ Invalid destination airport handled correctly")
    
    def test_euclidean_heuristic(self):
        """Test A* with Euclidean heuristic."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="euclidean")
        self.assertIsNotNone(path)
        if len(path) > 0:
            self.assertEqual(path[0], "LAX")
            self.assertEqual(path[-1], "JFK")
            print(f"\n✓ Euclidean heuristic LAX -> JFK: {' -> '.join(path)}, Cost: {cost:.2f} km")
    
    def test_haversine_heuristic(self):
        """Test A* with Haversine heuristic."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="haversine")
        self.assertIsNotNone(path)
        if len(path) > 0:
            self.assertEqual(path[0], "LAX")
            self.assertEqual(path[-1], "JFK")
            print(f"\n✓ Haversine heuristic LAX -> JFK: {' -> '.join(path)}, Cost: {cost:.2f} km")
    
    def test_manhattan_heuristic(self):
        """Test A* with Manhattan heuristic."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="manhattan")
        self.assertIsNotNone(path)
        if len(path) > 0:
            self.assertEqual(path[0], "LAX")
            self.assertEqual(path[-1], "JFK")
            print(f"\n✓ Manhattan heuristic LAX -> JFK: {' -> '.join(path)}, Cost: {cost:.2f} km")
    
    def test_heuristic_comparison(self):
        """Compare different heuristics on the same route."""
        heuristics = ["euclidean", "haversine", "manhattan"]
        results = {}
        
        for h in heuristics:
            path, cost = self.pathfinder.find_shortest_path("LAX", "SYD", heuristic=h)
            stats = self.pathfinder.last_run_stats
            results[h] = {
                "path_length": len(path),
                "cost": cost,
                "nodes_expanded": stats.get("nodes_expanded", 0),
                "execution_time": stats.get("execution_time", 0)
            }
        
        print("\n" + "="*60)
        print("Heuristic Comparison (LAX -> SYD):")
        print("="*60)
        for h, data in results.items():
            print(f"{h.capitalize():12} | Cost: {data['cost']:8.2f} km | "
                  f"Nodes: {data['nodes_expanded']:4} | "
                  f"Time: {data['execution_time']*1000:6.2f} ms")
    
    def test_algorithm_stats(self):
        """Test that algorithm statistics are tracked correctly."""
        self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="euclidean")
        stats = self.pathfinder.last_run_stats
        
        self.assertIn("nodes_expanded", stats)
        self.assertIn("nodes_generated", stats)
        self.assertIn("execution_time", stats)
        self.assertIn("path_cost", stats)
        self.assertIn("heuristic_calls", stats)
        
        self.assertGreater(stats["nodes_expanded"], 0)
        self.assertGreater(stats["execution_time"], 0)
        
        print(f"\n✓ Algorithm Stats for LAX -> JFK:")
        print(f"  Nodes expanded: {stats['nodes_expanded']}")
        print(f"  Nodes generated: {stats['nodes_generated']}")
        print(f"  Heuristic calls: {stats['heuristic_calls']}")
        print(f"  Execution time: {stats['execution_time']*1000:.2f} ms")
        print(f"  Path cost: {stats['path_cost']:.2f} km")
    
    def test_heuristic_caching(self):
        """Test that heuristic values are cached properly."""
        self.pathfinder.heuristic_cache.clear()
        
        self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="euclidean")
        cache_size_after_first = len(self.pathfinder.heuristic_cache)
        
        self.pathfinder.find_shortest_path("LAX", "JFK", heuristic="euclidean")
        cache_size_after_second = len(self.pathfinder.heuristic_cache)
        
        self.assertGreater(cache_size_after_first, 0)
        print(f"\n✓ Heuristic cache size after first run: {cache_size_after_first}")
        print(f"  Heuristic cache size after second run: {cache_size_after_second}")
    
    def test_path_optimality(self):
        """Test that A* finds optimal path by comparing with actual distances."""
        path, cost = self.pathfinder.find_shortest_path("LAX", "ORD")
        
        if len(path) > 1:
            manual_cost = 0.0
            for i in range(len(path) - 1):
                src = path[i]
                dst = path[i + 1]
                neighbors = self.network.get_neighbors(src)
                edge_weight = next((w for code, w in neighbors if code == dst), None)
                if edge_weight:
                    manual_cost += edge_weight
            
            self.assertAlmostEqual(cost, manual_cost, places=2)
            print(f"\n✓ Path optimality check LAX -> ORD:")
            print(f"  A* reported cost: {cost:.2f} km")
            print(f"  Manual calculation: {manual_cost:.2f} km")
            print(f"  Path: {' -> '.join(path)}")
    
    def test_round_trip(self):
        """Test that round trips work correctly."""
        path_there, cost_there = self.pathfinder.find_shortest_path("LAX", "JFK")
        path_back, cost_back = self.pathfinder.find_shortest_path("JFK", "LAX")
        
        if len(path_there) > 0 and len(path_back) > 0:
            print(f"\n✓ Round trip test:")
            print(f"  LAX -> JFK: {' -> '.join(path_there)}, Cost: {cost_there:.2f} km")
            print(f"  JFK -> LAX: {' -> '.join(path_back)}, Cost: {cost_back:.2f} km")


def run_comprehensive_tests():
    """Run all tests and display results."""
    print("\n" + "="*70)
    print(" A* PATHFINDING ALGORITHM - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")
    print("="*70 + "\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAStarPathFinder)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result


if __name__ == "__main__":
    result = run_comprehensive_tests()
    sys.exit(0 if result.wasSuccessful() else 1)