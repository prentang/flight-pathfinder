# OpenFlights Data Setup

## 📁 Folder Structure
```
data/openflights/
├── __init__.py           # Package initialization
├── downloader.py         # Main data download and parsing logic
├── README.md            # This file - setup instructions
├── airports.dat         # Downloaded airport data (created after download)
├── routes.dat          # Downloaded route data (created after download)
└── airlines.dat        # Downloaded airline data (created after download)
```

## 🔄 TODO: OpenFlights Data Setup Process

### Step 1: Download Data Files
```python
# TODO: Run this to download OpenFlights data
from data.openflights import download_openflights_data
download_openflights_data()
```

**What this downloads:**
- `airports.dat` - ~14,000 airports worldwide with coordinates, codes
- `routes.dat` - ~67,000 flight routes between airports  
- `airlines.dat` - ~6,000 airlines with codes and info

### Step 2: Parse and Filter Data
```python  
# TODO: Get US airports and routes
from data.openflights import setup_openflights_data
us_airports_df, us_routes_df = setup_openflights_data()
```

**What this does:**
- Parses CSV files into pandas DataFrames
- Filters to US airports only (~1,500 airports)
- Filters to US domestic routes only (~15,000 routes)
- Validates data integrity

### Step 3: Use in Graph Construction
```python
# TODO: Build flight network from OpenFlights data
from models.graph import FlightNetwork
network = FlightNetwork()
network.load_from_dataframes(us_airports_df, us_routes_df)
```

## 📊 Data Format Details

### Airports Data Columns:
- `Airport ID` - Unique OpenFlights identifier
- `Name` - Airport name
- `City` - Main city served  
- `Country` - Country name
- `IATA` - 3-letter IATA code (LAX, JFK, etc.)
- `ICAO` - 4-letter ICAO code
- `Latitude` - Decimal degrees
- `Longitude` - Decimal degrees
- `Altitude` - Feet above sea level
- `Timezone` - Hours offset from UTC

### Routes Data Columns:
- `Airline` - 2-letter airline code
- `Source airport` - Source airport IATA/ICAO
- `Destination airport` - Destination airport IATA/ICAO  
- `Stops` - Number of stops (0 = direct flight)
- `Equipment` - Aircraft types used

## 🎯 Implementation Priority:

1. **First**: Implement `download_openflights_data()` function
2. **Second**: Implement `parse_airports_data()` function  
3. **Third**: Implement `get_us_airports_from_openflights()` function
4. **Fourth**: Implement `parse_routes_data()` function
5. **Fifth**: Implement `get_us_routes_from_openflights()` function
6. **Last**: Implement `setup_openflights_data()` wrapper function

## 🔗 Data Sources:
- **Airports**: https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat
- **Routes**: https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat  
- **Airlines**: https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat

## ✅ Success Criteria:
- [ ] Download all 3 data files successfully
- [ ] Parse airports.dat into clean DataFrame
- [ ] Filter to ~1,500 US airports
- [ ] Parse routes.dat into clean DataFrame  
- [ ] Filter to US domestic routes
- [ ] Ready to build FlightNetwork graph!
