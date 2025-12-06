# Flight Path Optimizer - Dijkstra & A* Algorithm

## Overview
This project models the U.S. air travel network as a **graph**, where:
- **Airports** are nodes
- **Routes** are edges
- **Weights** represent flight distance or time

We apply **Dijkstra's** and **A*** algorithms to find the **shortest or fastest flight path** between two airports using **real-world datasets** from [OpenFlights](https://openflights.org/data.html) and [OpenSky Network](https://openskynetwork.github.io/opensky-api/).

The goal is to:
- Compute efficient flight paths between any two airports  
- Compare the performance of Dijkstra vs A*  
- Visualize the results using **Plotly** interactive maps
- Track space and time complexity with real benchmarks

---

## Features
- Graph-based modeling of 1055 US airports and 5353 routes
- Dijkstra's and A* algorithms implemented with performance tracking
- Real dataset integration from OpenFlights (CSV) and OpenSky (REST API)
- Memory profiling and execution time tracking
- Interactive Plotly visualizations with US Albers projection
- Comprehensive benchmark suite with TXT/JSON/CSV export
- 48 unit tests with 100% pass rate

---

## Tech Stack
| Category | Tools / Libraries |
|-----------|------------------|
| Language | Python 3.10+ |
| Graphs & Algorithms | Custom implementation + NetworkX |
| Data Processing | pandas, NumPy |
| Visualization | Plotly |
| Performance Tracking | tracemalloc |
| Data Sources | OpenFlights CSV, OpenSky REST API |
| Version Control | Git + GitHub |

---

## Setup Instructions

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
- pandas - Data processing
- numpy - Numerical operations
- plotly - Interactive visualizations
- networkx - Graph utilities
- requests - API integration
- pytest - Testing framework

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

## Quick Start Examples

### Example 1: Load Real Flight Data
```bash
python examples/load_openflights_example.py
```

Loads 1055 US airports and 5353 routes from OpenFlights dataset.

### Example 2: Run Interactive Visualizations

**With Test Data (Fast)**
```bash
python examples/visualize_test_paths.py
```

Opens 3 interactive Plotly maps:
1. Single Path Visualization (LAX to JFK)
2. Multiple Paths Comparison (LAX to BOS - 3 routes)
3. Full Network Graph (12 airports, SEA to MIA highlighted)

**With Real Data (Comprehensive)**
```bash
python examples/visualize_real_data.py
```

Opens 4 interactive Plotly maps with real US flight network:
1. Cross-country flight (LAX to JFK)
2. Algorithm comparison (LAX to MIA - Dijkstra vs A*)
3. Regional network (California airports)
4. Long-distance flight (SEA to MIA)

### Example 3: Run Performance Benchmarks
```bash
python benchmarks/run_benchmark.py
```

Runs 8 test cases and generates:
- `results_TIMESTAMP.txt` - Human-readable results
- `results_TIMESTAMP.json` - Structured data
- `results_TIMESTAMP.csv` - Spreadsheet format

**Benchmark Results Summary:**
- A* expands 53x fewer nodes than Dijkstra
- A* is 3x faster in execution time
- A* uses 4.6x less memory
- Both algorithms find optimal paths

---

## Visualization Features

Interactive Plotly maps include:
- **Zoom and pan** - Navigate the map freely
- **Hover details** - See airport information on hover
- **Geographic accuracy** - US Albers projection
- **Color-coded paths** - Different colors for algorithm comparison
- **Connectivity sizing** - Node size based on number of routes
- **Start/end markers** - Star markers for path endpoints

---

## Project Structure

```
flight-pathfinder/
├── algorithms/          # Dijkstra & A* implementations
│   ├── dijkstra.py     # Dijkstra's algorithm with stats
│   ├── a_star.py       # A* with multiple heuristics
│   └── benchmark.py    # Performance comparison tools
├── benchmarks/          # Benchmark results and runner
│   └── run_benchmark.py
├── data/               # Data loading utilities
│   ├── airport_loader.py
│   ├── route_loader.py
│   └── openflights/    # OpenFlights data integration
├── examples/           # Demo scripts
│   ├── load_openflights_example.py
│   ├── visualize_real_data.py
│   └── visualize_test_paths.py
├── models/             # Graph data structures
│   └── graph.py        # FlightNetwork, Airport, Route
├── tests/              # Unit tests (48 tests)
├── visualization/      # Plotly visualization functions
│   └── path_plotter.py
└── requirements.txt    # Python dependencies
```

---

## Algorithm Comparison

### Dijkstra's Algorithm
- **Guarantee**: Always finds optimal path
- **Strategy**: Explores all directions equally
- **Use case**: When heuristic unavailable or graph is small
- **Performance**: Slower but thorough

### A* Algorithm  
- **Guarantee**: Finds optimal path (with admissible heuristic)
- **Strategy**: Explores towards goal using geographic heuristic
- **Use case**: Large graphs with coordinate data
- **Performance**: Much faster, uses less memory

**Real-world Results (8 test cases):**
| Metric | Dijkstra Avg | A* Avg | Improvement |
|--------|--------------|--------|-------------|
| Nodes Expanded | 156 | 3.7 | 53x fewer |
| Execution Time | 3.3ms | 1.1ms | 3x faster |
| Peak Memory | 62 KB | 16 KB | 4.6x less |

---

## Code Example

```python
from models.graph import FlightNetwork, Airport, Route
from algorithms.dijkstra import DijkstraPathFinder
from algorithms.a_star import AStarPathFinder
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

# Find shortest path with Dijkstra
dijkstra_finder = DijkstraPathFinder(network)
path, distance = dijkstra_finder.find_shortest_path("LAX", "JFK")
stats = dijkstra_finder.get_algorithm_stats()

print(f"Path: {' → '.join(path)}")
print(f"Distance: {distance:.0f} km")
print(f"Nodes expanded: {stats['nodes_expanded']}")
print(f"Execution time: {stats['execution_time']:.4f}s")
print(f"Memory used: {stats['peak_memory_bytes'] / 1024:.2f} KB")

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

Total: 48 tests, 100% passing

---

## Dependencies

All dependencies are managed via `requirements.txt`:

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | >=1.5.0 | Data processing |
| numpy | >=1.21.0 | Numerical operations |
| plotly | >=5.11.0 | Interactive visualizations |
| networkx | >=2.8.0 | Graph utilities |
| requests | >=2.28.0 | API requests |
| pytest | >=7.0.0 | Testing framework |

---

## Data Sources

- **OpenFlights**: Comprehensive airport and route database
  - URL: https://openflights.org/data.html
  - Data: 7698 airports, 67652 routes globally
  - US subset: 1055 airports, 5353 routes
  
- **OpenSky Network**: Live flight tracking API
  - URL: https://openskynetwork.github.io/opensky-api/
  - Data: Real-time aircraft positions
  - Coverage: Global flight tracking

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contributors

- Prentice Tang ([@prentang](https://github.com/prentang))

---

## Acknowledgments

- OpenFlights for comprehensive airport and route data
- OpenSky Network for real-time flight tracking API
- Plotly for interactive visualization capabilities
