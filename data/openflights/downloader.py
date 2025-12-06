"""
OpenFlights data downloader and parser.
Downloads and processes OpenFlights dataset for airport and route information.
"""
import requests
import pandas as pd
import os
from typing import Optional
from pathlib import Path


# OpenFlights data URLs
OPENFLIGHTS_URLS = {
    "airports": "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat",
    "routes": "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat",
    "airlines": "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat"
}

# Data file paths
DATA_DIR = Path(__file__).parent
AIRPORTS_FILE = DATA_DIR / "airports.dat"
ROUTES_FILE = DATA_DIR / "routes.dat"
AIRLINES_FILE = DATA_DIR / "airlines.dat"


def download_openflights_data(force_refresh: bool = False) -> None:
    """
    Download OpenFlights dataset files.
    
    Args:
        force_refresh: If True, re-download even if files exist
    """
    # TODO: Check if data files already exist (unless force_refresh=True)
    # TODO: Create data directory if it doesn't exist
    # TODO: Download airports.dat from OpenFlights GitHub
    # TODO: Download routes.dat from OpenFlights GitHub  
    # TODO: Download airlines.dat from OpenFlights GitHub (optional)
    # TODO: Handle download errors gracefully
    # TODO: Verify downloaded files are valid (not empty, correct format)
    # TODO: Log download progress and file sizes
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)
        
    for name, url in OPENFLIGHTS_URLS.items():
        file_path = DATA_DIR / f"{name}.dat"
        if file_path.exists() and not force_refresh:
            print(f"Skipping {name} download, file already exists")
            continue
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            content = response.text.strip()

            if not content or "," not in content:
                raise ValueError("Downloaded file is empty or invalid.")

            file_path.write_text(content, encoding="utf-8")
            print(f"Downloaded {file_path.name} ({len(content)} bytes)")
        
        except Exception as e:
            print(f"Failed to download {name} data: {e}")
            

def parse_airports_data() -> pd.DataFrame:
    """
    Parse OpenFlights airports.dat file into pandas DataFrame.
    
    Returns:
        DataFrame with airport information
    """
    # TODO: Read airports.dat file (CSV format, no headers)
    # TODO: Define column names for airports data:
    #       Airport ID, Name, City, Country, IATA, ICAO, Latitude, Longitude, 
    #       Altitude, Timezone, DST, Tz database time zone
    # TODO: Handle missing values (\\N in OpenFlights data)
    # TODO: Convert latitude/longitude to float
    # TODO: Convert altitude to int
    # TODO: Filter out airports with missing IATA codes if needed
    # TODO: Clean up airport names and city names
    # TODO: Return standardized DataFrame
    airports = pd.read_csv(AIRPORTS_FILE, header=None)
    airports.columns = [
        "Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz database time zone", "Type", "Source"
    ]

    # Convert latitude/longitude to float and altitude to int
    airports["Latitude"] = airports["Latitude"].astype(float)
    airports["Longitude"] = airports["Longitude"].astype(float)
    airports["Altitude"] = airports["Altitude"].astype(int)

    # Filter out the airports with missing IATA codes
    airports = airports[airports["IATA"].notna() & (airports["IATA"] != "")]

    # Clean up airport names and city names
    airports["Name"] = airports["Name"].str.strip()
    airports["City"] = airports["City"].str.strip()

    # Return cleaned DataFrame
    return airports


def parse_routes_data() -> pd.DataFrame:
    """
    Parse OpenFlights routes.dat file into pandas DataFrame.
    
    Returns:
        DataFrame with route information
    """
    # TODO: Read routes.dat file (CSV format, no headers)
    # TODO: Define column names for routes data:
    #       Airline, Airline ID, Source airport, Source airport ID,
    #       Destination airport, Destination airport ID, Codeshare, Stops, Equipment
    # TODO: Handle missing values (\\N in OpenFlights data)
    # TODO: Filter routes to only include valid airport codes
    # TODO: Remove routes with stops > 0 if you want direct flights only
    # TODO: Clean airline and airport codes
    # TODO: Return standardized DataFrame
    routes = pd.read_csv(ROUTES_FILE, header=None, na_values="\\N")

    routes.columns = [
        "Airline", "Airline ID", "Source airport", "Source airport ID", "Destination airport", "Destination airport ID", "Codeshare", "Stops", "Equipment"
    ]

    # Convert Stops to numeric
    routes["Stops"] = pd.to_numeric(routes["Stops"], errors="coerce").fillna(0).astype(int)

    # Filter out the routes with stops > 0
    routes = routes[routes["Stops"] == 0]

    # Clean code columns (strip spaces, uppercase)
    for col in ["Airline", "Source airport", "Destination airport"]:
        routes[col] = routes[col].astype(str).str.strip().str.upper()

    # Drop routes missing essential codes
    routes = routes[
        routes["Source airport"].notna() &
        routes["Destination airport"].notna() &
        (routes["Source airport"] != "") &
        (routes["Destination airport"] != "")
    ]

    # Return cleaned DataFrame
    return routes


def parse_airlines_data() -> pd.DataFrame:
    """
    Parse OpenFlights airlines.dat file into pandas DataFrame.
    
    Returns:
        DataFrame with airline information
    """
    # TODO: Read airlines.dat file (CSV format, no headers)
    # TODO: Define column names for airlines data:
    #       Airline ID, Name, Alias, IATA, ICAO, Callsign, Country, Active
    # TODO: Handle missing values (\\N in OpenFlights data)
    # TODO: Filter to active airlines only
    # TODO: Clean airline names and codes
    # TODO: Return standardized DataFrame
    airlines = pd.read_csv(AIRLINES_FILE, header=None, na_values="\\N")
    airlines.columns = [
        "Airline ID", "Name", "Alias", "IATA", "ICAO", "Callsign", "Country", "Active"
    ]

    # Filter to active airlines only
    airlines = airlines[airlines["Active"].astype(str).str.upper() == "Y"]

    # Clean up airline names and codes
    airlines["Name"] = airlines["Name"].str.strip()
    airlines["Alias"] = airlines["Alias"].astype(str).str.strip()
    airlines["IATA"] = airlines["IATA"].astype(str).str.strip().str.upper()
    airlines["ICAO"] = airlines["ICAO"].astype(str).str.strip().str.upper()
    airlines["Callsign"] = airlines["Callsign"].astype(str).str.strip()
    airlines["Country"] = airlines["Country"].astype(str).str.strip()

    # Return cleaned DataFrame
    return airlines


def get_us_airports_from_openflights() -> pd.DataFrame:
    """
    Get filtered dataset of US airports from OpenFlights data.
    
    Returns:
        DataFrame containing only US airports
    """
    # TODO: Load airports data using parse_airports_data()
    # TODO: Filter to United States airports (Country == "United States")
    # TODO: Validate US coordinates are within continental US bounds:
    #       Lat: 24.396308 to 49.384358
    #       Lon: -125.0 to -66.93457
    # TODO: Remove airports without valid IATA codes
    # TODO: Sort by airport size/importance if data available
    # TODO: Return filtered US airports DataFrame
    
    airports = parse_airports_data()

    airports = airports[airports["Country"] == "United States"]

    # Validate US coordinates are withi contienental US bounds
    airports = airports[
        (airports["Latitude"].between(24.396308, 49.384358)) & 
        (airports["Longitude"].between(-125.0, -66.93457))
    ]
    # Remove airports without valid IATA codes
    airports = airports[airports["IATA"].notna() & (airports["IATA"] != "")]

    # Sort by airport size/importance if data available
    airports = airports.sort_values(by="Name")

    return airports


def get_us_routes_from_openflights() -> pd.DataFrame:
    """
    Get filtered dataset of US domestic routes from OpenFlights data.
    
    Returns:
        DataFrame containing routes between US airports
    """
    # TODO: Load routes data using parse_routes_data()
    # TODO: Load US airports data to get valid US airport codes
    # TODO: Filter routes where both source and destination are US airports
    # TODO: Remove routes with stops (keep direct flights only)
    # TODO: Remove inactive/codeshare routes if needed
    # TODO: Return filtered US domestic routes DataFrame
    routes = parse_routes_data()

    us_airports = get_us_airports_from_openflights()
    us_code = set(us_airports["IATA"])
    
    routes_filtered = routes[
        (routes["Source airport"].isin(us_code)) &
        (routes["Destination airport"].isin(us_code))
    ]

    # Remove routes with stops
    routes_filtered = routes_filtered[routes_filtered["Stops"] == 0]
    
    # Remove inactive/codeshare routes if needed
    routes_filtered = routes_filtered[routes_filtered["Codeshare"].isna() | (routes_filtered["Codeshare"] == "")]

    return routes_filtered

def validate_openflights_data() -> dict:
    """
    Validate downloaded and parsed OpenFlights data.
    
    Returns:
        Dictionary with validation results and statistics
    """
    # TODO: Check if all required files exist
    # TODO: Validate airports data:
    #       - Check for required columns
    #       - Validate coordinate ranges
    #       - Check for duplicate airport codes
    # TODO: Validate routes data:
    #       - Check for required columns  
    #       - Verify airport codes exist in airports data
    #       - Check for circular routes (source == destination)
    # TODO: Generate statistics:
    #       - Total airports, US airports
    #       - Total routes, US domestic routes
    #       - Data quality metrics
    # TODO: Return validation report dictionary
    
    if not AIRPORTS_FILE.exists():
        raise FileNotFoundError("Airports data file not found. Please run download_openflights_data() first.")
    if not ROUTES_FILE.exists():
        raise FileNotFoundError("Routes data file not found. Please run download_openflights_data() first.")
    if not AIRLINES_FILE.exists():
        raise FileNotFoundError("Airlines data file not found. Please run download_openflights_data() first.")

    # Load Data
    airports = parse_airports_data()
    routes = parse_routes_data()
    airlines = parse_airlines_data()

    report= {"status": "OK", "errors": [], "warnings": [], "stats": {}}

    # Validate Airports Data
    required_airport_cols = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz database time zone"]
    missing_cols = [col for col in required_airport_cols if col not in airports.columns]

    if missing_cols:
        report["status"] = "ERROR"
        report["errors"].append(f"Airports data is missing required columns: {missing_cols}")
    
    # Validate Coordinate Ranges
    invalid_lon = airports[(airports["Longitude"] < -180) | (airports["Longitude"] > 180)] 
    if len(invalid_lon) > 0:
        report["errors"].append(f"Found {len(invalid_lon)} airports with invalid longitude")
        report["status"] = "ERROR"
    invalid_lat = airports[(airports["Latitude"] < -90) | (airports["Latitude"] > 90)]
    if len(invalid_lat) > 0:
        report["errors"].append(f"Found {len(invalid_lat)} airports with invalid latitude")
        report["status"] = "ERROR"

    # Check for Duplicate Airport Codes
    dupe_iata = airports[airports["IATA"].duplicated(keep=False)]
    if len(dupe_iata) > 0:
        report["warnings"].append(f"Found {len(dupe_iata)} duplicate IATA codes")
    dupe_icao = airports[airports["ICAO"].duplicated(keep=False)]
    if len(dupe_icao) > 0:
        report["warnings"].append(f"Found {len(dupe_icao)} duplicate ICAO codes")

    # Validate Routes Data
    required_route_cols = ["Airline", "Airline ID", "Source airport", "Source airport ID", "Destination airport", "Destination airport ID", "Codeshare", "Stops", "Equipment"]
    missing_cols = [col for col in required_route_cols if col not in routes.columns]

    if missing_cols:
        report["status"] = "ERROR"
        report["errors"].append(f"Routes data is missing required columns: {missing_cols}")

    # Validate Airport Codes Exist in Airports Data
    valid_iata_codes = set(airports["IATA"].dropna())
    invalid_source = routes[~routes["Source airport"].isin(valid_iata_codes)]
    if len(invalid_source) > 0:
        report["warnings"].append(f"Found {len(invalid_source)} routes with invalid source airport codes") 
    invalid_dest = routes[~routes["Destination airport"].isin(valid_iata_codes)]
    if len(invalid_dest) > 0:
        report["warnings"].append(f"Found {len(invalid_dest)} routes with invalid destination airport codes")
    
    # Check for circular routes (source == destination)
    circular = routes[routes["Source airport"] == routes["Destination airport"]]
    if len(circular) > 0:
        report["warnings"].append(f"Found {len(circular)} circular routes (source == destination)")

    # Generate Statistics
    us_airports = get_us_airports_from_openflights()
    us_airport_count = set(us_airports["IATA"])
    us_routes = routes[(routes["Source airport"].isin(us_airport_count) & routes["Destination airport"].isin(us_airport_count))]

    report["stats"] = {
        "total_airports": len(airports),
        "us_airports": len(us_airports),
        "total_routes": len(routes),
        "total_airlines": len(airlines),
        "us_domestic_routes": len(us_routes),
        "airports_with_iata": len(airports[airports["IATA"].notna()]),
        "direct_flights_only": len(routes[routes["Stops"] == 0]),
        "data_quality": {
            "airports_missing_coordinates": len(airports[airports["Latitude"].isna() | airports["Longitude"].isna()]),
            "routes_with_stops": len(routes[routes["Stops"] > 0]),
            "invalid_source_airports": len(invalid_source),
            "invalid_dest_airports": len(invalid_dest),
            "circular_routes": len(circular)
        }
    }
    return report
    


def setup_openflights_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Complete setup: download, parse, and return US airports and routes data.
    
    Returns:
        Tuple of (us_airports_df, us_routes_df)
    """
    print("=" * 60)
    print("OpenFlights Data Setup")
    print("=" * 60)
    
    # Download OpenFlights data if not already present
    print("\n[1/4] Checking for data files...")
    if not (AIRPORTS_FILE.exists() and ROUTES_FILE.exists() and AIRLINES_FILE.exists()):
        print("Data files not found. Downloading...")
        download_openflights_data(force_refresh=False)
    else:
        print("Data files already exist. Skipping download.")
    
    # Parse and filter to US airports
    print("\n[2/4] Parsing and filtering US airports...")
    us_airports = get_us_airports_from_openflights()
    print(f"Found {len(us_airports)} US airports")
    
    # Parse and filter to US domestic routes
    print("\n[3/4] Parsing and filtering US domestic routes...")
    us_routes = get_us_routes_from_openflights()
    print(f"Found {len(us_routes)} US domestic routes")
    
    # Validate data integrity
    print("\n[4/4] Validating data integrity...")
    try:
        validation_report = validate_openflights_data()
        
        if validation_report["status"] == "OK":
            print("✓ Data validation passed")
        else:
            print("✗ Data validation found errors:")
            for error in validation_report["errors"]:
                print(f"  - {error}")
        
        if validation_report["warnings"]:
            print("\nWarnings:")
            for warning in validation_report["warnings"]:
                print(f"  - {warning}")
        
        # Log setup completion and data statistics
        print("\n" + "=" * 60)
        print("Setup Complete - Data Statistics")
        print("=" * 60)
        stats = validation_report["stats"]
        print(f"Total airports:        {stats['total_airports']}")
        print(f"US airports:           {stats['us_airports']}")
        print(f"Total routes:          {stats['total_routes']}")
        print(f"US domestic routes:    {stats['us_domestic_routes']}")
        print(f"Total airlines:        {stats['total_airlines']}")
        print("=" * 60)
        
    except Exception as e:
        print(f"⚠ Validation failed: {e}")
        print("Proceeding with data anyway...")
    
    # Return tuple of US airports and routes DataFrames
    # Standardize column names for compatibility with FlightNetwork
    us_airports_standardized = us_airports.rename(columns={
        'IATA': 'iata_code',
        'Name': 'name',
        'City': 'city',
        'Country': 'country',
        'Latitude': 'latitude',
        'Longitude': 'longitude'
    })
    
    us_routes_standardized = us_routes.rename(columns={
        'Source airport': 'source_airport',
        'Destination airport': 'dest_airport'
    })
    
    # Calculate distances for routes
    from data.route_loader import calculate_distance
    us_routes_standardized['distance_km'] = us_routes_standardized.apply(
        lambda row: calculate_distance(
            us_airports_standardized[us_airports_standardized['iata_code'] == row['source_airport']]['latitude'].values[0],
            us_airports_standardized[us_airports_standardized['iata_code'] == row['source_airport']]['longitude'].values[0],
            us_airports_standardized[us_airports_standardized['iata_code'] == row['dest_airport']]['latitude'].values[0],
            us_airports_standardized[us_airports_standardized['iata_code'] == row['dest_airport']]['longitude'].values[0]
        ) if len(us_airports_standardized[us_airports_standardized['iata_code'] == row['source_airport']]) > 0 
           and len(us_airports_standardized[us_airports_standardized['iata_code'] == row['dest_airport']]) > 0
        else 0,
        axis=1
    )
    
    # Filter out routes with 0 distance (missing airports)
    us_routes_standardized = us_routes_standardized[us_routes_standardized['distance_km'] > 0]
    
    return us_airports_standardized, us_routes_standardized


if __name__ == "__main__":
    import argparse
    
    # Command-line interface for data download and setup
    parser = argparse.ArgumentParser(
        description="Download and process OpenFlights airport and route data"
    )
    
    # Parse command-line arguments
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Force re-download of data files even if they exist"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run validation only (don't download or setup)"
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Download data files only (don't parse or validate)"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show detailed statistics about the data"
    )
    
    args = parser.parse_args()
    
    try:
        # Download and setup data
        if args.download_only:
            print("Downloading OpenFlights data...")
            download_openflights_data(force_refresh=args.force_refresh)
            print("✓ Download complete")
            
        elif args.validate:
            print("Validating OpenFlights data...")
            report = validate_openflights_data()
            
            # Print data statistics and validation results
            print("\n" + "=" * 60)
            print("Validation Report")
            print("=" * 60)
            print(f"Status: {report['status']}")
            
            if report['errors']:
                print("\nErrors:")
                for error in report['errors']:
                    print(f"  ✗ {error}")
            
            if report['warnings']:
                print("\nWarnings:")
                for warning in report['warnings']:
                    print(f"  ⚠ {warning}")
            
            print("\n" + "=" * 60)
            print("Statistics")
            print("=" * 60)
            stats = report['stats']
            print(f"Total airports:           {stats['total_airports']}")
            print(f"US airports:              {stats['us_airports']}")
            print(f"Airports with IATA:       {stats['airports_with_iata']}")
            print(f"Total routes:             {stats['total_routes']}")
            print(f"US domestic routes:       {stats['us_domestic_routes']}")
            print(f"Direct flights only:      {stats['direct_flights_only']}")
            print(f"Total airlines:           {stats['total_airlines']}")
            
            if args.stats:
                print("\n" + "=" * 60)
                print("Data Quality Metrics")
                print("=" * 60)
                dq = stats['data_quality']
                print(f"Missing coordinates:      {dq['airports_missing_coordinates']}")
                print(f"Routes with stops:        {dq['routes_with_stops']}")
                print(f"Invalid source airports:  {dq['invalid_source_airports']}")
                print(f"Invalid dest airports:    {dq['invalid_dest_airports']}")
                print(f"Circular routes:          {dq['circular_routes']}")
            
            print("=" * 60)
            
        else:
            # Full setup
            if args.force_refresh:
                print("Force refresh enabled - re-downloading data...")
                download_openflights_data(force_refresh=True)
            
            us_airports, us_routes = setup_openflights_data()
            
            if args.stats:
                print("\n" + "=" * 60)
                print("Sample Data Preview")
                print("=" * 60)
                print("\nTop 5 US Airports:")
                print(us_airports[["IATA", "Name", "City"]].head())
                print("\nSample Routes:")
                print(us_routes[["Source airport", "Destination airport", "Airline"]].head())
                print("=" * 60)
            
            print("\n✓ Setup complete! Data is ready to use.")
    
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("Run with --download-only first to download the data files.")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
