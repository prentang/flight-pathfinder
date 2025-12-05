#  Flight Path Optimizer — Dijkstra & A* Algorithm

## Overview
This project models the U.S. air travel network as a **graph**, where:
- **Airports** are nodes
- **Routes** are edges
- **Weights** represent flight distance or time

We apply **Dijkstra’s** and **A\*** algorithms to find the **shortest or fastest flight path** between two airports using **real-world datasets** from [OpenFlights](https://openflights.org/data.html) and [OpenSky Network](https://openskynetwork.github.io/opensky-api/).

The goal is to:
- Compute efficient flight paths between any two airports  
- Compare the performance of Dijkstra vs A\*  
- Visualize the results using **Plotly** or **NetworkX**

---

## Features
- Graph-based modeling of U.S. airports and routes  
- Dijkstra’s and A\* algorithms implemented from scratch  
- Real dataset integration via CSV/JSON (OpenFlights) or REST API (OpenSky)  
- Configurable parameters: shortest or longest flight, by distance or time  
- Visualization of computed paths on an interactive map  

---

## Tech Stack
| Category | Tools / Libraries |
|-----------|------------------|
| Language | Python 3.10+ |
| Graphs & Algorithms | `NetworkX` |
| Data Processing | `pandas`, `NumPy` |
| Visualization | `Plotly` or `Grafana` |
| Data Sources | OpenFlights CSV/JSON, OpenSky REST API |
| Version Control | Git + GitHub |

---

## Setup/Testing Instructions

### 1. Clone the repository
```bash
git clone https://github.com/prentang/flight-pathfinder.git
cd flight-pathfinder
```

### 2. Set up a virtual environment (REQUIRED)
```bash
python3 -m venv venv
source venv/bin/activate
```

**Important:** This project requires a virtual environment due to macOS externally managed Python. Always activate the virtual environment before running any commands.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

This installs all required packages including:
- `pandas` - Data processing
- `numpy` - Numerical operations
- `plotly` - Interactive visualizations
- `networkx` - Graph algorithms
- `requests` - API integration
- `pytest` - Testing framework

### 4. Run Unit Tests
```bash
python -m unittest discover tests -v
```

**Expected output:** All 48 tests should pass
```
Ran 48 tests in 0.XXXs
OK
```

---

## Interactive Visualizations

### Run the Visualization Demo
```bash
source venv/bin/activate  # Activate virtual environment
python examples/visualize_test_paths.py
```

This will open **3 interactive Plotly maps** in your browser:

1. **Single Path Visualization** (LAX → JFK)
   - Shows optimal route with start/end markers
   - Displays distance and waypoints
   
2. **Multiple Paths Comparison** (LAX → BOS)
   - Compares Dijkstra vs A* algorithms
   - Shows 3 alternative routes with different colors
   - Includes performance statistics
   
3. **Full Network Graph** (SEA → MIA highlighted)
   - Displays all 12 airports and 58 routes
   - Node size indicates airport connectivity
   - Highlighted path shown in red

**Features:**
- Interactive zoom and pan
- Hover for airport details
- US Albers projection for accurate geography
- Color-coded paths and markers

### Deactivate Virtual Environment
When finished:
```bash
deactivate
```

---

## Project Structure

```
flight-pathfinder/
├── algorithms/          # Dijkstra & A* implementations
├── data/               # Data loading utilities
├── examples/           # Demo scripts & visualizations
├── models/             # Graph data structures
├── tests/              # Unit tests (48 tests)
├── visualization/      # Plotly visualization functions
└── requirements.txt    # Python dependencies
```

---

## Quick Start Example

```python
from models.graph import FlightNetwork, Airport, Route
from algorithms.dijkstra import DijkstraPathFinder
from visualization.path_plotter import plot_flight_path

# Create network
network = FlightNetwork()

# Add airports
network.add_airport(Airport("LAX", "Los Angeles Airport", 
                            "Los Angeles", "USA", 33.9425, -118.408))
network.add_airport(Airport("JFK", "JFK Airport", 
                            "New York", "USA", 40.6413, -73.7781))

# Add route
network.add_route(Route("LAX", "JFK", 3944))

# Find shortest path
pathfinder = DijkstraPathFinder(network)
path, distance = pathfinder.find_shortest_path("LAX", "JFK")

# Visualize
plot_flight_path(network, path, title=f"Path ({distance:.0f} km)")
```

---

## Testing

### Run All Tests
```bash
source venv/bin/activate
python -m unittest discover tests -v
```

### Run Specific Test Files
```bash
python -m unittest tests.test_dijkstra -v
python -m unittest tests.test_a_star -v
python -m unittest tests.test_graph -v
python -m unittest tests.test_visualization -v
```

### Test Coverage
- Graph data structures (12 tests)
- Dijkstra's algorithm (12 tests)
- A* algorithm (13 tests)
- Visualization functions (6 tests)
- OpenSky API integration (5 tests)

---

## Dependencies

All dependencies are managed via `requirements.txt`:

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | >=1.5.0 | Data processing |
| numpy | >=1.21.0 | Numerical operations |
| plotly | >=5.11.0 | Interactive visualizations |
| networkx | >=2.8.0 | Graph algorithms |
| requests | >=2.28.0 | API requests |
| pytest | >=7.0.0 | Testing framework |

**Installation:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```
