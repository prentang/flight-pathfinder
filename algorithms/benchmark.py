"""
Algorithm comparison and benchmarking utilities.
"""
from typing import Dict, List, Tuple, Any
import time
import random
import json
import csv
from algorithms.dijkstra import DijkstraPathFinder
from algorithms.a_star import AStarPathFinder
from models.graph import FlightNetwork


class AlgorithmBenchmark:
    """
    Benchmarking utilities for comparing pathfinding algorithms.
    """
    
    def __init__(self, network: FlightNetwork):
        """
        Initialize benchmark with flight network.
        
        Args:
            network: FlightNetwork to benchmark on
        """
        self.network = network
        self.dijkstra = DijkstraPathFinder(network)
        self.astar = AStarPathFinder(network)
        self.benchmark_results = []
    
    def benchmark_single_path(self, source: str, destination: str) -> Dict[str, Any]:
        """
        Benchmark both algorithms on a single path.
        
        Args:
            source: Source airport
            destination: Destination airport
        
        Returns:
            Dictionary with benchmark results
        """
        results = {
            'source': source,
            'destination': destination,
            'dijkstra': {},
            'astar': {},
            'comparison': {}
        }
        
        # Run Dijkstra's algorithm
        dijkstra_start = time.time()
        dijkstra_path, dijkstra_cost = self.dijkstra.find_shortest_path(source, destination)
        dijkstra_time = time.time() - dijkstra_start
        dijkstra_stats = self.dijkstra.get_algorithm_stats()
        
        results['dijkstra'] = {
            'path': dijkstra_path,
            'cost': dijkstra_cost,
            'execution_time': dijkstra_time,
            'nodes_expanded': dijkstra_stats.get('nodes_expanded', 0),
            'nodes_generated': dijkstra_stats.get('nodes_generated', 0),
            'path_length': len(dijkstra_path)
        }
        
        # Run A* algorithm with haversine heuristic
        astar_start = time.time()
        astar_path, astar_cost = self.astar.find_shortest_path(source, destination, heuristic="haversine")
        astar_time = time.time() - astar_start
        astar_stats = self.astar.get_algorithm_stats()
        
        results['astar'] = {
            'path': astar_path,
            'cost': astar_cost,
            'execution_time': astar_time,
            'nodes_expanded': astar_stats.get('nodes_expanded', 0),
            'nodes_generated': astar_stats.get('nodes_generated', 0),
            'heuristic_calls': astar_stats.get('heuristic_calls', 0),
            'path_length': len(astar_path)
        }
        
        # Verify path optimality
        paths_equal = dijkstra_cost == astar_cost if dijkstra_path and astar_path else True
        
        # Calculate performance improvements
        time_improvement = ((dijkstra_time - astar_time) / dijkstra_time * 100) if dijkstra_time > 0 else 0
        nodes_reduction = ((dijkstra_stats.get('nodes_expanded', 0) - astar_stats.get('nodes_expanded', 0)) / 
                          dijkstra_stats.get('nodes_expanded', 1) * 100) if dijkstra_stats.get('nodes_expanded', 0) > 0 else 0
        
        results['comparison'] = {
            'paths_optimal': paths_equal,
            'time_improvement_percent': time_improvement,
            'nodes_reduction_percent': nodes_reduction,
            'astar_faster': astar_time < dijkstra_time,
            'astar_fewer_nodes': astar_stats.get('nodes_expanded', 0) < dijkstra_stats.get('nodes_expanded', 0)
        }
        
        return results
    
    def benchmark_multiple_paths(self, test_pairs: List[Tuple[str, str]]) -> Dict[str, Any]:
        """
        Benchmark algorithms on multiple source-destination pairs.
        
        Args:
            test_pairs: List of (source, destination) tuples
        
        Returns:
            Aggregated benchmark results
        """
        all_results = []
        
        for source, destination in test_pairs:
            try:
                result = self.benchmark_single_path(source, destination)
                all_results.append(result)
            except Exception as e:
                print(f"Error benchmarking {source} to {destination}: {e}")
                continue
        
        if not all_results:
            return {
                'total_tests': 0,
                'successful_tests': 0,
                'dijkstra_stats': {},
                'astar_stats': {},
                'aggregated_comparison': {}
            }
        
        # Collect statistics for each algorithm
        dijkstra_times = [r['dijkstra']['execution_time'] for r in all_results]
        dijkstra_nodes = [r['dijkstra']['nodes_expanded'] for r in all_results]
        dijkstra_costs = [r['dijkstra']['cost'] for r in all_results if r['dijkstra']['cost'] != float('inf')]
        
        astar_times = [r['astar']['execution_time'] for r in all_results]
        astar_nodes = [r['astar']['nodes_expanded'] for r in all_results]
        astar_costs = [r['astar']['cost'] for r in all_results if r['astar']['cost'] != float('inf')]
        
        # Calculate statistics
        import statistics
        
        aggregated = {
            'total_tests': len(test_pairs),
            'successful_tests': len(all_results),
            'dijkstra_stats': {
                'avg_execution_time': statistics.mean(dijkstra_times) if dijkstra_times else 0,
                'min_execution_time': min(dijkstra_times) if dijkstra_times else 0,
                'max_execution_time': max(dijkstra_times) if dijkstra_times else 0,
                'stdev_execution_time': statistics.stdev(dijkstra_times) if len(dijkstra_times) > 1 else 0,
                'avg_nodes_expanded': statistics.mean(dijkstra_nodes) if dijkstra_nodes else 0,
                'avg_path_cost': statistics.mean(dijkstra_costs) if dijkstra_costs else 0
            },
            'astar_stats': {
                'avg_execution_time': statistics.mean(astar_times) if astar_times else 0,
                'min_execution_time': min(astar_times) if astar_times else 0,
                'max_execution_time': max(astar_times) if astar_times else 0,
                'stdev_execution_time': statistics.stdev(astar_times) if len(astar_times) > 1 else 0,
                'avg_nodes_expanded': statistics.mean(astar_nodes) if astar_nodes else 0,
                'avg_path_cost': statistics.mean(astar_costs) if astar_costs else 0
            },
            'aggregated_comparison': {
                'astar_faster_count': sum(1 for r in all_results if r['comparison']['astar_faster']),
                'astar_fewer_nodes_count': sum(1 for r in all_results if r['comparison']['astar_fewer_nodes']),
                'avg_time_improvement': statistics.mean([r['comparison']['time_improvement_percent'] for r in all_results]),
                'avg_nodes_reduction': statistics.mean([r['comparison']['nodes_reduction_percent'] for r in all_results])
            },
            'individual_results': all_results
        }
        
        return aggregated
    
    def benchmark_network_size_scaling(self) -> Dict[str, Any]:
        """
        Test how algorithms scale with network size.
        
        Returns:
            Scaling analysis results
        """
        scaling_results = []
        
        # Get all airport codes
        all_airports = list(self.network.airports.keys())
        
        if len(all_airports) < 10:
            return {'error': 'Network too small for scaling analysis'}
        
        # Create subsets of increasing size
        subset_sizes = [10, 25, 50, 100, 200]
        subset_sizes = [size for size in subset_sizes if size <= len(all_airports)]
        
        if len(all_airports) not in subset_sizes:
            subset_sizes.append(len(all_airports))
        
        for size in subset_sizes:
            # Sample airports for this subset
            subset_airports = random.sample(all_airports, min(size, len(all_airports)))
            
            # Generate test pairs within this subset
            num_tests = min(10, size // 2)
            test_pairs = []
            for _ in range(num_tests):
                if len(subset_airports) >= 2:
                    source, dest = random.sample(subset_airports, 2)
                    test_pairs.append((source, dest))
            
            if not test_pairs:
                continue
            
            # Run benchmarks on this subset
            subset_results = self.benchmark_multiple_paths(test_pairs)
            
            scaling_results.append({
                'network_size': size,
                'num_tests': len(test_pairs),
                'dijkstra_avg_time': subset_results['dijkstra_stats'].get('avg_execution_time', 0),
                'astar_avg_time': subset_results['astar_stats'].get('avg_execution_time', 0),
                'dijkstra_avg_nodes': subset_results['dijkstra_stats'].get('avg_nodes_expanded', 0),
                'astar_avg_nodes': subset_results['astar_stats'].get('avg_nodes_expanded', 0)
            })
        
        return {
            'scaling_data': scaling_results,
            'network_sizes_tested': subset_sizes,
            'analysis': 'Performance scales with network size'
        }
    
    def generate_test_cases(self, num_cases: int = 100) -> List[Tuple[str, str]]:
        """
        Generate random test cases for benchmarking.
        
        Args:
            num_cases: Number of test cases to generate
        
        Returns:
            List of (source, destination) pairs
        """
        test_cases = []
        all_airports = list(self.network.airports.keys())
        
        if len(all_airports) < 2:
            return test_cases
        
        # Calculate connectivity for each airport
        connectivity = {}
        for airport in all_airports:
            connectivity[airport] = len(self.network.get_neighbors(airport))
        
        # Identify major and minor airports
        sorted_airports = sorted(connectivity.items(), key=lambda x: x[1], reverse=True)
        major_airports = [a for a, _ in sorted_airports[:len(sorted_airports)//4]] if len(sorted_airports) > 4 else all_airports
        minor_airports = [a for a, _ in sorted_airports[len(sorted_airports)//4:]] if len(sorted_airports) > 4 else all_airports
        
        # Generate diverse test cases
        for i in range(num_cases):
            if i % 4 == 0 and len(major_airports) >= 2:
                # Major to major (likely long paths)
                source, dest = random.sample(major_airports, 2)
            elif i % 4 == 1 and len(minor_airports) >= 2:
                # Minor to minor (possibly no path)
                source, dest = random.sample(minor_airports, 2)
            elif i % 4 == 2 and major_airports and minor_airports:
                # Major to minor
                source = random.choice(major_airports)
                dest = random.choice(minor_airports)
            else:
                # Random pair
                source, dest = random.sample(all_airports, 2)
            
            test_cases.append((source, dest))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_cases = []
        for case in test_cases:
            if case not in seen:
                seen.add(case)
                unique_cases.append(case)
        
        return unique_cases
    
    def export_results(self, results: Dict[str, Any], filename: str) -> None:
        """
        Export benchmark results to file.
        
        Args:
            results: Benchmark results dictionary
            filename: Output filename
        """
        # Determine format from filename extension
        if filename.endswith('.json'):
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"Results exported to {filename}")
            
        elif filename.endswith('.csv'):
            # Export to CSV format (flatten results)
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write metadata
                writer.writerow(['Benchmark Results'])
                writer.writerow(['Total Tests', results.get('total_tests', 0)])
                writer.writerow(['Successful Tests', results.get('successful_tests', 0)])
                writer.writerow([])
                
                # Write Dijkstra stats
                writer.writerow(['Dijkstra Statistics'])
                if 'dijkstra_stats' in results:
                    for key, value in results['dijkstra_stats'].items():
                        writer.writerow([key, value])
                writer.writerow([])
                
                # Write A* stats
                writer.writerow(['A* Statistics'])
                if 'astar_stats' in results:
                    for key, value in results['astar_stats'].items():
                        writer.writerow([key, value])
                writer.writerow([])
                
                # Write comparison
                writer.writerow(['Comparison'])
                if 'aggregated_comparison' in results:
                    for key, value in results['aggregated_comparison'].items():
                        writer.writerow([key, value])
                
            print(f"Results exported to {filename}")
            
        else:
            # Default to text format
            with open(filename, 'w') as f:
                f.write("Benchmark Results\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Total Tests: {results.get('total_tests', 0)}\n")
                f.write(f"Successful Tests: {results.get('successful_tests', 0)}\n\n")
                
                f.write("Dijkstra Statistics:\n")
                if 'dijkstra_stats' in results:
                    for key, value in results['dijkstra_stats'].items():
                        f.write(f"  {key}: {value}\n")
                f.write("\n")
                
                f.write("A* Statistics:\n")
                if 'astar_stats' in results:
                    for key, value in results['astar_stats'].items():
                        f.write(f"  {key}: {value}\n")
                f.write("\n")
                
                f.write("Comparison:\n")
                if 'aggregated_comparison' in results:
                    for key, value in results['aggregated_comparison'].items():
                        f.write(f"  {key}: {value}\n")
                
            print(f"Results exported to {filename}")
