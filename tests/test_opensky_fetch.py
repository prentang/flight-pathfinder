"""
Unit test for OpenSky API fetcher.
"""
import unittest
from src.opensky_fetch import fetch_flights_from_opensky

class TestOpenSkyFetch(unittest.TestCase):
    def test_fetch_returns_dataframe(self):
        df = fetch_flights_from_opensky()
        self.assertTrue(hasattr(df, 'head'))  # Basic check for pandas DataFrame

    def test_dataframe_columns(self):
        df = fetch_flights_from_opensky()
        expected = {"callsign", "origin_country", "latitude", "longitude", "velocity", "baro_altitude"}
        self.assertTrue(set(df.columns).issuperset(expected))

if __name__ == "__main__":
    unittest.main()
