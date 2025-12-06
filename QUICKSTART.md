# Quick Start Guide

## Simple Usage - 5 Easy Scripts

### 1. Find Fastest Path (CLI)

```bash
# Basic usage - find fastest path
python find_path.py LAX JFK

# With visualization
python find_path.py LAX JFK --visualize

# Use different algorithm
python find_path.py SEA MIA --algorithm dijkstra

# List available airports
python find_path.py --list-airports

# Get airport info
python find_path.py --airport-info LAX
```

**Example Output:**
```
Loading flight network...
Loaded 1055 airports, 5353 routes

Finding fastest path using A* algorithm...

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
Execution Time: 2.15 ms
Memory Used: 37.87 KB
======================================================================
```

---

### 2. Quick Visualization

```bash
# Visualize any route
python visualize.py LAX JFK
python visualize.py SEA MIA
python visualize.py SFO BOS
```

Opens an interactive map in your browser showing the optimal path.

---

### 3. Algorithm Comparison

```bash
# Compare Dijkstra vs A*
python compare.py LAX JFK
python compare.py ORD ATL
```

Shows performance comparison and visualizes both paths side-by-side.

---

### 4. Search Visualization

```bash
# See how algorithms explore the network
python simulate_search.py LAX JFK
python simulate_search.py SEA MIA
```

Creates a side-by-side visualization showing which airports each algorithm explores during the search. This dramatically illustrates why A* is so much more efficient!

**Example Output:**
```
Simulating search from LAX to JFK...

Running Dijkstra's algorithm...
  Path: LAX -> JFK
  Explored 274 airports

Running A* algorithm...
  Path: LAX -> JFK
  Explored 2 airports

Efficiency: A* explored 137.0x fewer nodes
```

---

### 5. Alternative Routes with Layovers

```bash
# Find multiple route options
python find_alternatives.py ABE JFK

# With visualization
python find_alternatives.py LAX JFK --visualize

# With algorithm comparison
python find_alternatives.py LAX JFK --compare

# Both options
python find_alternatives.py LAX JFK -v -c
```

Shows alternative routes with different numbers of layovers. Perfect for comparing direct vs connecting flights!

**Example Output:**
```
ALTERNATIVE ROUTES: ABE to JFK

Option 1: ABE -> PHL -> JFK
  Distance: 239 km
  Type: 1 LAYOVER at PHL (Philadelphia International Airport)
  
Option 2: ABE -> PHL -> DCA -> JFK
  Distance: 622 km
  Type: 2 LAYOVERS at PHL, DCA

SUMMARY:
Total routes found: 3
Direct flights available: No (minimum 1 layovers required)

ALGORITHM PERFORMANCE:

Algorithm: A*
Nodes Explored: 2
Execution Time: 1.23 ms
Memory Used: 20.98 KB

Algorithm: Dijkstra
Nodes Explored: 6
Execution Time: 1.80 ms
Memory Used: 58.99 KB

Efficiency Comparison:
A* explored 3.0x fewer nodes than Dijkstra
A* was 1.5x faster than Dijkstra

Note: Performance metrics vary based on route complexity, 
distance, and your system specifications.
```

---

## Popular Airport Codes

**West Coast:**
- LAX - Los Angeles
- SFO - San Francisco
- SEA - Seattle
- PDX - Portland
- SAN - San Diego

**East Coast:**
- JFK - New York (JFK)
- BOS - Boston
- MIA - Miami
- PHL - Philadelphia
- DCA - Washington DC

**Central:**
- ORD - Chicago
- DFW - Dallas
- DEN - Denver
- ATL - Atlanta
- MSP - Minneapolis

---

## First Time Setup

```bash
# 1. Clone and navigate
git clone https://github.com/prentang/flight-pathfinder.git
cd flight-pathfinder

# 2. Create virtual environment (REQUIRED on macOS)
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run your first search
python find_path.py LAX JFK --visualize
```

---

## All Commands Cheat Sheet

```bash
# Find path (text output)
python find_path.py LAX JFK

# Find path + map
python find_path.py LAX JFK -v

# Just visualize
python visualize.py LAX JFK

# Compare algorithms
python compare.py LAX JFK

# Simulate search exploration
python simulate_search.py LAX JFK

# Find alternative routes
python find_alternatives.py ABE JFK
python find_alternatives.py LAX JFK -v -c

# List airports
python find_path.py -l

# Airport info
python find_path.py -i LAX

# Run tests
python -m unittest discover tests -v

# Run benchmarks
python benchmarks/run_benchmark.py
```

---

## Advanced Examples

Full demonstrations with detailed output:

```bash
# Test data demos (fast)
python examples/visualize_test_paths.py

# Real data demos (comprehensive)
python examples/visualize_real_data.py

# Load data example
python examples/load_openflights_example.py
```

---

## Tips

- **Use A* for speed** - Default algorithm, 53x more efficient
- **Add --visualize** - See your route on an interactive map
- **3-letter codes only** - Use IATA codes (LAX, JFK, etc.)
- **Case insensitive** - `lax` works the same as `LAX`

---

## Troubleshooting

**"Airport not found"**
- Use 3-letter IATA code (not city name)
- Run `python find_path.py --list-airports` to see available airports

**"No module named 'pandas'"**
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

**"No path found"**
- Airports may not be connected in the network
- Try different airports or check network coverage
