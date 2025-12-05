from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class Airport:
    code: str
    name: str
    city: str
    country: str
    latitude: float
    longitude: float

@dataclass
class Route:
    source: str
    destination: str
    distance: float

class FlightNetwork:
    def __init__(self):
        self.airports: Dict[str, Airport] = {}
        self.adjacency_list: Dict[str, List[Tuple[str, float]]] = {}

    def add_airport(self, airport: Airport) -> None:
        self.airports[airport.code] = airport
        self.adjacency_list.setdefault(airport.code, [])

    def add_route(self, route: Route) -> None:
        self.adjacency_list.setdefault(route.source, [])
        self.adjacency_list[route.source].append((route.destination, route.distance))

    def get_neighbors(self, airport_code: str) -> List[Tuple[str, float]]:
        return self.adjacency_list.get(airport_code, [])

    def get_airport(self, code: str) -> Optional[Airport]:
        return self.airports.get(code)
    
    def remove_edge(self, source: str, destination: str) -> Optional[float]:
        """
        Remove an edge from the network and return its weight.
        
        Args:
            source: Source airport code
            destination: Destination airport code
            
        Returns:
            Weight of removed edge, or None if edge doesn't exist
        """
        if source in self.adjacency_list:
            for i, (dest, weight) in enumerate(self.adjacency_list[source]):
                if dest == destination:
                    self.adjacency_list[source].pop(i)
                    return weight
        return None
    
    def add_edge(self, source: str, destination: str, weight: float) -> None:
        """
        Add an edge to the network.
        
        Args:
            source: Source airport code
            destination: Destination airport code
            weight: Edge weight
        """
        self.adjacency_list.setdefault(source, [])
        self.adjacency_list[source].append((destination, weight))
    
    def get_edge_weight(self, source: str, destination: str) -> Optional[float]:
        """
        Get weight of edge between two airports.
        
        Args:
            source: Source airport code
            destination: Destination airport code
            
        Returns:
            Edge weight or None if edge doesn't exist
        """
        if source in self.adjacency_list:
            for dest, weight in self.adjacency_list[source]:
                if dest == destination:
                    return weight
        return None

__all__ = ["FlightNetwork", "Airport", "Route"]
