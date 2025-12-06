"""
Find alternative flight routes with different numbers of layovers.
Shows multiple path options between two airports.
"""
import sys
from pathlib import Path
import heapq
from typing import List, Tuple, Set

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data.openflights.downloader import setup_openflights_data
from models.graph import FlightNetwork
from algorithms.a_star import AStarPathFinder
from algorithms.dijkstra import DijkstraPathFinder
from visualization.path_plotter import plot_multiple_paths


def find_k_shortest_paths(network: FlightNetwork, source: str, destination: str, k: int = 5, 
                           use_dijkstra: bool = False) -> Tuple[List[Tuple[List[str], float]], dict, dict]:
    """
    Find k shortest paths using Yen's algorithm (simplified version).
    
    Args:
        network: Flight network
        source: Source airport code
        destination: Destination airport code  
        k: Number of paths to find
        use_dijkstra: If True, also run Dijkstra for comparison
        
    Returns:
        Tuple of (paths_list, astar_stats, dijkstra_stats)
        paths_list: List of (path, distance) tuples
        astar_stats: A* performance statistics
        dijkstra_stats: Dijkstra performance statistics (or empty dict)
    """
    paths = []
    
    # Find the shortest path first with A*
    astar_finder = AStarPathFinder(network)
    shortest_path, shortest_distance = astar_finder.find_shortest_path(source, destination)
    astar_stats = astar_finder.last_run_stats.copy()
    
    # Optionally run Dijkstra for comparison
    dijkstra_stats = {}
    if use_dijkstra:
        dijkstra_finder = DijkstraPathFinder(network)
        dijkstra_finder.find_shortest_path(source, destination)
        dijkstra_stats = dijkstra_finder.last_run_stats.copy()
    
    if not shortest_path:
        return [], astar_stats, dijkstra_stats
    
    paths.append((shortest_path, shortest_distance))
    
    # Simple approach: find alternatives by temporarily removing edges
    potential_paths = []
    
    # Try removing each edge in the shortest path and finding alternative
    for i in range(len(shortest_path) - 1):
        from_node = shortest_path[i]
        to_node = shortest_path[i + 1]
        
        # Temporarily remove this edge
        original_neighbors = list(network.get_neighbors(from_node))
        temp_neighbors = [(n, w) for n, w in original_neighbors if n != to_node]
        
        # Monkey patch to remove edge
        network.adjacency_list[from_node] = [(n, w) for n, w in network.adjacency_list[from_node] if n != to_node]
        
        # Find path without this edge
        alt_finder = AStarPathFinder(network)
        alt_path, alt_distance = alt_finder.find_shortest_path(source, destination)
        
        if alt_path and alt_path not in [p[0] for p in paths]:
            potential_paths.append((alt_path, alt_distance))
        
        # Restore edge
        network.adjacency_list[from_node] = original_neighbors
    
    # Sort potential paths by distance and add unique ones
    potential_paths.sort(key=lambda x: x[1])
    for path, dist in potential_paths:
        if len(paths) >= k:
            break
        if path not in [p[0] for p in paths]:
            paths.append((path, dist))
    
    return paths[:k], astar_stats, dijkstra_stats


def display_alternative_routes(network: FlightNetwork, source: str, destination: str, 
                              visualize: bool = False, compare_algorithms: bool = False):
    """
    Display alternative routes with different numbers of layovers.
    
    Args:
        network: Flight network
        source: Source airport code
        destination: Destination airport code
        visualize: If True, create visualization of all routes
        compare_algorithms: If True, show both A* and Dijkstra performance
    """
    
    print(f"\n{'='*70}")
    print(f"ALTERNATIVE ROUTES: {source} to {destination}")
    print(f"{'='*70}\n")
    
    # Find multiple paths
    paths, astar_stats, dijkstra_stats = find_k_shortest_paths(
        network, source, destination, k=5, use_dijkstra=compare_algorithms
    )
    
    if not paths:
        print(f"No routes found from {source} to {destination}")
        return
    
    # Group by number of layovers
    by_layovers = {}
    for path, distance in paths:
        num_layovers = len(path) - 2
        if num_layovers not in by_layovers:
            by_layovers[num_layovers] = []
        by_layovers[num_layovers].append((path, distance))
    
    # Display each route
    for idx, (path, distance) in enumerate(paths, 1):
        num_layovers = len(path) - 2
        
        print(f"Option {idx}: {' -> '.join(path)}")
        print(f"  Distance: {distance:.0f} km")
        
        if num_layovers == 0:
            print(f"  Type: DIRECT FLIGHT")
        elif num_layovers == 1:
            layover_airport = network.get_airport(path[1])
            print(f"  Type: 1 LAYOVER at {path[1]} ({layover_airport.name})")
        else:
            layover_codes = ', '.join(path[1:-1])
            print(f"  Type: {num_layovers} LAYOVERS at {layover_codes}")
        
        # Show segments
        print(f"  Segments:")
        for i in range(len(path) - 1):
            from_apt = network.get_airport(path[i])
            to_apt = network.get_airport(path[i+1])
            leg_distance = network.get_edge_weight(path[i], path[i+1])
            print(f"    {path[i]} ({from_apt.city}) -> {path[i+1]} ({to_apt.city}): {leg_distance:.0f} km")
        
        print()
    
    # Summary
    print(f"{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Total routes found: {len(paths)}")
    print(f"Shortest route: {paths[0][1]:.0f} km with {len(paths[0][0]) - 2} layovers")
    if len(paths) > 1:
        print(f"Longest route: {paths[-1][1]:.0f} km with {len(paths[-1][0]) - 2} layovers")
    
    # Show direct flights if available
    direct_flights = [p for p in paths if len(p[0]) == 2]
    if direct_flights:
        print(f"\nDirect flights available: Yes ({direct_flights[0][1]:.0f} km)")
    else:
        print(f"\nDirect flights available: No (minimum {len(paths[0][0]) - 2} layovers required)")
    
    # Display algorithm performance
    print(f"\n{'='*70}")
    print(f"ALGORITHM PERFORMANCE")
    print(f"{'='*70}")
    
    # A* stats
    print(f"\nAlgorithm: A*")
    print(f"Nodes Explored: {astar_stats.get('nodes_expanded', 0)}")
    print(f"Execution Time: {astar_stats.get('execution_time', 0)*1000:.2f} ms")
    print(f"Memory Used: {astar_stats.get('peak_memory_bytes', 0)/1024:.2f} KB")
    
    # Dijkstra stats if requested
    if compare_algorithms and dijkstra_stats:
        print(f"\nAlgorithm: Dijkstra")
        print(f"Nodes Explored: {dijkstra_stats.get('nodes_expanded', 0)}")
        print(f"Execution Time: {dijkstra_stats.get('execution_time', 0)*1000:.2f} ms")
        print(f"Memory Used: {dijkstra_stats.get('peak_memory_bytes', 0)/1024:.2f} KB")
        
        # Show comparison
        if astar_stats.get('nodes_expanded', 0) > 0 and dijkstra_stats.get('nodes_expanded', 0) > 0:
            speedup = dijkstra_stats.get('nodes_expanded', 1) / astar_stats.get('nodes_expanded', 1)
            time_ratio = dijkstra_stats.get('execution_time', 1) / astar_stats.get('execution_time', 1)
            print(f"\nEfficiency Comparison:")
            print(f"A* explored {speedup:.1f}x fewer nodes than Dijkstra")
            print(f"A* was {time_ratio:.1f}x faster than Dijkstra")
    
    # Visualization if requested
    if visualize:
        print(f"\n{'='*70}")
        print(f"GENERATING VISUALIZATION...")
        print(f"{'='*70}\n")
        
        # Prepare paths for visualization
        path_list = []
        label_list = []
        for idx, (path, distance) in enumerate(paths, 1):
            num_layovers = len(path) - 2
            if num_layovers == 0:
                label = f"Route {idx}: Direct Flight ({distance:.0f} km)"
            elif num_layovers == 1:
                label = f"Route {idx}: 1 Layover ({distance:.0f} km)"
            else:
                label = f"Route {idx}: {num_layovers} Layovers ({distance:.0f} km)"
            
            path_list.append(path)
            label_list.append(label)
        
        # Create visualization
        plot_multiple_paths(network, path_list, label_list)
        print("Visualization complete! Opening in browser...")



def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Find alternative flight routes with different layover options',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python find_alternatives.py ABE JFK
  python find_alternatives.py ABE JFK --visualize
  python find_alternatives.py LAX JFK --compare
  python find_alternatives.py SFO MIA --visualize --compare
        """
    )
    parser.add_argument('source', help='Source airport code (e.g., ABE)')
    parser.add_argument('destination', help='Destination airport code (e.g., JFK)')
    parser.add_argument('--visualize', '-v', action='store_true',
                       help='Generate visualization of all alternative routes')
    parser.add_argument('--compare', '-c', action='store_true',
                       help='Compare A* and Dijkstra algorithm performance')
    
    args = parser.parse_args()
    
    source = args.source.upper()
    destination = args.destination.upper()
    
    print("="*70)
    print("ALTERNATIVE ROUTE FINDER")
    print("="*70)
    
    # Load network
    print("\nLoading flight network...")
    us_airports_df, us_routes_df = setup_openflights_data()
    network = FlightNetwork()
    network.load_from_dataframes(us_airports_df, us_routes_df)
    print(f"Loaded {len(network.airports)} airports\n")
    
    # Validate airports
    if not network.get_airport(source):
        print(f"Error: Airport {source} not found")
        sys.exit(1)
    if not network.get_airport(destination):
        print(f"Error: Airport {destination} not found")
        sys.exit(1)
    
    # Find and display alternatives
    display_alternative_routes(network, source, destination, 
                              visualize=args.visualize,
                              compare_algorithms=args.compare)


if __name__ == "__main__":
    main()
