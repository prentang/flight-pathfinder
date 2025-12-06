"""
Benchmark runner for flight pathfinding algorithms.

This script:
1. Loads real flight network data
2. Runs pathfinding algorithms on various test cases
3. Collects performance metrics (time, space, nodes expanded)
4. Exports results to txt, json, and csv formats
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import csv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data.openflights.downloader import setup_openflights_data
from models.graph import FlightNetwork
from algorithms.dijkstra import DijkstraPathFinder
from algorithms.a_star import AStarPathFinder


# Test cases: (start, goal, description)
TEST_CASES = [
    ('LAX', 'JFK', 'Cross-country (West to East)'),
    ('SEA', 'MIA', 'Northwest to Southeast'),
    ('LAX', 'MIA', 'West to Southeast'),
    ('SFO', 'BOS', 'West Coast to East Coast'),
    ('ORD', 'ATL', 'Midwest to South'),
    ('DFW', 'DEN', 'Texas to Colorado'),
    ('LAX', 'SFO', 'Short distance (CA)'),
    ('JFK', 'BOS', 'Short distance (Northeast)'),
]


def format_memory(bytes_val):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} TB"


def run_benchmark(network: FlightNetwork):
    """Run comprehensive benchmarks on all test cases."""
    print("\n" + "=" * 80)
    print("FLIGHT PATHFINDER ALGORITHM BENCHMARK")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Network size: {len(network.airports)} airports, "
          f"{sum(len(routes) for routes in network.adjacency_list.values())} routes")
    print("=" * 80)
    
    results = []
    
    for i, (start, goal, description) in enumerate(TEST_CASES, 1):
        print(f"\n[Test {i}/{len(TEST_CASES)}] {description}: {start} → {goal}")
        print("-" * 80)
        
        # Check if airports exist
        if not network.get_airport(start) or not network.get_airport(goal):
            print(f"  ⚠ Skipping: Airport not found in network")
            continue
        
        # Run Dijkstra
        print("  Running Dijkstra's algorithm...")
        dijkstra_finder = DijkstraPathFinder(network)
        try:
            dijkstra_path, dijkstra_distance = dijkstra_finder.find_shortest_path(start, goal)
            dijkstra_stats = dijkstra_finder.get_algorithm_stats()
            
            if dijkstra_path:
                print(f"    ✓ Path found: {len(dijkstra_path)} stops, {dijkstra_distance:.0f} km")
                print(f"    • Nodes expanded: {dijkstra_stats['nodes_expanded']}")
                print(f"    • Execution time: {dijkstra_stats['execution_time']:.6f}s")
                print(f"    • Peak memory: {format_memory(dijkstra_stats['peak_memory_bytes'])}")
            else:
                print(f"    ✗ No path found")
                dijkstra_stats = None
        except Exception as e:
            print(f"    ✗ Error: {e}")
            dijkstra_stats = None
        
        # Run A*
        print("  Running A* algorithm...")
        astar_finder = AStarPathFinder(network)
        try:
            astar_path, astar_distance = astar_finder.find_shortest_path(start, goal)
            astar_stats = astar_finder.get_algorithm_stats()
            
            if astar_path:
                print(f"    ✓ Path found: {len(astar_path)} stops, {astar_distance:.0f} km")
                print(f"    • Nodes expanded: {astar_stats['nodes_expanded']}")
                print(f"    • Execution time: {astar_stats['execution_time']:.6f}s")
                print(f"    • Peak memory: {format_memory(astar_stats['peak_memory_bytes'])}")
            else:
                print(f"    ✗ No path found")
                astar_stats = None
        except Exception as e:
            print(f"    ✗ Error: {e}")
            astar_stats = None
        
        # Compare results
        if dijkstra_stats and astar_stats:
            speedup = dijkstra_stats['nodes_expanded'] / astar_stats['nodes_expanded']
            time_ratio = dijkstra_stats['execution_time'] / astar_stats['execution_time']
            memory_ratio = dijkstra_stats['peak_memory_bytes'] / astar_stats['peak_memory_bytes']
            
            print(f"\n  Comparison:")
            print(f"    • A* expanded {speedup:.2f}x fewer nodes")
            print(f"    • A* was {time_ratio:.2f}x faster")
            print(f"    • A* used {memory_ratio:.2f}x memory")
            
            # Store results
            results.append({
                'test_case': description,
                'start': start,
                'goal': goal,
                'dijkstra_path_length': len(dijkstra_path),
                'dijkstra_distance_km': dijkstra_distance,
                'dijkstra_nodes_expanded': dijkstra_stats['nodes_expanded'],
                'dijkstra_time_seconds': dijkstra_stats['execution_time'],
                'dijkstra_memory_bytes': dijkstra_stats['peak_memory_bytes'],
                'astar_path_length': len(astar_path),
                'astar_distance_km': astar_distance,
                'astar_nodes_expanded': astar_stats['nodes_expanded'],
                'astar_time_seconds': astar_stats['execution_time'],
                'astar_memory_bytes': astar_stats['peak_memory_bytes'],
                'speedup_factor': speedup,
                'time_ratio': time_ratio,
                'memory_ratio': memory_ratio
            })
    
    return results


def export_results_txt(results, output_path):
    """Export results to plain text format."""
    with open(output_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("FLIGHT PATHFINDER ALGORITHM BENCHMARK RESULTS\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total test cases: {len(results)}\n")
        f.write("=" * 80 + "\n\n")
        
        for i, result in enumerate(results, 1):
            f.write(f"Test Case {i}: {result['test_case']}\n")
            f.write(f"Route: {result['start']} → {result['goal']}\n")
            f.write("-" * 80 + "\n")
            
            f.write(f"Dijkstra's Algorithm:\n")
            f.write(f"  Path length: {result['dijkstra_path_length']} stops\n")
            f.write(f"  Distance: {result['dijkstra_distance_km']:.2f} km\n")
            f.write(f"  Nodes expanded: {result['dijkstra_nodes_expanded']}\n")
            f.write(f"  Execution time: {result['dijkstra_time_seconds']:.6f}s\n")
            f.write(f"  Peak memory: {format_memory(result['dijkstra_memory_bytes'])}\n")
            
            f.write(f"\nA* Algorithm:\n")
            f.write(f"  Path length: {result['astar_path_length']} stops\n")
            f.write(f"  Distance: {result['astar_distance_km']:.2f} km\n")
            f.write(f"  Nodes expanded: {result['astar_nodes_expanded']}\n")
            f.write(f"  Execution time: {result['astar_time_seconds']:.6f}s\n")
            f.write(f"  Peak memory: {format_memory(result['astar_memory_bytes'])}\n")
            
            f.write(f"\nComparison:\n")
            f.write(f"  Speedup factor: {result['speedup_factor']:.2f}x\n")
            f.write(f"  Time ratio: {result['time_ratio']:.2f}x\n")
            f.write(f"  Memory ratio: {result['memory_ratio']:.2f}x\n")
            f.write("\n" + "=" * 80 + "\n\n")
    
    print(f"\n✓ Exported text results to: {output_path}")


def export_results_json(results, output_path):
    """Export results to JSON format."""
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'test_cases_count': len(results),
        'results': results
    }
    
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"✓ Exported JSON results to: {output_path}")


def export_results_csv(results, output_path):
    """Export results to CSV format."""
    if not results:
        print("⚠ No results to export to CSV")
        return
    
    fieldnames = results[0].keys()
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✓ Exported CSV results to: {output_path}")


def main():
    """Main benchmark execution."""
    print("\n" + "=" * 80)
    print("INITIALIZING BENCHMARK SUITE")
    print("=" * 80)
    
    # Load network
    print("\n[1/3] Loading flight network data...")
    us_airports_df, us_routes_df = setup_openflights_data()
    network = FlightNetwork()
    network.load_from_dataframes(us_airports_df, us_routes_df)
    print(f"✓ Network loaded: {len(network.airports)} airports, "
          f"{sum(len(routes) for routes in network.adjacency_list.values())} routes")
    
    # Run benchmarks
    print("\n[2/3] Running benchmarks...")
    results = run_benchmark(network)
    
    # Export results
    print("\n[3/3] Exporting results...")
    benchmarks_dir = Path(__file__).parent
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    export_results_txt(results, benchmarks_dir / f'results_{timestamp}.txt')
    export_results_json(results, benchmarks_dir / f'results_{timestamp}.json')
    export_results_csv(results, benchmarks_dir / f'results_{timestamp}.csv')
    
    print("\n" + "=" * 80)
    print("BENCHMARK COMPLETE")
    print("=" * 80)
    print(f"Results saved to: {benchmarks_dir}")
    print(f"Total test cases run: {len(results)}")
    
    # Summary statistics
    if results:
        avg_speedup = sum(r['speedup_factor'] for r in results) / len(results)
        avg_time_ratio = sum(r['time_ratio'] for r in results) / len(results)
        avg_memory_ratio = sum(r['memory_ratio'] for r in results) / len(results)
        
        print(f"\nAverage Performance:")
        print(f"  • A* expanded {avg_speedup:.2f}x fewer nodes on average")
        print(f"  • A* was {avg_time_ratio:.2f}x faster on average")
        print(f"  • A* used {avg_memory_ratio:.2f}x memory on average")
    
    print("=" * 80)


if __name__ == "__main__":
    main()
