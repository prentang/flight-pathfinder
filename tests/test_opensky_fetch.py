"""
Unit tests for OpenSky API fetcher with mocked responses.
"""
import unittest
from unittest.mock import patch, Mock

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

if PANDAS_AVAILABLE:
    from src.opensky_fetch import fetch_flights_from_opensky


@unittest.skipIf(not PANDAS_AVAILABLE, "pandas not available")
class TestOpenSkyFetch(unittest.TestCase):
    """Test cases for OpenSky API fetcher."""
    
    @patch('src.opensky_fetch.requests.get')
    def test_fetch_returns_dataframe(self, mock_get):
        """Test that fetch returns a pandas DataFrame."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "states": [
                [None, "UAL123", "United States", None, None, -118.0, 34.0, 10000, False, 200, 0, None, None, None, "1234", False, 0],
                [None, "AAL456", "United States", None, None, -119.0, 35.0, 11000, False, 220, 0, None, None, None, "5678", False, 0]
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        df = fetch_flights_from_opensky()
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(hasattr(df, 'head'))
    
    @patch('src.opensky_fetch.requests.get')
    def test_dataframe_columns(self, mock_get):
        """Test that DataFrame has expected columns."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "states": [
                [None, "UAL123", "United States", None, None, -118.0, 34.0, 10000, False, 200, 0, None, None, None, "1234", False, 0]
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        df = fetch_flights_from_opensky()
        
        expected = {"callsign", "origin_country", "latitude", "longitude", "velocity", "baro_altitude"}
        self.assertTrue(set(df.columns).issuperset(expected))
    
    @patch('src.opensky_fetch.requests.get')
    def test_filters_by_us_bounds(self, mock_get):
        """Test that only US flights are included."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "states": [
                [None, "UAL123", "United States", None, None, -118.0, 34.0, 10000, False, 200, 0, None, None, None, "1234", False, 0],
                [None, "EUR456", "Germany", None, None, 10.0, 50.0, 11000, False, 220, 0, None, None, None, "5678", False, 0],
                [None, "AAL789", "United States", None, None, -97.0, 32.0, 9000, False, 210, 0, None, None, None, "9012", False, 0]
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        df = fetch_flights_from_opensky()
        
        self.assertEqual(len(df), 2)
    
    @patch('src.opensky_fetch.requests.get')
    def test_handles_api_error(self, mock_get):
        """Test that API errors are handled gracefully."""
        mock_get.side_effect = Exception("API Error")
        
        df = fetch_flights_from_opensky()
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)
    
    @patch('src.opensky_fetch.requests.get')
    def test_handles_missing_coordinates(self, mock_get):
        """Test that flights with missing coordinates are filtered out."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "states": [
                [None, "UAL123", "United States", None, None, None, None, 10000, False, 200, 0, None, None, None, "1234", False, 0],
                [None, "AAL456", "United States", None, None, -118.0, 34.0, 11000, False, 220, 0, None, None, None, "5678", False, 0]
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        df = fetch_flights_from_opensky()
        
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['callsign'], "AAL456")
    
    @patch('src.opensky_fetch.requests.get')
    def test_with_authentication(self, mock_get):
        """Test that authentication credentials are passed correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"states": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        fetch_flights_from_opensky(username="test_user", password="test_pass")
        
        mock_get.assert_called_once()
        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs['auth'], ("test_user", "test_pass"))


if __name__ == "__main__":
    unittest.main()
