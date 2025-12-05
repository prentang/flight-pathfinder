from typing import Dict, List, Tuple, Optional


def load_airport_data(filepath: str) -> Dict:
    """
    Load airport data from a file.
    
    Args:
        filepath: Path to the airport data file
        
    Returns:
        Dictionary containing airport data
    """
    raise NotImplementedError("load_airport_data not yet implemented")


def get_us_airports() -> List[Dict]:
    """
    Get list of US airports.
    
    Returns:
        List of dictionaries containing US airport data
    """
    raise NotImplementedError("get_us_airports not yet implemented")


def get_airport_coordinates(airport_code: str) -> Optional[Tuple[float, float]]:
    """
    Get coordinates for an airport.
    
    Args:
        airport_code: IATA airport code
        
    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    raise NotImplementedError("get_airport_coordinates not yet implemented")


def validate_airport_code(airport_code: str) -> bool:
    """
    Validate an airport code.
    
    Args:
        airport_code: IATA airport code to validate
        
    Returns:
        True if valid, False otherwise
    """
    raise NotImplementedError("validate_airport_code not yet implemented")
