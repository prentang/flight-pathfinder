"""
Main script for flight-pathfinder project.
Fetches, cleans, and visualizes live flight data using OpenSky REST API.
"""
from src.opensky_fetch import fetch_flights_from_opensky
from visualization.plot_aircraft import plot_aircraft_positions
from utils.logging_utils import setup_logger


def main():
    logger = setup_logger()
    # Optionally set your OpenSky credentials for higher rate limits
    # username = "your_username"
    # password = "your_password"
    username = None
    password = None
    logger.info("Fetching live flight data from OpenSky API...")
    df = fetch_flights_from_opensky(username, password)
    logger.info(f"Fetched {len(df)} flights over the continental US.")
    print(df.head())

    # Optional: Visualize aircraft positions
    if not df.empty:
        plot_aircraft_positions(df)

if __name__ == "__main__":
    main()
