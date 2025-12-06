#!/usr/bin/env python3
"""
Quick Visualization - Single Flight Path

Usage:
    python visualize.py LAX JFK
    python visualize.py SEA MIA
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data.openflights.downloader import setup_openflights_data
from models.graph import FlightNetwork
from algorithms.a_star import AStarPathFinder
from visualization.path_plotter import plot_flight_path


def visualize_path(source, destination):
    """Visualize the fastest path between two airports."""
    source = source.upper()
    destination = destination.upper()
    
    # Load network
    print("Loading flight network...")
    us_airports_df, us_routes_df = setup_openflights_data()
    network = FlightNetwork()
    network.load_from_dataframes(us_airports_df, us_routes_df)
    print(f"Loaded {len(network.airports)} airports\n")
    
    # Validate airports
    if not network.get_airport(source):
        print(f"Error: Airport '{source}' not found")
        return
    if not network.get_airport(destination):
        print(f"Error: Airport '{destination}' not found")
        return
    
    # Find path
    print(f"Finding path from {source} to {destination}...")
    finder = AStarPathFinder(network)
    path, distance = finder.find_shortest_path(source, destination)
    stats = finder.get_algorithm_stats()
    
    if not path:
        print(f"No path found from {source} to {destination}")
        return
    
    # Show results
    print(f"Path: {' → '.join(path)}")
    print(f"Distance: {distance:.0f} km")
    print(f"Stops: {len(path) - 1}")
    print(f"Time: {stats['execution_time']*1000:.2f} ms\n")
    
    # Visualize
    print("Opening interactive map...")
    plot_flight_path(network, path, title=f"{source} → {destination}")
    print("✓ Done! Check your browser")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python visualize.py <SOURCE> <DESTINATION>")
        print("Example: python visualize.py LAX JFK")
        sys.exit(1)
    
    visualize_path(sys.argv[1], sys.argv[2])
