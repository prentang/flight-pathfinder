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

__all__ = ["FlightNetwork", "Airport", "Route"]
