"""
Plotly-based visualization for aircraft positions over the US.
"""
import plotly.express as px
import pandas as pd

def plot_aircraft_positions(df: pd.DataFrame):
    """
    Plots aircraft positions on a scatter_geo map of the continental US.
    """
    if df.empty:
        print("No aircraft data to plot.")
        return
    fig = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="callsign",
        title="Live Aircraft Over Continental US"
    )
    fig.update_geos(fitbounds="locations", visible=False, projection_type="albers usa")
    fig.show()
