"""
Route data loader module.
Handles loading and processing flight route data between airports.
"""
from typing import Dict, List, Tuple, Optional, TYPE_CHECKING
import math
import pandas as pd

if TYPE_CHECKING:
    import pandas as pd


def load_route_data(filepath: str) -> pd.DataFrame:
    """
    Load flight route data from a CSV file.
    
    Args:
        filepath: Path to the route data file (CSV format)
    
    Returns:
        DataFrame with columns: airline, source_airport, dest_airport, equipment, stops
    """
    df = pd.read_csv(filepath)
    
    # Standardize column names if needed
    column_mapping = {
        'source': 'source_airport',
        'destination': 'dest_airport',
        'dest': 'dest_airport',
        'codeshare': 'equipment',
        'num_stops': 'stops'
    }
    df = df.rename(columns=column_mapping)
    
    # Filter to direct flights only (stops == 0)
    if 'stops' in df.columns:
        df = df[df['stops'] == 0]
    
    return df


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great circle distance between two points using Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
    
    Returns:
        Distance in kilometers
    """
    # TODO: Implement Haversine formula for great circle distance
    # TODO: Convert degrees to radians
    # TODO: Apply Haversine formula: a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    # TODO: Calculate c = 2 ⋅ atan2(√a, √(1−a))
    # TODO: Return distance = R ⋅ c (where R = Earth's radius ≈ 6371 km)
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) **2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    R = 6371.0
    return R * c

def estimate_flight_time(distance_km: float, aircraft_speed_kmh: float = 800) -> float:
    """
    Estimate flight time based on distance and average aircraft speed.
    
    Args:
        distance_km: Distance in kilometers
        aircraft_speed_kmh: Average aircraft speed in km/h (default 800 km/h)
    
    Returns:
        Estimated flight time in hours
    """
    # Base flight time
    flight_time = distance_km / aircraft_speed_kmh
    
    # Add overhead for taxi, takeoff, landing (0.5 hours = 30 minutes)
    overhead_hours = 0.5
    
    # For very short flights, use minimum time
    min_flight_time = 0.75  # 45 minutes minimum
    
    total_time = flight_time + overhead_hours
    return max(total_time, min_flight_time)


def generate_route_network(airports_df: pd.DataFrame, max_distance_km: float = 5000) -> pd.DataFrame:
    """
    Generate all possible routes between airports within distance threshold.
    
    Args:
        airports_df: DataFrame with airport data (must have iata_code, latitude, longitude)
        max_distance_km: Maximum distance for direct routes (default 5000 km)
    
    Returns:
        DataFrame with columns: source_airport, dest_airport, distance_km, flight_time_hours
    """
    routes = []
    airports_list = airports_df.to_dict('records')
    
    # Generate routes between all airport pairs
    for i, src_airport in enumerate(airports_list):
        for dest_airport in airports_list[i+1:]:  # Avoid duplicates and self-loops
            # Calculate distance
            distance = calculate_distance(
                src_airport['latitude'], src_airport['longitude'],
                dest_airport['latitude'], dest_airport['longitude']
            )
            
            # Filter by max distance (realistic for commercial flights)
            if distance <= max_distance_km and distance >= 50:  # Min 50km to avoid too short
                flight_time = estimate_flight_time(distance)
                
                # Add both directions (bidirectional routes)
                routes.append({
                    'source_airport': src_airport['iata_code'],
                    'dest_airport': dest_airport['iata_code'],
                    'distance_km': round(distance, 2),
                    'flight_time_hours': round(flight_time, 2)
                })
                routes.append({
                    'source_airport': dest_airport['iata_code'],
                    'dest_airport': src_airport['iata_code'],
                    'distance_km': round(distance, 2),
                    'flight_time_hours': round(flight_time, 2)
                })
    
    return pd.DataFrame(routes)


def add_route_weights(routes_df: pd.DataFrame, weight_type: str = "distance") -> pd.DataFrame:
    """
    Add weight column to routes for pathfinding algorithms.
    
    Args:
        routes_df: DataFrame with route data (must have distance_km, flight_time_hours)
        weight_type: Type of weight to use ("distance", "time", "cost")
    
    Returns:
        DataFrame with added 'weight' column
    """
    routes_with_weights = routes_df.copy()
    
    if weight_type == "distance":
        # Use distance in km as weight
        routes_with_weights['weight'] = routes_df['distance_km']
    elif weight_type == "time":
        # Use flight time in hours as weight
        routes_with_weights['weight'] = routes_df['flight_time_hours']
    elif weight_type == "cost":
        # Estimate cost based on distance (rough approximation: $0.15 per km)
        routes_with_weights['weight'] = routes_df['distance_km'] * 0.15
    else:
        raise ValueError(f"Unknown weight_type: {weight_type}. Use 'distance', 'time', or 'cost'.")
    
    return routes_with_weights
