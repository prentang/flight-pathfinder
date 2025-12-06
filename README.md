# Flight Path Optimizer

Find the fastest flight path between any two US airports using Dijkstra's and A* algorithms.

## Quick Start

```bash
# Setup (first time only)
git clone https://github.com/prentang/flight-pathfinder.git
cd flight-pathfinder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Find fastest path
python find_path.py LAX JFK

# Visualize route on map
python visualize.py LAX JFK

# Compare algorithms
python compare.py LAX JFK
```

## Usage

### Find Path
```bash
python find_path.py LAX JFK                    # Find fastest route
python find_path.py LAX JFK --visualize        # + show map
python find_path.py --list-airports            # List all airports
python find_path.py --airport-info LAX         # Airport details
```

### Visualize
```bash
python visualize.py LAX JFK                    # Quick visualization
```

### Compare
```bash
python compare.py LAX JFK                      # Dijkstra vs A*
```

## Features

- **1055 US airports** from OpenFlights database
- **5353 flight routes** with real distances
- **A* algorithm** - 53x more efficient than Dijkstra
- **Interactive maps** with Plotly
- **Memory profiling** and performance tracking
- **Comprehensive benchmarks** with TXT/JSON/CSV export

## Popular Airport Codes

| West Coast | East Coast | Central |
|------------|------------|---------|
| LAX - Los Angeles | JFK - New York | ORD - Chicago |
| SFO - San Francisco | BOS - Boston | DFW - Dallas |
| SEA - Seattle | MIA - Miami | ATL - Atlanta |
| PDX - Portland | PHL - Philadelphia | DEN - Denver |
| SAN - San Diego | DCA - Washington DC | MSP - Minneapolis |

## Example Output

```
======================================================================
FASTEST PATH FOUND
======================================================================
From: LAX - Los Angeles International Airport (Los Angeles)
To:   JFK - John F Kennedy International Airport (New York)

Route: LAX -> JFK
Total Distance: 3974 km
Number of Stops: 1

Algorithm: A*
Nodes Explored: 5
Execution Time: 2.21 ms
Memory Used: 37.73 KB
======================================================================
```

## Algorithm Comparison

| Metric | Dijkstra | A* | Advantage |
|--------|----------|-----|-----------|
| Nodes Explored | 156 avg | 3 avg | **53x fewer** |
| Speed | 3.3ms | 1.1ms | **3x faster** |
| Memory | 62 KB | 16 KB | **4.6x less** |
| Path Quality | Optimal | Optimal | Equal |

A* uses geographic heuristics to explore toward the goal, making it much more efficient than Dijkstra's uniform exploration.

## Advanced Usage

### Benchmarks
```bash
python benchmarks/run_benchmark.py             # Run 8 test cases
# Generates results_TIMESTAMP.txt/json/csv
```

### Examples
```bash
python examples/visualize_test_paths.py        # Test data demos
python examples/visualize_real_data.py         # Real data demos
python examples/load_openflights_example.py    # Data loading
```

### Tests
```bash
python -m unittest discover tests -v           # Run all 48 tests
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Detailed examples and commands
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Code organization
- **[LICENSE](LICENSE)** - MIT License

## Tech Stack

- **Python 3.10+** with pandas, numpy, plotly
- **Algorithms**: Custom Dijkstra and A* implementations
- **Data**: OpenFlights database (7698 airports, 67652 routes globally)
- **Visualization**: Interactive Plotly maps with US Albers projection

## How It Works

1. **Graph Model**: Airports are nodes, routes are weighted edges
2. **Data Loading**: Automatically downloads OpenFlights data
3. **Pathfinding**: A* uses Haversine distance heuristic to find optimal paths
4. **Visualization**: Plotly generates interactive maps with zoom/pan/hover

## Project Structure

```
flight-pathfinder/
├── find_path.py         # Main CLI tool
├── visualize.py         # Quick visualization
├── compare.py           # Algorithm comparison
├── algorithms/          # Dijkstra & A* implementations
├── data/                # Data loaders & OpenFlights integration
├── models/              # Graph data structures
├── visualization/       # Plotly functions
├── tests/               # 48 unit tests
└── benchmarks/          # Performance analysis
```

## Contributors

- **Prentice Tang** - [@prentang](https://github.com/prentang)
- **Kenneth Chen** - [@KennethC12](https://github.com/KennethC12)

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Quick Links**: [Examples](QUICKSTART.md) | [Structure](PROJECT_STRUCTURE.md) | [Tests](tests/) | [Benchmarks](benchmarks/)
