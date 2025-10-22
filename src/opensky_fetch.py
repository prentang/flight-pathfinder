"""
OpenSky API fetcher module
Handles all API requests and data retrieval from OpenSky Network.
"""
import requests
import pandas as pd
from typing import Optional

API_URL = "https://opensky-network.org/api/states/all"

# Continental US bounding box (approximate)
US_BOUNDS = {
    "min_lat": 24.396308,
    "max_lat": 49.384358,
    "min_lon": -125.0,
    "max_lon": -66.93457
}

def fetch_flights_from_opensky(username: Optional[str] = None, password: Optional[str] = None) -> pd.DataFrame:
    """
    Fetch live aircraft states from OpenSky API, filter to continental US, and return as DataFrame.
    """
    auth = (username, password) if username and password else None
    try:
        response = requests.get(API_URL, auth=auth, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return pd.DataFrame()

    data = response.json()
    states = data.get("states", [])
    filtered = []
    for s in states:
        lon, lat = s[5], s[6]
        if lat is None or lon is None:
            continue
        if (US_BOUNDS["min_lat"] <= lat <= US_BOUNDS["max_lat"] and
            US_BOUNDS["min_lon"] <= lon <= US_BOUNDS["max_lon"]):
            filtered.append({
                "callsign": s[1],
                "origin_country": s[2],
                "latitude": lat,
                "longitude": lon,
                "velocity": s[9],
                "baro_altitude": s[7]
            })
    df = pd.DataFrame(filtered)
    print(f"Fetched {len(df)} flights over the continental US.")
    return df
