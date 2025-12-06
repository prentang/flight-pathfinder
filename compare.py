#!/usr/bin/env python3
"""
Compare Algorithms - Visualize Dijkstra vs A*

Usage:
    python compare.py LAX JFK
    python compare.py SEA MIA
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data.openflights.downloader import setup_openflights_data
from models.graph import FlightNetwork
from algorithms.dijkstra import DijkstraPathFinder
from algorithms.a_star import AStarPathFinder
from visualization.path_plotter import plot_multiple_paths


def compare_algorithms(source, destination):
    """Compare Dijkstra and A* algorithms."""
    source = source.upper()
    destination = destination.upper()
    
    # Load network
    print("Loading flight network...")
    us_airports_df, us_routes_df = setup_openflights_data()
    network = FlightNetwork()
    network.load_from_dataframes(us_airports_df, us_routes_df)
    print(f"Loaded {len(network.airports)} airports\n")
    
    # Validate airports
    if not network.get_airport(source) or not network.get_airport(destination):
        print(f"Error: One or both airports not found")
        return
    
    print(f"Comparing algorithms for {source} -> {destination}...\n")
    
    # Run Dijkstra
    print("Running Dijkstra's algorithm...")
    dijkstra = DijkstraPathFinder(network)
    dijkstra_path, dijkstra_dist = dijkstra.find_shortest_path(source, destination)
    dijkstra_stats = dijkstra.get_algorithm_stats()
    
    print(f"  Path: {' -> '.join(dijkstra_path)}")
    print(f"  Distance: {dijkstra_dist:.0f} km")
    print(f"  Nodes explored: {dijkstra_stats['nodes_expanded']}")
    print(f"  Time: {dijkstra_stats['execution_time']*1000:.2f} ms")
    print(f"  Memory: {dijkstra_stats['peak_memory_bytes']/1024:.2f} KB\n")
    
    # Run A*
    print("Running A* algorithm...")
    astar = AStarPathFinder(network)
    astar_path, astar_dist = astar.find_shortest_path(source, destination)
    astar_stats = astar.get_algorithm_stats()
    
    print(f"  Path: {' -> '.join(astar_path)}")
    print(f"  Distance: {astar_dist:.0f} km")
    print(f"  Nodes explored: {astar_stats['nodes_expanded']}")
    print(f"  Time: {astar_stats['execution_time']*1000:.2f} ms")
    print(f"  Memory: {astar_stats['peak_memory_bytes']/1024:.2f} KB\n")
    
    # Comparison
    print("Comparison:")
    print(f"  A* explored {dijkstra_stats['nodes_expanded'] / astar_stats['nodes_expanded']:.1f}x fewer nodes")
    print(f"  A* was {dijkstra_stats['execution_time'] / astar_stats['execution_time']:.1f}x faster")
    print(f"  A* used {dijkstra_stats['peak_memory_bytes'] / astar_stats['peak_memory_bytes']:.1f}x less memory\n")
    
    # Visualize
    print("Opening comparison visualization...")
    plot_multiple_paths(
        network,
        [dijkstra_path, astar_path],
        labels=["Dijkstra", "A*"]
    )
    print("Done! Check your browser")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare.py <SOURCE> <DESTINATION>")
        print("Example: python compare.py LAX JFK")
        sys.exit(1)
    
    compare_algorithms(sys.argv[1], sys.argv[2])
