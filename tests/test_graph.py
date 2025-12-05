"""
Test suite for flight network graph data structures.
"""
import unittest
from models.graph import FlightNetwork, Airport, Route


class TestAirport(unittest.TestCase):
    """Test cases for Airport data structure."""
    
    def test_airport_creation(self):
        """Test Airport object creation and initialization."""
        airport = Airport(
            code="LAX",
            name="Los Angeles International Airport",
            city="Los Angeles",
            country="United States",
            latitude=33.9425,
            longitude=-118.408
        )
        
        self.assertEqual(airport.code, "LAX")
        self.assertEqual(airport.name, "Los Angeles International Airport")
        self.assertEqual(airport.city, "Los Angeles")
        self.assertEqual(airport.country, "United States")
        self.assertEqual(airport.latitude, 33.9425)
        self.assertEqual(airport.longitude, -118.408)
    
    def test_airport_equality(self):
        """Test Airport equality."""
        airport1 = Airport(
            code="LAX",
            name="Los Angeles International Airport",
            city="Los Angeles",
            country="United States",
            latitude=33.9425,
            longitude=-118.408
        )
        
        airport2 = Airport(
            code="LAX",
            name="Los Angeles International Airport",
            city="Los Angeles",
            country="United States",
            latitude=33.9425,
            longitude=-118.408
        )
        
        airport3 = Airport(
            code="JFK",
            name="John F. Kennedy International Airport",
            city="New York",
            country="United States",
            latitude=40.6413,
            longitude=-73.7781
        )
        
        self.assertEqual(airport1, airport2)
        self.assertNotEqual(airport1, airport3)


class TestRoute(unittest.TestCase):
    """Test cases for Route data structure."""
    
    def test_route_creation(self):
        """Test Route object creation and initialization."""
        route = Route(
            source="LAX",
            destination="JFK",
            distance=3944.0
        )
        
        self.assertEqual(route.source, "LAX")
        self.assertEqual(route.destination, "JFK")
        self.assertEqual(route.distance, 3944.0)
    
    def test_route_equality(self):
        """Test Route equality."""
        route1 = Route(source="LAX", destination="JFK", distance=3944.0)
        route2 = Route(source="LAX", destination="JFK", distance=3944.0)
        route3 = Route(source="JFK", destination="LAX", distance=3944.0)
        
        self.assertEqual(route1, route2)
        self.assertNotEqual(route1, route3)


class TestFlightNetwork(unittest.TestCase):
    """Test cases for FlightNetwork graph structure."""
    
    def setUp(self):
        """Set up test fixtures for FlightNetwork tests."""
        self.network = FlightNetwork()
        
        self.lax = Airport(
            code="LAX",
            name="Los Angeles International Airport",
            city="Los Angeles",
            country="United States",
            latitude=33.9425,
            longitude=-118.408
        )
        
        self.jfk = Airport(
            code="JFK",
            name="John F. Kennedy International Airport",
            city="New York",
            country="United States",
            latitude=40.6413,
            longitude=-73.7781
        )
        
        self.ord = Airport(
            code="ORD",
            name="O'Hare International Airport",
            city="Chicago",
            country="United States",
            latitude=41.9742,
            longitude=-87.9073
        )
    
    def test_network_initialization(self):
        """Test FlightNetwork initialization."""
        network = FlightNetwork()
        self.assertIsInstance(network.airports, dict)
        self.assertIsInstance(network.adjacency_list, dict)
        self.assertEqual(len(network.airports), 0)
        self.assertEqual(len(network.adjacency_list), 0)
    
    def test_add_airport(self):
        """Test adding airports to the network."""
        self.network.add_airport(self.lax)
        
        self.assertIn("LAX", self.network.airports)
        self.assertEqual(self.network.airports["LAX"], self.lax)
        self.assertIn("LAX", self.network.adjacency_list)
        self.assertEqual(len(self.network.adjacency_list["LAX"]), 0)
        
        self.network.add_airport(self.jfk)
        self.assertEqual(len(self.network.airports), 2)
    
    def test_add_duplicate_airport(self):
        """Test adding duplicate airports."""
        self.network.add_airport(self.lax)
        self.network.add_airport(self.lax)
        
        self.assertEqual(len(self.network.airports), 1)
    
    def test_add_route(self):
        """Test adding routes to the network."""
        self.network.add_airport(self.lax)
        self.network.add_airport(self.jfk)
        
        route = Route(source="LAX", destination="JFK", distance=3944.0)
        self.network.add_route(route)
        
        neighbors = self.network.get_neighbors("LAX")
        self.assertEqual(len(neighbors), 1)
        self.assertEqual(neighbors[0], ("JFK", 3944.0))
    
    def test_add_multiple_routes(self):
        """Test adding multiple routes from one airport."""
        self.network.add_airport(self.lax)
        self.network.add_airport(self.jfk)
        self.network.add_airport(self.ord)
        
        route1 = Route(source="LAX", destination="JFK", distance=3944.0)
        route2 = Route(source="LAX", destination="ORD", distance=2800.0)
        
        self.network.add_route(route1)
        self.network.add_route(route2)
        
        neighbors = self.network.get_neighbors("LAX")
        self.assertEqual(len(neighbors), 2)
    
    def test_get_neighbors(self):
        """Test retrieving airport neighbors."""
        self.network.add_airport(self.lax)
        self.network.add_airport(self.jfk)
        
        route = Route(source="LAX", destination="JFK", distance=3944.0)
        self.network.add_route(route)
        
        neighbors = self.network.get_neighbors("LAX")
        self.assertIsInstance(neighbors, list)
        self.assertEqual(len(neighbors), 1)
        
        empty_neighbors = self.network.get_neighbors("JFK")
        self.assertEqual(len(empty_neighbors), 0)
        
        nonexistent_neighbors = self.network.get_neighbors("XXX")
        self.assertEqual(len(nonexistent_neighbors), 0)
    
    def test_get_airport(self):
        """Test airport lookup methods."""
        self.network.add_airport(self.lax)
        
        airport = self.network.get_airport("LAX")
        self.assertIsNotNone(airport)
        self.assertEqual(airport.code, "LAX")
        
        nonexistent = self.network.get_airport("XXX")
        self.assertIsNone(nonexistent)
    
    def test_network_with_bidirectional_routes(self):
        """Test network with bidirectional routes."""
        self.network.add_airport(self.lax)
        self.network.add_airport(self.jfk)
        
        route1 = Route(source="LAX", destination="JFK", distance=3944.0)
        route2 = Route(source="JFK", destination="LAX", distance=3944.0)
        
        self.network.add_route(route1)
        self.network.add_route(route2)
        
        lax_neighbors = self.network.get_neighbors("LAX")
        jfk_neighbors = self.network.get_neighbors("JFK")
        
        self.assertEqual(len(lax_neighbors), 1)
        self.assertEqual(len(jfk_neighbors), 1)
        self.assertEqual(lax_neighbors[0][0], "JFK")
        self.assertEqual(jfk_neighbors[0][0], "LAX")


if __name__ == "__main__":
    unittest.main()
