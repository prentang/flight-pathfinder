"""
OpenFlights package for downloading and parsing flight data.
"""

from .downloader import (
    download_openflights_data,
    parse_airports_data,
    parse_routes_data,
    get_us_airports_from_openflights,
    get_us_routes_from_openflights,
    setup_openflights_data
)

__all__ = [
    'download_openflights_data',
    'parse_airports_data', 
    'parse_routes_data',
    'get_us_airports_from_openflights',
    'get_us_routes_from_openflights',
    'setup_openflights_data'
]
