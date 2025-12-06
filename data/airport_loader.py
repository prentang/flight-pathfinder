from typing import Dict, List, Tuple, Optional
import pandas as pd


def load_airport_data(filepath: str) -> pd.DataFrame:
    """
    Load airport data from a CSV file.
    
    Args:
        filepath: Path to the airport data file (CSV format)
        
    Returns:
        DataFrame with columns: iata_code, name, city, country, latitude, longitude
    """
    df = pd.read_csv(filepath)
    
    # Standardize column names if needed
    expected_columns = ['iata_code', 'name', 'city', 'country', 'latitude', 'longitude']
    
    # If columns don't match, try to map common variations
    if not all(col in df.columns for col in expected_columns):
        column_mapping = {
            'code': 'iata_code',
            'airport_code': 'iata_code',
            'airport_name': 'name',
            'lat': 'latitude',
            'lon': 'longitude',
            'lng': 'longitude'
        }
        df = df.rename(columns=column_mapping)
    
    # Filter to only required columns
    df = df[expected_columns]
    
    # Remove rows with missing IATA codes
    df = df.dropna(subset=['iata_code'])
    
    return df


def get_us_airports(airports_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter airports to US only.
    
    Args:
        airports_df: DataFrame with airport data
        
    Returns:
        DataFrame containing only US airports
    """
    us_df = airports_df[airports_df['country'] == 'United States'].copy()
    
    # Additional filtering for continental US (optional)
    # Latitude roughly 24°N to 49°N, Longitude roughly -125°W to -67°W
    us_df = us_df[
        (us_df['latitude'] >= 24.0) & (us_df['latitude'] <= 49.0) &
        (us_df['longitude'] >= -125.0) & (us_df['longitude'] <= -67.0)
    ]
    
    return us_df


def get_airport_coordinates(airport_code: str, airports_df: pd.DataFrame) -> Optional[Tuple[float, float]]:
    """
    Get coordinates for an airport from a DataFrame.
    
    Args:
        airport_code: IATA airport code
        airports_df: DataFrame with airport data
        
    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    airport = airports_df[airports_df['iata_code'] == airport_code]
    
    if airport.empty:
        return None
    
    row = airport.iloc[0]
    return (row['latitude'], row['longitude'])


def validate_airport_code(airport_code: str, airports_df: pd.DataFrame) -> bool:
    """
    Validate that an airport code exists in the dataset.
    
    Args:
        airport_code: IATA airport code to validate
        airports_df: DataFrame with airport data
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(airport_code, str) or len(airport_code) != 3:
        return False
    
    return airport_code in airports_df['iata_code'].values

