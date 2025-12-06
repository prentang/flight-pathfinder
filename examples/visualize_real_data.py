"""
Example: Visualize Real Flight Data from OpenFlights

This script demonstrates the complete workflow:
1. Load real US airport and route data from OpenFlights
2. Create FlightNetwork with real data
3. Find paths using Dijkstra and A* algorithms
4. Visualize results with interactive Plotly maps
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data.openflights.downloader import setup_openflights_data
from models.graph import FlightNetwork
from algorithms.dijkstra import DijkstraPathFinder
from algorithms.a_star import AStarPathFinder
from visualization.path_plotter import (
    plot_flight_path,
    plot_multiple_paths,
    plot_network_graph
)


def load_real_network():
    """Load real US flight network from OpenFlights."""
    print("Loading OpenFlights data...")
    us_airports_df, us_routes_df = setup_openflights_data()
    
    print(f"Loaded {len(us_airports_df)} US airports")
    print(f"Loaded {len(us_routes_df)} US routes")
    
    network = FlightNetwork()
    network.load_from_dataframes(us_airports_df, us_routes_df)
    
    print(f"Created network with {len(network.airports)} airports and "
          f"{sum(len(routes) for routes in network.adjacency_list.values())} routes\n")
    
    return network


def demo_cross_country_path(network: FlightNetwork):
    """Demonstrate cross-country pathfinding (LAX to JFK)."""
    print("=" * 60)
    print("Demo 1: Cross-Country Flight (LAX -> JFK)")
    print("=" * 60)
    
    start = 'LAX'
    goal = 'JFK'
    
    # Check if airports exist
    if not network.get_airport(start) or not network.get_airport(goal):
        print(f"Error: {start} or {goal} not found in network")
        return
    
    # Find path using Dijkstra
    print(f"\nFinding shortest path from {start} to {goal}...")
    pathfinder = DijkstraPathFinder(network)
    path, total_distance = pathfinder.find_shortest_path(start, goal)
    stats = pathfinder.get_algorithm_stats()
    
    if path:
        print(f"\nPath found: {' -> '.join(path)}")
        print(f"Total distance: {total_distance:.0f} km")
        print(f"Number of stops: {len(path) - 1}")
        print(f"Algorithm stats: {stats['nodes_expanded']} nodes expanded, "
              f"{stats['execution_time']:.4f}s")
        
        # Visualize
        print("\nGenerating visualization...")
        plot_flight_path(
            network, 
            path, 
            title=f"Cross-Country Flight: {start} -> {goal}"
        )
        print("Visualization opened in browser")
    else:
        print(f"No path found from {start} to {goal}")


def demo_algorithm_comparison(network: FlightNetwork):
    """Compare Dijkstra vs A* on the same route."""
    print("\n" + "=" * 60)
    print("Demo 2: Algorithm Comparison (LAX -> MIA)")
    print("=" * 60)
    
    start = 'LAX'
    goal = 'MIA'
    
    # Check if airports exist
    if not network.get_airport(start) or not network.get_airport(goal):
        print(f"Error: {start} or {goal} not found in network")
        return
    
    print(f"\nComparing algorithms for route {start} -> {goal}...\n")
    
    # Run Dijkstra
    print("Running Dijkstra's algorithm...")
    dijkstra_finder = DijkstraPathFinder(network)
    dijkstra_path, dijkstra_distance = dijkstra_finder.find_shortest_path(start, goal)
    dijkstra_stats = dijkstra_finder.get_algorithm_stats()
    
    if dijkstra_path:
        print(f"  Path: {' -> '.join(dijkstra_path)}")
        print(f"  Distance: {dijkstra_distance:.0f} km")
        print(f"  Nodes expanded: {dijkstra_stats['nodes_expanded']}")
        print(f"  Time: {dijkstra_stats['execution_time']:.4f}s")
    
    # Run A*
    print("\nRunning A* algorithm...")
    astar_finder = AStarPathFinder(network)
    astar_path, astar_distance = astar_finder.find_shortest_path(start, goal)
    astar_stats = astar_finder.get_algorithm_stats()
    
    if astar_path:
        print(f"  Path: {' -> '.join(astar_path)}")
        print(f"  Distance: {astar_distance:.0f} km")
        print(f"  Nodes expanded: {astar_stats['nodes_expanded']}")
        print(f"  Time: {astar_stats['execution_time']:.4f}s")
    
    # Compare efficiency
    if dijkstra_path and astar_path:
        print("\nComparison:")
        print(f"  A* expanded {astar_stats['nodes_expanded']} nodes vs "
              f"Dijkstra's {dijkstra_stats['nodes_expanded']} nodes")
        print(f"  A* speedup: {dijkstra_stats['nodes_expanded'] / astar_stats['nodes_expanded']:.2f}x fewer nodes")
        
        # Visualize both paths
        print("\nGenerating comparison visualization...")
        plot_multiple_paths(
            network,
            [dijkstra_path, astar_path],
            labels=["Dijkstra", "A*"]
        )
        print("Visualization opened in browser")


def demo_regional_network(network: FlightNetwork):
    """Visualize a regional network subset."""
    print("\n" + "=" * 60)
    print("Demo 3: Regional Network Visualization (California)")
    print("=" * 60)
    
    # Find California airports
    ca_airports = [code for code, airport in network.airports.items() 
                   if 'California' in airport.name or 
                   airport.city in ['Los Angeles', 'San Francisco', 'San Diego', 
                                   'Oakland', 'San Jose', 'Sacramento']]
    
    print(f"\nFound {len(ca_airports)} California airports")
    print(f"Airports: {', '.join(sorted(ca_airports)[:10])}")
    
    # Create a path to highlight (LAX to SFO)
    start, goal = 'LAX', 'SFO'
    if start in ca_airports and goal in ca_airports:
        print(f"\nFinding path {start} -> {goal}...")
        pathfinder = DijkstraPathFinder(network)
        path, distance = pathfinder.find_shortest_path(start, goal)
        stats = pathfinder.get_algorithm_stats()
        
        if path:
            print(f"Path: {' -> '.join(path)}")
            print(f"Distance: {distance:.0f} km")
            
            # Visualize network with highlighted path
            print("\nGenerating network visualization...")
            plot_network_graph(
                network,
                highlight_path=path
            )
            print("Visualization opened in browser")
    else:
        print("Could not find LAX or SFO in California airports")


def demo_long_distance_path(network: FlightNetwork):
    """Demonstrate a long-distance path across the country."""
    print("\n" + "=" * 60)
    print("Demo 4: Long-Distance Flight (SEA -> MIA)")
    print("=" * 60)
    
    start = 'SEA'
    goal = 'MIA'
    
    # Check if airports exist
    if not network.get_airport(start) or not network.get_airport(goal):
        print(f"Error: {start} or {goal} not found in network")
        return
    
    print(f"\nFinding path from {start} to {goal}...")
    pathfinder = AStarPathFinder(network)
    path, total_distance = pathfinder.find_shortest_path(start, goal)
    stats = pathfinder.get_algorithm_stats()
    
    if path:
        print(f"\nPath found: {' -> '.join(path)}")
        print(f"Total distance: {total_distance:.0f} km")
        print(f"Number of stops: {len(path) - 1}")
        print(f"Algorithm stats: {stats['nodes_expanded']} nodes expanded, "
              f"{stats['execution_time']:.4f}s")
        
        # Visualize
        print("\nGenerating visualization...")
        plot_flight_path(
            network, 
            path, 
            title=f"Long-Distance Flight: {start} -> {goal}"
        )
        print("Visualization opened in browser")
    else:
        print(f"No path found from {start} to {goal}")


def main():
    print("\n" + "=" * 60)
    print("REAL FLIGHT DATA VISUALIZATION DEMO")
    print("=" * 60)
    print("\nThis demo will:")
    print("  1. Load real US airport/route data from OpenFlights")
    print("  2. Run pathfinding algorithms on real flight networks")
    print("  3. Generate interactive visualizations")
    print("\nNote: This may take a minute to download and process data...")
    print("=" * 60)
    
    # Load network
    network = load_real_network()
    
    # Run demonstrations
    demo_cross_country_path(network)
    demo_algorithm_comparison(network)
    demo_regional_network(network)
    demo_long_distance_path(network)
    
    print("\n" + "=" * 60)
    print("All demonstrations complete!")
    print("Check your browser for interactive visualizations")
    print("=" * 60)


if __name__ == "__main__":
    main()
