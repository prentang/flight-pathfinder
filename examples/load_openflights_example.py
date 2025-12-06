"""
Example: Load OpenFlights data into FlightNetwork

This script demonstrates how to:
1. Download and parse OpenFlights data
2. Filter to US airports and routes
3. Load data into FlightNetwork for pathfinding
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data.openflights.downloader import setup_openflights_data
from models.graph import FlightNetwork


def main():
    print("=" * 60)
    print("OpenFlights Data Loading Example")
    print("=" * 60)
    
    # Step 1: Download and setup OpenFlights data
    print("\n[1/3] Downloading and processing OpenFlights data...")
    us_airports_df, us_routes_df = setup_openflights_data()
    
    print(f"\nLoaded {len(us_airports_df)} US airports")
    print(f"Loaded {len(us_routes_df)} US routes")
    
    # Show sample airports
    print("\nSample airports:")
    print(us_airports_df[['iata_code', 'name', 'city', 'latitude', 'longitude']].head(10))
    
    # Show sample routes
    print("\nSample routes:")
    print(us_routes_df[['source_airport', 'dest_airport', 'distance_km']].head(10))
    
    # Step 2: Create FlightNetwork and load data
    print("\n[2/3] Creating FlightNetwork and loading data...")
    network = FlightNetwork()
    network.load_from_dataframes(us_airports_df, us_routes_df)
    
    print(f"\nNetwork created with:")
    print(f"  - {len(network.airports)} airports")
    print(f"  - {sum(len(routes) for routes in network.adjacency_list.values())} routes")
    
    # Step 3: Verify network is working
    print("\n[3/3] Verifying network functionality...")
    
    # Check a few major airports
    major_airports = ['LAX', 'JFK', 'ORD', 'DFW', 'ATL']
    print("\nMajor airports in network:")
    for code in major_airports:
        airport = network.get_airport(code)
        if airport:
            num_routes = len(network.get_neighbors(code))
            print(f"  {code}: {airport.name} ({airport.city}) - {num_routes} outbound routes")
        else:
            print(f"  {code}: Not found in network")
    
    # Show connectivity example
    print("\nExample: Routes from LAX:")
    lax_routes = network.get_neighbors('LAX')
    print(f"  LAX has {len(lax_routes)} direct routes")
    if lax_routes:
        print(f"  First 5 destinations:")
        for dest, distance in sorted(lax_routes, key=lambda x: x[1])[:5]:
            dest_airport = network.get_airport(dest)
            if dest_airport:
                print(f"    -> {dest} ({dest_airport.city}): {distance:.0f} km")
    
    print("\n" + "=" * 60)
    print("Data loading complete! Network ready for pathfinding.")
    print("=" * 60)


if __name__ == "__main__":
    main()
