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

# Visualize algorithm search patterns
python simulate_search.py LAX JFK

# Find alternative routes with layovers
python find_alternatives.py ABE JFK
python find_alternatives.py LAX JFK --visualize --compare
```

## Usage

### Find Path
```bash
python find_path.py LAX JFK                    # Find fastest route
python find_path.py LAX JFK --visualize        # + show map
python find_path.py --list-airports            # List all airports
python find_path.py --airport-info LAX         # Airport details
```

Shows layover information clearly:
- Direct flights: "DIRECT FLIGHT (no layovers)"
- One layover: "1 LAYOVER at ORD"
- Multiple layovers: "2 LAYOVERS at ORD, DEN"

### Find Alternatives
```bash
python find_alternatives.py ABE JFK            # Multiple route options
python find_alternatives.py LAX JFK --visualize # + show map
python find_alternatives.py LAX JFK --compare  # + algorithm stats
python find_alternatives.py LAX JFK -v -c     # Both options
```

Finds alternative routes with different layover patterns. Great for:
- Comparing direct vs connecting flights
- Finding backup options
- Seeing all possible routes
- Visualizing multiple routes on a map (--visualize) - opens in browser
- Comparing A* vs Dijkstra performance (--compare)

### Visualize
```bash
python visualize.py LAX JFK                    # Quick visualization
```

Interactive map opens automatically in your default browser.

### Compare
```bash
python compare.py LAX JFK                      # Dijkstra vs A*
```

### Simulate Search
```bash
python simulate_search.py LAX JFK              # See how algorithms explore
```

Shows side-by-side visualization of which airports each algorithm explores before finding the path.

## Features

- **1055 US airports** from OpenFlights database
- **5353 flight routes** with real distances
- **A* algorithm** - 53x more efficient than Dijkstra
- **Interactive maps** with Plotly
- **Memory profiling** and performance tracking
- **Comprehensive benchmarks** with TXT/JSON/CSV export
- **Layover tracking** - Clear display of connecting flights
- **Alternative routes** - Find multiple path options

## Popular Airport Codes

| West Coast | East Coast | Central |
|------------|------------|---------|
| LAX - Los Angeles | JFK - New York | ORD - Chicago |
| SFO - San Francisco | BOS - Boston | DFW - Dallas |
| SEA - Seattle | MIA - Miami | ATL - Atlanta |
| PDX - Portland | PHL - Philadelphia | DEN - Denver |
| SAN - San Diego | DCA - Washington DC | MSP - Minneapolis |

## Example Output

### Direct Flight
```
Route: LAX -> JFK
Total Distance: 3974 km
Flight Type: DIRECT FLIGHT (no layovers)
```

### Flight with Layover
```
Route: ABE -> PHL -> JFK
Total Distance: 239 km
Flight Type: 1 LAYOVER at PHL

Flight Segments:
  Segment 1 (Departure): ABE (Allentown) -> PHL (Philadelphia) - 88 km
    ** LAYOVER at PHL - Philadelphia International Airport **
  Segment 2 (Final Leg): PHL (Philadelphia) -> JFK (New York) - 151 km
```

### Alternative Routes with Algorithm Comparison
```
======================================================================
ALGORITHM PERFORMANCE
======================================================================

Algorithm: A*
Nodes Explored: 5
Execution Time: 2.45 ms
Memory Used: 37.87 KB

Algorithm: Dijkstra
Nodes Explored: 274
Execution Time: 5.98 ms
Memory Used: 74.27 KB

Efficiency Comparison:
A* explored 54.8x fewer nodes than Dijkstra
A* was 2.4x faster than Dijkstra
```

### Original Format
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
| Nodes Explored | ~150-300 | ~2-10 | **20-100x fewer** |
| Speed | ~5-8ms | ~1-3ms | **2-5x faster** |
| Memory | ~60-80 KB | ~20-40 KB | **2-4x less** |
| Path Quality | Optimal | Optimal | Equal |

*Performance metrics vary by route complexity, distance, and system specifications.*

A* uses geographic heuristics to explore toward the goal, making it much more efficient than Dijkstra's uniform exploration.

**Example: LAX to JFK**
- Dijkstra explored 274 airports
- A* explored only 2 airports
- A* was 137x more efficient!

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
├── simulate_search.py   # Algorithm search visualization
├── find_alternatives.py # Find alternative routes with layovers
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
