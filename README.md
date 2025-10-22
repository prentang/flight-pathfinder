# ✈️ Flight Path Optimizer — Dijkstra & A* Algorithm

## 📍 Overview
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

## 🧠 Features
- Graph-based modeling of U.S. airports and routes  
- Dijkstra’s and A\* algorithms implemented from scratch  
- Real dataset integration via CSV/JSON (OpenFlights) or REST API (OpenSky)  
- Configurable parameters: shortest or longest flight, by distance or time  
- Visualization of computed paths on an interactive map  

---

## ⚙️ Tech Stack
| Category | Tools / Libraries |
|-----------|------------------|
| Language | Python 3.10+ |
| Graphs & Algorithms | `NetworkX` |
| Data Processing | `pandas`, `NumPy` |
| Visualization | `Plotly` or `Grafana` |
| Data Sources | OpenFlights CSV/JSON, OpenSky REST API |
| Version Control | Git + GitHub |

---

## 🚀 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/flight-path-optimizer.git
cd flight-path-optimizer
