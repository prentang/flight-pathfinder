"""
Example script demonstrating visualization capabilities with test data.
Run this to see the visualization functions in action.
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from models.graph import FlightNetwork, Airport, Route
from algorithms.dijkstra import DijkstraPathFinder
from algorithms.a_star import AStarPathFinder
from visualization.path_plotter import (
    plot_flight_path,
    plot_multiple_paths,
    plot_network_graph
)


def create_test_network():
    """Create a test flight network with US airports."""
    network = FlightNetwork()
    
    # Add major US airports with coordinates
    airports_data = [
        ("LAX", "Los Angeles International", "Los Angeles", "United States", 33.9425, -118.408),
        ("JFK", "John F. Kennedy International", "New York", "United States", 40.6413, -73.7781),
        ("ORD", "O'Hare International", "Chicago", "United States", 41.9742, -87.9073),
        ("DFW", "Dallas/Fort Worth International", "Dallas", "United States", 32.8998, -97.0403),
        ("ATL", "Hartsfield-Jackson Atlanta International", "Atlanta", "United States", 33.6407, -84.4277),
        ("DEN", "Denver International", "Denver", "United States", 39.8561, -104.6737),
        ("SFO", "San Francisco International", "San Francisco", "United States", 37.6213, -122.379),
        ("SEA", "Seattle-Tacoma International", "Seattle", "United States", 47.4502, -122.3088),
        ("MIA", "Miami International", "Miami", "United States", 25.7959, -80.2870),
        ("BOS", "Logan International", "Boston", "United States", 42.3656, -71.0096),
        ("LAS", "Harry Reid International", "Las Vegas", "United States", 36.0840, -115.1537),
        ("PHX", "Phoenix Sky Harbor International", "Phoenix", "United States", 33.4484, -112.0740),
    ]
    
    for code, name, city, country, lat, lon in airports_data:
        airport = Airport(
            code=code,
            name=name,
            city=city,
            country=country,
            latitude=lat,
            longitude=lon
        )
        network.add_airport(airport)
    
    # Add routes with approximate distances (in km)
    routes_data = [
        ("LAX", "SFO", 543),
        ("LAX", "LAS", 370),
        ("LAX", "PHX", 600),
        ("LAX", "DEN", 1400),
        ("LAX", "DFW", 1990),
        ("LAX", "ORD", 2800),
        ("SFO", "SEA", 1090),
        ("SFO", "DEN", 1500),
        ("SFO", "ORD", 2984),
        ("SEA", "DEN", 1650),
        ("LAS", "PHX", 410),
        ("LAS", "DEN", 970),
        ("PHX", "DFW", 1423),
        ("PHX", "DEN", 1010),
        ("DEN", "DFW", 1070),
        ("DEN", "ORD", 1480),
        ("DEN", "ATL", 2130),
        ("DFW", "ORD", 1290),
        ("DFW", "ATL", 1160),
        ("DFW", "MIA", 1760),
        ("DFW", "JFK", 2250),
        ("ORD", "JFK", 1190),
        ("ORD", "BOS", 1370),
        ("ORD", "ATL", 950),
        ("ATL", "MIA", 970),
        ("ATL", "JFK", 1210),
        ("ATL", "BOS", 1510),
        ("JFK", "BOS", 300),
        ("JFK", "MIA", 2050),
    ]
    
    # Add bidirectional routes
    for source, dest, distance in routes_data:
        network.add_route(Route(source=source, destination=dest, distance=distance))
        network.add_route(Route(source=dest, destination=source, distance=distance))
    
    return network


def demo_single_path_visualization():
    """Demonstrate single path visualization."""
    print("\n" + "="*60)
    print("DEMO 1: Single Path Visualization")
    print("="*60)
    
    network = create_test_network()
    pathfinder = DijkstraPathFinder(network)
    
    # Find path from LAX to JFK
    source, destination = "LAX", "JFK"
    path, distance = pathfinder.find_shortest_path(source, destination)
    
    print(f"\nShortest path from {source} to {destination}:")
    print(f"Route: {' → '.join(path)}")
    print(f"Total distance: {distance:.0f} km")
    
    print("\nOpening interactive map...")
    plot_flight_path(
        network, 
        path, 
        title=f"Shortest Flight Path: {source} → {destination} ({distance:.0f} km)"
    )


def demo_multiple_paths_comparison():
    """Demonstrate comparison of Dijkstra vs A* paths."""
    print("\n" + "="*60)
    print("DEMO 2: Multiple Paths Comparison (Dijkstra vs A*)")
    print("="*60)
    
    network = create_test_network()
    dijkstra = DijkstraPathFinder(network)
    astar = AStarPathFinder(network)
    
    source, destination = "LAX", "BOS"
    
    # Find paths with both algorithms
    dijkstra_path, dijkstra_dist = dijkstra.find_shortest_path(source, destination)
    astar_path, astar_dist = astar.find_shortest_path(source, destination, heuristic="haversine")
    
    print(f"\nComparing paths from {source} to {destination}:")
    print(f"\nDijkstra: {' → '.join(dijkstra_path)}")
    print(f"Distance: {dijkstra_dist:.0f} km")
    print(f"Nodes expanded: {dijkstra.get_algorithm_stats()['nodes_expanded']}")
    
    print(f"\nA*: {' → '.join(astar_path)}")
    print(f"Distance: {astar_dist:.0f} km")
    print(f"Nodes expanded: {astar.get_algorithm_stats()['nodes_expanded']}")
    
    # Find alternative k-shortest paths
    k_paths = dijkstra.find_k_shortest_paths(source, destination, k=3)
    
    all_paths = [dijkstra_path, astar_path]
    labels = [
        f"Dijkstra ({dijkstra_dist:.0f} km)",
        f"A* ({astar_dist:.0f} km)"
    ]
    
    if len(k_paths) > 1:
        all_paths.append(k_paths[1][0])
        labels.append(f"Alternative Path ({k_paths[1][1]:.0f} km)")
    
    print("\nOpening comparison map...")
    plot_multiple_paths(network, all_paths, labels)


def demo_network_visualization():
    """Demonstrate full network visualization with highlighted path."""
    print("\n" + "="*60)
    print("DEMO 3: Full Network Graph Visualization")
    print("="*60)
    
    network = create_test_network()
    pathfinder = DijkstraPathFinder(network)
    
    # Find an interesting path to highlight
    source, destination = "SEA", "MIA"
    path, distance = pathfinder.find_shortest_path(source, destination)
    
    print(f"\nNetwork statistics:")
    print(f"Total airports: {len(network.airports)}")
    
    total_routes = sum(len(network.get_neighbors(code)) for code in network.airports)
    print(f"Total routes: {total_routes}")
    
    print(f"\nHighlighting path: {' → '.join(path)}")
    print(f"Distance: {distance:.0f} km")
    
    print("\nOpening network graph...")
    plot_network_graph(network, highlight_path=path)


def demo_all():
    """Run all demonstrations."""
    print("\n" + "="*60)
    print("FLIGHT PATH VISUALIZATION DEMONSTRATIONS")
    print("="*60)
    print("\nThis script will open 3 interactive Plotly maps:")
    print("1. Single path visualization (LAX → JFK)")
    print("2. Multiple paths comparison (LAX → BOS)")
    print("3. Full network graph (with SEA → MIA highlighted)")
    print("\nEach map will open in your default web browser.")
    print("Close each browser tab to proceed to the next demo.")
    
    input("\nPress Enter to start Demo 1...")
    demo_single_path_visualization()
    
    input("\nPress Enter to start Demo 2...")
    demo_multiple_paths_comparison()
    
    input("\nPress Enter to start Demo 3...")
    demo_network_visualization()
    
    print("\n" + "="*60)
    print("All demonstrations complete!")
    print("="*60)


if __name__ == "__main__":
    demo_all()
