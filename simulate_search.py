"""
Simulate and visualize the search process for Dijkstra vs A* algorithms.
Shows step-by-step exploration patterns for LAX to JFK.
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
import plotly.graph_objects as go
from typing import List, Set, Tuple


def simulate_dijkstra_exploration(network: FlightNetwork, source: str, destination: str) -> Tuple[List[str], Set[str]]:
    """
    Simulate Dijkstra and track all explored nodes.
    
    Returns:
        Tuple of (path, explored_nodes_set)
    """
    finder = DijkstraPathFinder(network)
    path, distance = finder.find_shortest_path(source, destination)
    
    # Get the explored nodes from the algorithm's internal state
    # The nodes_expanded in stats tells us how many, but we need the actual nodes
    # We'll run it again with tracking
    
    import heapq
    
    distances = {airport: float('infinity') for airport in network.airports}
    distances[source] = 0
    predecessors = {}
    priority_queue = [(0, source)]
    explored = set()
    
    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)
        
        if current in explored:
            continue
            
        explored.add(current)
        
        if current == destination:
            break
        
        for neighbor, weight in network.get_neighbors(current):
            distance_through_current = current_distance + weight
            
            if distance_through_current < distances[neighbor]:
                distances[neighbor] = distance_through_current
                predecessors[neighbor] = current
                heapq.heappush(priority_queue, (distance_through_current, neighbor))
    
    # Reconstruct path
    path_result = []
    if destination in predecessors or destination == source:
        current = destination
        while current is not None:
            path_result.insert(0, current)
            current = predecessors.get(current)
    
    return path_result, explored


def simulate_astar_exploration(network: FlightNetwork, source: str, destination: str) -> Tuple[List[str], Set[str]]:
    """
    Simulate A* and track all explored nodes.
    
    Returns:
        Tuple of (path, explored_nodes_set)
    """
    import heapq
    from math import radians, sin, cos, sqrt, atan2
    
    def heuristic(from_code: str, to_code: str) -> float:
        """Haversine distance heuristic."""
        from_airport = network.get_airport(from_code)
        to_airport = network.get_airport(to_code)
        
        if not from_airport or not to_airport:
            return 0.0
        
        R = 6371.0
        lat1, lon1 = radians(from_airport.latitude), radians(from_airport.longitude)
        lat2, lon2 = radians(to_airport.latitude), radians(to_airport.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
    
    g_scores = {airport: float('infinity') for airport in network.airports}
    g_scores[source] = 0
    f_scores = {airport: float('infinity') for airport in network.airports}
    f_scores[source] = heuristic(source, destination)
    
    predecessors = {}
    priority_queue = [(f_scores[source], source)]
    explored = set()
    
    while priority_queue:
        _, current = heapq.heappop(priority_queue)
        
        if current in explored:
            continue
            
        explored.add(current)
        
        if current == destination:
            break
        
        for neighbor, weight in network.get_neighbors(current):
            tentative_g = g_scores[current] + weight
            
            if tentative_g < g_scores[neighbor]:
                predecessors[neighbor] = current
                g_scores[neighbor] = tentative_g
                f_scores[neighbor] = tentative_g + heuristic(neighbor, destination)
                heapq.heappush(priority_queue, (f_scores[neighbor], neighbor))
    
    # Reconstruct path
    path_result = []
    if destination in predecessors or destination == source:
        current = destination
        while current is not None:
            path_result.insert(0, current)
            current = predecessors.get(current)
    
    return path_result, explored


def create_comparison_visualization(network: FlightNetwork, source: str, destination: str):
    """
    Create side-by-side visualization of Dijkstra vs A* exploration.
    """
    print(f"\nSimulating search from {source} to {destination}...\n")
    
    # Run both algorithms
    print("Running Dijkstra's algorithm...")
    dijkstra_path, dijkstra_explored = simulate_dijkstra_exploration(network, source, destination)
    print(f"  Path: {' -> '.join(dijkstra_path)}")
    print(f"  Explored {len(dijkstra_explored)} airports")
    
    print("\nRunning A* algorithm...")
    astar_path, astar_explored = simulate_astar_exploration(network, source, destination)
    print(f"  Path: {' -> '.join(astar_path)}")
    print(f"  Explored {len(astar_explored)} airports")
    
    print(f"\nEfficiency: A* explored {len(dijkstra_explored) / len(astar_explored):.1f}x fewer nodes\n")
    
    # Create visualization
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Dijkstra's Algorithm", "A* Algorithm"),
        specs=[[{"type": "geo"}, {"type": "geo"}]],
        horizontal_spacing=0.05
    )
    
    # Helper function to add exploration to subplot
    def add_exploration_to_subplot(explored_set, path, row, col, color):
        # All airports (gray)
        all_lats = [network.get_airport(code).latitude for code in network.airports if network.get_airport(code)]
        all_lons = [network.get_airport(code).longitude for code in network.airports if network.get_airport(code)]
        
        fig.add_trace(
            go.Scattergeo(
                lon=all_lons,
                lat=all_lats,
                mode='markers',
                marker=dict(size=2, color='lightgray', opacity=0.3),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=row, col=col
        )
        
        # Explored nodes (colored)
        explored_lats = [network.get_airport(code).latitude for code in explored_set if network.get_airport(code)]
        explored_lons = [network.get_airport(code).longitude for code in explored_set if network.get_airport(code)]
        explored_names = [f"{code}: {network.get_airport(code).name}" for code in explored_set if network.get_airport(code)]
        
        fig.add_trace(
            go.Scattergeo(
                lon=explored_lons,
                lat=explored_lats,
                mode='markers',
                marker=dict(size=4, color=color, opacity=0.6),
                text=explored_names,
                hoverinfo='text',
                name=f'Explored ({len(explored_set)} nodes)',
                showlegend=(col == 1)
            ),
            row=row, col=col
        )
        
        # Final path (bold line)
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                from_airport = network.get_airport(path[i])
                to_airport = network.get_airport(path[i + 1])
                
                if from_airport and to_airport:
                    fig.add_trace(
                        go.Scattergeo(
                            lon=[from_airport.longitude, to_airport.longitude],
                            lat=[from_airport.latitude, to_airport.latitude],
                            mode='lines',
                            line=dict(width=3, color='red'),
                            showlegend=False,
                            hoverinfo='skip'
                        ),
                        row=row, col=col
                    )
        
        # Source and destination markers
        src_airport = network.get_airport(source)
        dst_airport = network.get_airport(destination)
        
        if src_airport:
            fig.add_trace(
                go.Scattergeo(
                    lon=[src_airport.longitude],
                    lat=[src_airport.latitude],
                    mode='markers+text',
                    marker=dict(size=12, color='green', symbol='star'),
                    text=[source],
                    textposition='top center',
                    name='Source',
                    showlegend=(col == 1),
                    hoverinfo='text',
                    hovertext=f"{source}: {src_airport.name}"
                ),
                row=row, col=col
            )
        
        if dst_airport:
            fig.add_trace(
                go.Scattergeo(
                    lon=[dst_airport.longitude],
                    lat=[dst_airport.latitude],
                    mode='markers+text',
                    marker=dict(size=12, color='red', symbol='star'),
                    text=[destination],
                    textposition='top center',
                    name='Destination',
                    showlegend=(col == 1),
                    hoverinfo='text',
                    hovertext=f"{destination}: {dst_airport.name}"
                ),
                row=row, col=col
            )
    
    # Add Dijkstra exploration (left subplot)
    add_exploration_to_subplot(dijkstra_explored, dijkstra_path, 1, 1, 'blue')
    
    # Add A* exploration (right subplot)
    add_exploration_to_subplot(astar_explored, astar_path, 1, 2, 'purple')
    
    # Update layout
    fig.update_geos(
        scope='usa',
        projection_type='albers usa',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        coastlinecolor='rgb(204, 204, 204)',
        showlakes=True,
        lakecolor='rgb(255, 255, 255)'
    )
    
    fig.update_layout(
        title=f"Algorithm Comparison: {source} to {destination}<br>" +
              f"<sub>Dijkstra explored {len(dijkstra_explored)} nodes | " +
              f"A* explored {len(astar_explored)} nodes | " +
              f"A* is {len(dijkstra_explored) / len(astar_explored):.1f}x more efficient</sub>",
        height=600,
        showlegend=True,
        legend=dict(x=1.02, y=0.5)
    )
    
    fig.show()
    print("Visualization opened in browser")


def main():
    """Main execution."""
    source = 'LAX'
    destination = 'JFK'
    
    if len(sys.argv) == 3:
        source = sys.argv[1].upper()
        destination = sys.argv[2].upper()
    elif len(sys.argv) > 1:
        print("Usage: python simulate_search.py [SOURCE] [DESTINATION]")
        print("Example: python simulate_search.py LAX JFK")
        print("\nRunning with default: LAX to JFK")
    
    print("="*70)
    print("ALGORITHM SEARCH VISUALIZATION")
    print("="*70)
    print(f"\nComparing Dijkstra vs A* for route: {source} -> {destination}")
    
    # Load network
    print("\nLoading flight network...")
    us_airports_df, us_routes_df = setup_openflights_data()
    network = FlightNetwork()
    network.load_from_dataframes(us_airports_df, us_routes_df)
    print(f"Loaded {len(network.airports)} airports\n")
    
    # Validate airports
    if not network.get_airport(source):
        print(f"Error: Airport {source} not found")
        return
    if not network.get_airport(destination):
        print(f"Error: Airport {destination} not found")
        return
    
    # Create visualization
    create_comparison_visualization(network, source, destination)


if __name__ == "__main__":
    main()
