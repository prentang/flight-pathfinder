"""
Airport data loader module.
Handles loading and processing airport data from OpenFlights and other sources.
"""
import pandas as pd
from typing import Dict, Optional
from models.graph import Airport
from utils.logging_utils import setup_logger
from pathlib import Path

logger = setup_logger("airport_loader")

AIRPORTS_FILE = Path(__file__).parent / "openflights" / "airports.dat"


def load_airport_data(source: str = "openflights") -> Dict[str, Airport]:
    """
    Load airport data from specified source.
    Args:
        source: Data source (default: "openflights")
    Returns:
        Dictionary of airport code -> Airport object
    """
    airports = {}
    try:
        df = pd.read_csv(
            AIRPORTS_FILE,
            header=None,
            names=[
                "id", "name", "city", "country", "iata", "icao", "latitude", "longitude", "altitude", "timezone", "dst", "tz", "type", "source"
            ],
            dtype={"iata": str, "icao": str},
            na_values=["\\N", ""],
            quotechar='"',
            encoding="utf-8"
        )
        for _, row in df.iterrows():
            code = row["iata"] if pd.notna(row["iata"]) and row["iata"] else row["icao"]
            if not code or pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
                continue
            airport = Airport(
                code=code,
                name=row["name"],
                city=row["city"],
                country=row["country"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"])
            )
            airports[code] = airport
        logger.info(f"Loaded {len(airports)} airports from {AIRPORTS_FILE}")
    except Exception as e:
        logger.error(f"Failed to load airport data: {e}")
    return airports


def get_us_airports(airports: Optional[Dict[str, Airport]] = None) -> Dict[str, Airport]:
    """
    Filter and return US airports only.
    Args:
        airports: Optional dict of airports (if None, loads all)
    Returns:
        Dictionary of US airport code -> Airport object
    """
    if airports is None:
        airports = load_airport_data()
    us_airports = {code: ap for code, ap in airports.items() if ap.country == "United States"}
    logger.info(f"Filtered {len(us_airports)} US airports")
    return us_airports


def get_airport_coordinates(code: str, airports: Optional[Dict[str, Airport]] = None) -> Optional[tuple]:
    """
    Get latitude and longitude for a given airport code.
    Args:
        code: Airport IATA/ICAO code
        airports: Optional dict of airports
    Returns:
        (latitude, longitude) tuple or None
    """
    if airports is None:
        airports = load_airport_data()
    airport = airports.get(code)
    if airport:
        return (airport.latitude, airport.longitude)
    return None


def validate_airport_code(code: str, airports: Optional[Dict[str, Airport]] = None) -> bool:
    """
    Validate if an airport code exists in the dataset.
    Args:
        code: Airport IATA/ICAO code
        airports: Optional dict of airports
    Returns:
        True if valid, False otherwise
    """
    if airports is None:
        airports = load_airport_data()
    return code in airports
