# Flight Path Optimizer - Project Structure

## Project Organization

```
flight-pathfinder/
├── README.md                    # Project documentation
├── LICENSE                      # MIT License
├── PROJECT_STRUCTURE.md         # This file
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore patterns
├── opensky_us_flights.py       # Legacy OpenSky script
├── flight_pathfinder.py        # Main application entry point
│
├── algorithms/                  # Pathfinding algorithms
│   ├── __init__.py             
│   ├── dijkstra.py             # Dijkstra's algorithm implementation
│   ├── a_star.py               # A* algorithm implementation
│   └── benchmark.py            # Algorithm comparison utilities
│
├── benchmarks/                  # Performance benchmarking
│   ├── run_benchmark.py        # Benchmark runner script
│   ├── results_*.txt           # Text benchmark results
│   ├── results_*.json          # JSON benchmark results
│   └── results_*.csv           # CSV benchmark results
│
├── data/                        # Data loading and processing
│   ├── __init__.py             
│   ├── airport_loader.py       # Airport data loading utilities
│   ├── route_loader.py         # Route data loading and distance calculations
│   └── openflights/            # OpenFlights data integration
│       ├── __init__.py         
│       ├── downloader.py       # Download and parse OpenFlights data
│       ├── README.md           # OpenFlights documentation
│       ├── airports.dat        # Downloaded airport data
│       ├── routes.dat          # Downloaded route data
│       └── airlines.dat        # Downloaded airline data
│
├── examples/                    # Example scripts and demonstrations
│   ├── load_openflights_example.py  # Load real US flight data
│   ├── visualize_real_data.py       # Visualize with real data (4 demos)
│   └── visualize_test_paths.py      # Visualize with test data (3 demos)
│
├── models/                      # Data structures and models
│   ├── __init__.py             
│   └── graph.py                # FlightNetwork, Airport, Route classes
│
├── src/                         # Additional source code
│   └── opensky_fetch.py        # OpenSky Network API integration
│
├── tests/                       # Test suites (48 tests)
│   ├── __init__.py             
│   ├── test_dijkstra.py        # Dijkstra algorithm tests (12 tests)
│   ├── test_a_star.py          # A* algorithm tests (13 tests)
│   ├── test_graph.py           # Graph structure tests (12 tests)
│   ├── test_opensky_fetch.py   # OpenSky API tests (5 tests)
│   └── test_visualization.py   # Visualization tests (6 tests)
│
├── utils/                       # Utilities
│   ├── __init__.py             
│   └── logging_utils.py        # Logging configuration
│
└── visualization/               # Visualization modules
    ├── __init__.py             
    ├── plot_aircraft.py        # Aircraft position plotting
    └── path_plotter.py         # Flight path visualization (Plotly)
```

```

## Implementation Status

### COMPLETED

**Phase 1: Data Foundation**
- Airport data loading from OpenFlights dataset
- Route data processing with distance calculations
- US airports filtering (1055 airports, 5353 routes)
- Haversine distance formula implementation

**Phase 2: Graph Infrastructure**
- FlightNetwork class with adjacency list representation
- Airport and Route dataclasses
- DataFrame loading support
- Network statistics and validation

**Phase 3: Core Algorithms**
- Dijkstra's algorithm with performance tracking
- A* algorithm with multiple heuristics (Euclidean, Haversine, Manhattan)
- K-shortest paths implementation
- Memory profiling with tracemalloc

**Phase 4: Benchmarking & Analysis**
- Comprehensive benchmark suite (8 test cases)
- Performance comparison (Dijkstra vs A*)
- Export to TXT, JSON, CSV formats
- Space and time complexity tracking

**Phase 5: Visualization & Testing**
- Interactive Plotly visualizations (3 functions)
- US Albers projection mapping
- 48 unit tests (100% passing)
- Test data and real data demos

## Key Statistics

- **Airports**: 1055 US airports loaded
- **Routes**: 5353 direct flight routes
- **Test Coverage**: 48 unit tests passing
- **Algorithms**: Dijkstra and A* fully implemented
- **Visualizations**: 3 interactive map types
- **Benchmarks**: 8 test cases, 3 export formats

## Algorithm Performance (Real Data)

Based on benchmark results with US flight network:

| Metric | Dijkstra | A* | A* Advantage |
|--------|----------|-----|--------------|
| Nodes Expanded | 156 avg | 3.7 avg | 53x fewer |
| Execution Time | 3.3ms avg | 1.1ms avg | 3x faster |
| Memory Usage | 62 KB avg | 16 KB avg | 4.6x less |
| Path Quality | Optimal | Optimal | Equal |

## Getting Started

### Installation
```bash
git clone https://github.com/prentang/flight-pathfinder.git
cd flight-pathfinder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Quick Examples

**1. Load Real Flight Data**
```bash
python examples/load_openflights_example.py
```

**2. Run Visualizations**
```bash
python examples/visualize_test_paths.py    # Test data (3 visualizations)
python examples/visualize_real_data.py     # Real data (4 visualizations)
```

**3. Run Benchmarks**
```bash
python benchmarks/run_benchmark.py
```

**4. Run Tests**
```bash
python -m unittest discover tests -v
```

## Dependencies

Core requirements (from requirements.txt):
```
pandas>=1.5.0          # Data processing
numpy>=1.21.0          # Numerical operations
plotly>=5.11.0         # Interactive visualizations
networkx>=2.8.0        # Graph utilities
requests>=2.28.0       # API integration
pytest>=7.0.0          # Testing framework
```

## Data Sources

- **OpenFlights**: Airport and route data (https://openflights.org/data.html)
- **OpenSky Network**: Live flight tracking API (https://openskynetwork.github.io/)

## License

This project is licensed under the MIT License - see LICENSE file for details.
