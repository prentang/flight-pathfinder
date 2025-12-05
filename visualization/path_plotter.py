"""
Path visualization utilities using Plotly for flight route visualization.
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict, Tuple, Optional
from models.graph import FlightNetwork


def plot_flight_path(network: FlightNetwork, path: List[str], title: str = "Flight Path") -> None:
    """
    Visualize a flight path on a map.
    
    Args:
        network: FlightNetwork containing airport data
        path: List of airport codes in path order
        title: Plot title
    """
    if not path:
        print("No path to plot.")
        return
    
    # Extract coordinates for each airport in path
    lats = []
    lons = []
    names = []
    
    for airport_code in path:
        airport = network.get_airport(airport_code)
        if airport:
            lats.append(airport.latitude)
            lons.append(airport.longitude)
            names.append(f"{airport.code} - {airport.city}")
        else:
            print(f"Warning: Airport {airport_code} not found in network")
    
    if len(lats) < 2:
        print("Not enough valid airports to plot a path.")
        return
    
    # Create figure with path line and airport markers
    fig = go.Figure()
    
    # Add path line
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode='lines',
        line=dict(width=2, color='red'),
        name='Flight Path'
    ))
    
    # Add airport markers
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode='markers+text',
        marker=dict(size=10, color='blue', symbol='circle'),
        text=[airport_code for airport_code in path],
        textposition='top center',
        hovertext=names,
        hoverinfo='text',
        name='Airports'
    ))
    
    # Highlight start and end airports
    fig.add_trace(go.Scattergeo(
        lon=[lons[0], lons[-1]],
        lat=[lats[0], lats[-1]],
        mode='markers',
        marker=dict(size=15, color=['green', 'red'], symbol='star'),
        text=[path[0], path[-1]],
        hovertext=[f"Start: {names[0]}", f"End: {names[-1]}"],
        hoverinfo='text',
        name='Start/End'
    ))
    
    # Update layout with US-focused projection
    fig.update_geos(
        projection_type="albers usa",
        showland=True,
        landcolor='rgb(243, 243, 243)',
        coastlinecolor='rgb(204, 204, 204)',
        showlakes=True,
        lakecolor='rgb(255, 255, 255)',
        showcountries=True,
        countrycolor='rgb(204, 204, 204)'
    )
    
    fig.update_layout(
        title=title,
        showlegend=True,
        geo=dict(
            scope='usa',
            projection_scale=1.0
        ),
        height=600
    )
    
    fig.show()


def plot_multiple_paths(network: FlightNetwork, paths: List[List[str]], 
                       labels: List[str] = None) -> None:
    """
    Visualize multiple flight paths on the same map for comparison.
    
    Args:
        network: FlightNetwork containing airport data
        paths: List of paths (each path is list of airport codes)
        labels: Optional labels for each path
    """
    if not paths:
        print("No paths to plot.")
        return
    
    # Generate labels if not provided
    if labels is None:
        labels = [f"Path {i+1}" for i in range(len(paths))]
    
    # Color palette for different paths
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    
    fig = go.Figure()
    
    # Collect all airports for marker overlay
    all_airports = set()
    for path in paths:
        all_airports.update(path)
    
    # Plot each path
    for idx, (path, label) in enumerate(zip(paths, labels)):
        if not path:
            continue
        
        # Extract coordinates
        lats = []
        lons = []
        names = []
        
        for airport_code in path:
            airport = network.get_airport(airport_code)
            if airport:
                lats.append(airport.latitude)
                lons.append(airport.longitude)
                names.append(f"{airport.code} - {airport.city}")
        
        if len(lats) < 2:
            continue
        
        color = colors[idx % len(colors)]
        
        # Add path line
        fig.add_trace(go.Scattergeo(
            lon=lons,
            lat=lats,
            mode='lines',
            line=dict(width=2, color=color),
            name=label,
            hovertext=[f"{label}: {name}" for name in names],
            hoverinfo='text'
        ))
        
        # Add start/end markers for this path
        fig.add_trace(go.Scattergeo(
            lon=[lons[0], lons[-1]],
            lat=[lats[0], lats[-1]],
            mode='markers',
            marker=dict(size=12, color=color, symbol='star', line=dict(width=1, color='white')),
            showlegend=False,
            hovertext=[f"{label} Start: {names[0]}", f"{label} End: {names[-1]}"],
            hoverinfo='text'
        ))
    
    # Add markers for all unique airports
    airport_lats = []
    airport_lons = []
    airport_labels = []
    
    for airport_code in all_airports:
        airport = network.get_airport(airport_code)
        if airport:
            airport_lats.append(airport.latitude)
            airport_lons.append(airport.longitude)
            airport_labels.append(airport.code)
    
    fig.add_trace(go.Scattergeo(
        lon=airport_lons,
        lat=airport_lats,
        mode='markers+text',
        marker=dict(size=8, color='darkblue', symbol='circle'),
        text=airport_labels,
        textposition='top center',
        textfont=dict(size=8),
        name='Airports',
        hovertext=[f"{code}" for code in airport_labels],
        hoverinfo='text'
    ))
    
    # Update layout
    fig.update_geos(
        projection_type="albers usa",
        showland=True,
        landcolor='rgb(243, 243, 243)',
        coastlinecolor='rgb(204, 204, 204)',
        showlakes=True,
        lakecolor='rgb(255, 255, 255)'
    )
    
    fig.update_layout(
        title="Flight Path Comparison",
        showlegend=True,
        geo=dict(scope='usa'),
        height=600
    )
    
    fig.show()


def plot_network_graph(network: FlightNetwork, highlight_path: List[str] = None) -> None:
    """
    Visualize the entire flight network as a graph.
    
    Args:
        network: FlightNetwork to visualize
        highlight_path: Optional path to highlight
    """
    if not network.airports:
        print("Network is empty.")
        return
    
    fig = go.Figure()
    
    # Calculate node sizes based on connectivity (number of connections)
    connectivity = {}
    for airport_code in network.airports:
        connectivity[airport_code] = len(network.get_neighbors(airport_code))
    
    max_connections = max(connectivity.values()) if connectivity else 1
    
    # Draw all edges (routes)
    edge_lats = []
    edge_lons = []
    
    for airport_code in network.airports:
        airport = network.get_airport(airport_code)
        neighbors = network.get_neighbors(airport_code)
        
        for neighbor_code, _ in neighbors:
            neighbor_airport = network.get_airport(neighbor_code)
            if neighbor_airport:
                # Add line segment
                edge_lats.extend([airport.latitude, neighbor_airport.latitude, None])
                edge_lons.extend([airport.longitude, neighbor_airport.longitude, None])
    
    # Add edges as trace
    fig.add_trace(go.Scattergeo(
        lon=edge_lons,
        lat=edge_lats,
        mode='lines',
        line=dict(width=0.5, color='rgba(100, 100, 100, 0.3)'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Highlight path if provided
    if highlight_path and len(highlight_path) > 1:
        path_lats = []
        path_lons = []
        
        for airport_code in highlight_path:
            airport = network.get_airport(airport_code)
            if airport:
                path_lats.append(airport.latitude)
                path_lons.append(airport.longitude)
        
        fig.add_trace(go.Scattergeo(
            lon=path_lons,
            lat=path_lats,
            mode='lines',
            line=dict(width=3, color='red'),
            name='Highlighted Path',
            hoverinfo='skip'
        ))
    
    # Draw all airport nodes
    airport_lats = []
    airport_lons = []
    airport_sizes = []
    airport_labels = []
    airport_hover = []
    
    for airport_code, airport in network.airports.items():
        airport_lats.append(airport.latitude)
        airport_lons.append(airport.longitude)
        
        # Size based on connectivity (normalized)
        num_connections = connectivity[airport_code]
        size = 5 + (num_connections / max_connections) * 15  # Range: 5-20
        airport_sizes.append(size)
        
        airport_labels.append(airport.code)
        airport_hover.append(
            f"{airport.code} - {airport.city}<br>"
            f"Connections: {num_connections}"
        )
    
    # Color airports in highlighted path differently
    if highlight_path:
        colors = ['red' if code in highlight_path else 'blue' for code in network.airports.keys()]
    else:
        colors = 'blue'
    
    fig.add_trace(go.Scattergeo(
        lon=airport_lons,
        lat=airport_lats,
        mode='markers',
        marker=dict(
            size=airport_sizes,
            color=colors,
            symbol='circle',
            line=dict(width=0.5, color='white')
        ),
        text=airport_labels,
        hovertext=airport_hover,
        hoverinfo='text',
        name='Airports'
    ))
    
    # Update layout
    fig.update_geos(
        projection_type="albers usa",
        showland=True,
        landcolor='rgb(243, 243, 243)',
        coastlinecolor='rgb(204, 204, 204)',
        showlakes=True,
        lakecolor='rgb(255, 255, 255)'
    )
    
    title = "Flight Network Graph"
    if highlight_path:
        title += f" (Highlighting: {' → '.join(highlight_path)})"
    
    fig.update_layout(
        title=title,
        showlegend=True,
        geo=dict(scope='usa'),
        height=700
    )
    
    fig.show()


def plot_algorithm_comparison(benchmark_results: Dict) -> None:
    """
    Create visualizations comparing algorithm performance.
    
    Args:
        benchmark_results: Results from algorithm benchmarking
    """
    # TODO: Create bar charts comparing execution times
    # TODO: Plot nodes visited comparison
    # TODO: Show memory usage differences
    # TODO: Create scatter plots for path length vs time
    # TODO: Generate performance distribution histograms
    pass


def plot_search_space(network: FlightNetwork, source: str, destination: str,
                     visited_nodes: List[str], algorithm: str = "Dijkstra") -> None:
    """
    Visualize the search space explored by pathfinding algorithms.
    
    Args:
        network: FlightNetwork being searched
        source: Source airport
        destination: Destination airport  
        visited_nodes: List of airports visited during search
        algorithm: Algorithm name for title
    """
    # TODO: Plot all airports in network
    # TODO: Highlight visited nodes in different color
    # TODO: Show source and destination prominently
    # TODO: Add exploration order if available
    # TODO: Compare search spaces between algorithms
    pass


def create_interactive_path_planner(network: FlightNetwork) -> None:
    """
    Create interactive web interface for path planning.
    
    Args:
        network: FlightNetwork for path planning
    """
    # TODO: Create Plotly Dash web application
    # TODO: Add dropdown menus for source/destination selection
    # TODO: Add algorithm selection (Dijkstra vs A*)
    # TODO: Add weight type selection (distance, time, cost)
    # TODO: Display results with interactive map
    # TODO: Show path statistics and comparison
    pass


def export_path_visualization(network: FlightNetwork, path: List[str], 
                            filename: str, format: str = "html") -> None:
    """
    Export path visualization to file.
    
    Args:
        network: FlightNetwork containing airport data
        path: Flight path to visualize
        filename: Output filename
        format: Export format ("html", "png", "pdf")
    """
    # TODO: Generate path visualization
    # TODO: Export in specified format
    # TODO: Handle different export formats appropriately
    # TODO: Include metadata and statistics
    pass
