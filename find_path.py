#!/usr/bin/env python3
"""
Flight Path Finder - Simple CLI for finding optimal flight paths

Usage:
    python find_path.py LAX JFK                    # Find fastest path
    python find_path.py LAX JFK --visualize        # Find and visualize
    python find_path.py LAX JFK --algorithm astar  # Use A* algorithm
    python find_path.py --list-airports            # List available airports
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from data.openflights.downloader import setup_openflights_data
from models.graph import FlightNetwork
from algorithms.dijkstra import DijkstraPathFinder
from algorithms.a_star import AStarPathFinder
from visualization.path_plotter import plot_flight_path


class SimpleFlightPathFinder:
    """Simple interface for finding flight paths."""
    
    def __init__(self):
        """Initialize and load flight network."""
        self.network = None
        self._load_network()
    
    def _load_network(self):
        """Load the flight network from OpenFlights data."""
        print("Loading flight network...")
        us_airports_df, us_routes_df = setup_openflights_data()
        
        self.network = FlightNetwork()
        self.network.load_from_dataframes(us_airports_df, us_routes_df)
        
        print(f"Loaded {len(self.network.airports)} airports, "
              f"{sum(len(routes) for routes in self.network.adjacency_list.values())} routes\n")
    
    def find_fastest_path(self, source, destination, algorithm='astar', visualize=False):
        """
        Find the fastest path between two airports.
        
        Args:
            source: Source airport code (e.g., 'LAX')
            destination: Destination airport code (e.g., 'JFK')
            algorithm: 'dijkstra' or 'astar' (default: 'astar' - faster)
            visualize: If True, open interactive map
        
        Returns:
            Tuple of (path, distance, stats)
        """
        # Validate airports exist
        source = source.upper()
        destination = destination.upper()
        
        if not self.network.get_airport(source):
            print(f"Error: Airport '{source}' not found in network")
            return None
        
        if not self.network.get_airport(destination):
            print(f"Error: Airport '{destination}' not found in network")
            return None
        
        # Select algorithm
        if algorithm.lower() == 'astar':
            finder = AStarPathFinder(self.network)
            algo_name = "A*"
        else:
            finder = DijkstraPathFinder(self.network)
            algo_name = "Dijkstra"
        
        # Find path
        print(f"Finding fastest path using {algo_name} algorithm...")
        path, distance = finder.find_shortest_path(source, destination)
        stats = finder.get_algorithm_stats()
        
        if not path:
            print(f"No path found from {source} to {destination}")
            return None
        
        # Display results
        src_airport = self.network.get_airport(source)
        dest_airport = self.network.get_airport(destination)
        
        num_layovers = len(path) - 2  # path includes source and destination
        
        print(f"\n{'='*70}")
        print(f"FASTEST PATH FOUND")
        print(f"{'='*70}")
        print(f"From: {source} - {src_airport.name} ({src_airport.city})")
        print(f"To:   {destination} - {dest_airport.name} ({dest_airport.city})")
        print(f"\nRoute: {' -> '.join(path)}")
        print(f"Total Distance: {distance:.0f} km")
        
        if num_layovers == 0:
            print(f"Flight Type: DIRECT FLIGHT (no layovers)")
        elif num_layovers == 1:
            print(f"Flight Type: 1 LAYOVER at {path[1]}")
        else:
            layover_airports = ', '.join(path[1:-1])
            print(f"Flight Type: {num_layovers} LAYOVERS at {layover_airports}")
        
        print(f"\nAlgorithm: {algo_name}")
        print(f"Nodes Explored: {stats['nodes_expanded']}")
        print(f"Execution Time: {stats['execution_time']*1000:.2f} ms")
        print(f"Memory Used: {stats['peak_memory_bytes']/1024:.2f} KB")
        print(f"{'='*70}\n")
        
        # Show route details with layover information
        if len(path) > 1:
            print("Flight Segments:")
            for i in range(len(path) - 1):
                leg_distance = self.network.get_edge_weight(path[i], path[i+1])
                from_apt = self.network.get_airport(path[i])
                to_apt = self.network.get_airport(path[i+1])
                
                # Determine if this is a layover stop
                if i == 0:
                    segment_type = "Departure"
                elif i == len(path) - 2:
                    segment_type = "Final Leg"
                else:
                    segment_type = "Connecting"
                
                print(f"  Segment {i+1} ({segment_type}): {path[i]} ({from_apt.city}) -> {path[i+1]} "
                      f"({to_apt.city}) - {leg_distance:.0f} km")
                
                # Show layover info for intermediate stops
                if i < len(path) - 2:  # Not the last segment
                    layover_airport = self.network.get_airport(path[i+1])
                    print(f"    ** LAYOVER at {path[i+1]} - {layover_airport.name} **")
        
        # Visualize if requested
        if visualize:
            print("\nGenerating interactive visualization...")
            plot_flight_path(self.network, path, 
                           title=f"Fastest Route: {source} -> {destination}")
            print("Visualization opened in browser")
        
        return path, distance, stats
    
    def list_airports(self, limit=20):
        """List available airports."""
        print(f"\nAvailable Airports (showing {limit} of {len(self.network.airports)}):")
        print(f"{'Code':<6} {'Airport Name':<45} {'City':<20}")
        print("-" * 71)
        
        for i, (code, airport) in enumerate(sorted(self.network.airports.items())):
            if i >= limit:
                break
            print(f"{code:<6} {airport.name:<45} {airport.city:<20}")
        
        print(f"\nTotal: {len(self.network.airports)} airports available")
        print("Use any 3-letter airport code (e.g., LAX, JFK, ORD, DFW, ATL)")
    
    def get_airport_info(self, code):
        """Get detailed information about an airport."""
        code = code.upper()
        airport = self.network.get_airport(code)
        
        if not airport:
            print(f"Airport '{code}' not found")
            return
        
        routes = self.network.get_neighbors(code)
        
        print(f"\n{'='*70}")
        print(f"AIRPORT INFORMATION: {code}")
        print(f"{'='*70}")
        print(f"Name: {airport.name}")
        print(f"City: {airport.city}")
        print(f"Country: {airport.country}")
        print(f"Coordinates: ({airport.latitude:.4f}, {airport.longitude:.4f})")
        print(f"Direct Routes: {len(routes)}")
        
        if routes:
            print(f"\nTop 10 Nearest Destinations:")
            sorted_routes = sorted(routes, key=lambda x: x[1])[:10]
            for dest, dist in sorted_routes:
                dest_apt = self.network.get_airport(dest)
                print(f"  {dest} ({dest_apt.city}): {dist:.0f} km")
        print(f"{'='*70}\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Find the fastest flight path between two airports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s LAX JFK                    Find fastest path from LAX to JFK
  %(prog)s LAX JFK --visualize        Find path and show on map
  %(prog)s SEA MIA --algorithm astar  Use A* algorithm (faster)
  %(prog)s --list-airports            Show available airports
  %(prog)s --airport-info LAX         Get info about LAX
        """
    )
    
    parser.add_argument('source', nargs='?', help='Source airport code (e.g., LAX)')
    parser.add_argument('destination', nargs='?', help='Destination airport code (e.g., JFK)')
    parser.add_argument('-a', '--algorithm', choices=['astar', 'dijkstra'], 
                       default='astar',
                       help='Algorithm to use (default: astar - faster)')
    parser.add_argument('-v', '--visualize', action='store_true',
                       help='Show interactive map visualization')
    parser.add_argument('-l', '--list-airports', action='store_true',
                       help='List available airports')
    parser.add_argument('-i', '--airport-info', metavar='CODE',
                       help='Show information about an airport')
    
    args = parser.parse_args()
    
    # Initialize finder
    finder = SimpleFlightPathFinder()
    
    # Handle different modes
    if args.list_airports:
        finder.list_airports(limit=50)
        return
    
    if args.airport_info:
        finder.get_airport_info(args.airport_info)
        return
    
    if not args.source or not args.destination:
        parser.print_help()
        print("\nQuick start: python find_path.py LAX JFK --visualize")
        return
    
    # Find path
    finder.find_fastest_path(
        args.source, 
        args.destination, 
        algorithm=args.algorithm,
        visualize=args.visualize
    )


if __name__ == "__main__":
    main()
