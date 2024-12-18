# Main queries for Dashboard
import influxdb_client_3
from influxdb_client_3 import InfluxDBClient3, Point
from influxdb_client_3 import flight_client_options
import certifi
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


fh = open(certifi.where(), "r")
cert = fh.read()
#fh.close()

#-------- QUERIES --------

query_Lab_1_Spy_1 = """
SELECT *
FROM "Lab_1_Spy_1"
WHERE
time >= now() - interval '1 day'
"""
query_Lab_2_Spy_1 = """
SELECT *
FROM "Lab_2_Spy_1"
WHERE
time >= now() - interval '1 day'
"""
query_Tent_1_Spy_1 = """
SELECT *
FROM "Tent_1_Spy_1"
WHERE
time >= now() - interval '1 day'
"""

query_Tent_2_Spy_1 = """
SELECT *
FROM "Tent_2_Spy_1"
WHERE
time >= now() - interval '1 day'
"""

query_Tent_3_Spy_1 = """
SELECT *
FROM "Tent_3_Spy_1"
WHERE
time >= now() - interval '1 day'
"""

query_Tent_4_Spy_1 = """
SELECT *
FROM "MycoBrain_12"
WHERE
time >= now() - interval '1 day'
"""

query_Sto_1_Spy_1 = """
SELECT *
FROM "Sto_1_Spy_1"
WHERE
time >= now() - interval '1 day'
"""

# query_Mini_Tent_1_Spy_1 = """
# SELECT *
# FROM "Mini_Tent_1_Spy_1"
# WHERE
# time >= now() - interval '24 hour' AND time <= now()
# AND
# ("SCD30_CO2" IS NOT NULL OR "SCD30_Humidity" IS NOT NULL OR "SCD30_Temperature" IS NOT NULL)
# """

# query_Mini_Tent_2_Spy_1 = """
# SELECT *
# FROM "Mini_Tent_2_Spy_1"
# WHERE
# time >= now() - interval '24 hour' AND time <= now()
# AND
# ("SCD30_CO2" IS NOT NULL OR "SCD30_Humidity" IS NOT NULL OR "SCD30_Temperature" IS NOT NULL)
# """
#-------- INFLUXDB CONNECTIONS --------

client_Mycodash = InfluxDBClient3(
    token="8w-iWRvCbi7o_G83uZ2QteMHbE677ioKImXetJv5ActAKttDzb2jolr7AaQO_zpzWcOIxSEpoReQS8tmH_ncpw==",  #Read buckets Infra_Fungarium
    host="https://eu-central-1-1.aws.cloud2.influxdata.com",
    org="c46a66937900cfee",
    database="Infra_Fungarium",
    flight_client_options=flight_client_options(
        tls_root_certs=cert))

def main_plotter(query, sensors, name):
    # Fetch data
    info = client_Mycodash.query(query=query, language="sql")
    df = info.to_pandas()

    # Format time to Day_Month_Year format
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Determine the number of rows needed based on the number of sensors
    num_sensors = len(sensors)
    fig = make_subplots(rows=num_sensors, cols=1, shared_xaxes=True, vertical_spacing=0.05)

    # Iterate over sensors and add traces dynamically
    for i, (sensor, measurement) in enumerate(sensors, start=1):
        col_name = f"{sensor}_{measurement}"
        if col_name in df.columns:  # Check if the column exists
            # Add the main trace
            fig.add_trace(
                go.Scatter(x=df['time'], y=df[col_name], mode='lines', name=f'{sensor} - {measurement}'),
                row=i, col=1
            )
            # Add the rolling average trace
            fig.add_trace(
                go.Scatter(
                    x=df['time'],
                    y=df[col_name].rolling(window=25).mean(),
                    mode='lines',
                    name=f'{sensor} - Avg. {measurement}'
                ),
                row=i, col=1
            )
            # Update y-axis label
            fig.update_yaxes(title_text=f"{measurement}", showgrid=True, row=i, col=1)
        else:
            print(f"Warning: Column {col_name} not found in the data.")

    # Update layout
    fig.update_layout(
        title_text=name,
        height=300 * num_sensors,  # Adjust height dynamically based on the number of rows
        showlegend=False,#remove legend
    )
    return fig


import logging

def indicator(query, sensors, name):
    # Query data
    info = client_Mycodash.query(query=query, language="sql")
    df = info.to_pandas()

    # Check if the DataFrame is empty
    if df.empty:
        logging.warning(f"No data available for the query: {name}")
        # Return an empty figure with a placeholder message
        fig = go.Figure()
        fig.update_layout(
            title_text=f"{name} - No Data Available",
            annotations=[{
                "text": "No data available for the selected sensors.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 20}
            }]
        )
        return fig

    # Initialize the figure
    fig = go.Figure()

    # Loop over sensors and measurements
    for i, (sensor, measurement) in enumerate(sensors, start=0):
        col_name = f"{sensor}_{measurement}"
        if col_name not in df.columns:
            logging.warning(f"Column {col_name} not found in the data for {name}.")
            continue

        try:
            # Retrieve the latest value for the indicator
            value = df[col_name].iloc[-1]
            time_label = str(df['time'].iloc[-1])
        except (IndexError, KeyError):
            # Handle missing data
            value = np.nan
            time_label = "No data available"

        # Add the indicator trace
        fig.add_trace(go.Indicator(
            mode="number",
            value=value,
            title={"text": f"{sensor} {measurement}"},
            number={"font": {"size": 50}},
            domain={'row': i, 'column': 0}
        ))

    # Update layout
    fig.update_layout(
        title_text=f'{name}',
        grid={'rows': len(sensors), 'columns': 1, 'pattern': "independent"},
        height=300 * len(sensors)  # Adjust height dynamically
    )

    return fig
