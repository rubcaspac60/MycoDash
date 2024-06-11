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
time >= now() - interval '24 hour' AND time <= now()
AND
("SCD41_CO2" IS NOT NULL OR "SCD41_Humidity" IS NOT NULL OR "SCD41_Temperature" IS NOT NULL)
"""
query_Lab_2_Spy_1 = """
SELECT *
FROM "Lab_2_Spy_1"
WHERE
time >= now() - interval '24 hour' AND time <= now()
AND
("SCD41_CO2" IS NOT NULL OR "SCD41_Humidity" IS NOT NULL OR "SCD41_Temperature" IS NOT NULL)
"""
query_Tent_1_Spy_1 = """
SELECT *
FROM "Tent_1_Spy_1"
WHERE
time >= now() - interval '24 hour' AND time <= now()
AND
("SCD30_Temperature" IS NOT NULL OR "SCD30_Humidity" IS NOT NULL OR "SCD30_CO2" IS NOT NULL)
"""

query_Tent_2_Spy_1 = """
SELECT *
FROM "Tent_2_Spy_1"
WHERE
time >= now() - interval '24 hour' AND time <= now()
AND
("SCD30_Temperature" IS NOT NULL OR "SCD30_Humidity" IS NOT NULL OR "SCD30_CO2" IS NOT NULL)
"""

query_Tent_3_Spy_1 = """
SELECT *
FROM "Tent_3_Spy_1"
WHERE
time >= now() - interval '24 hour' AND time <= now()
AND
("SCD41_Temperature" IS NOT NULL OR "SCD41_Humidity" IS NOT NULL OR "SCD41_CO2" IS NOT NULL)
"""

query_Tent_4_Spy_1 = """
SELECT *
FROM "Tent_4_Spy_1"
WHERE
time >= now() - interval '24 hour' AND time <= now()
AND
("SCD30_CO2" IS NOT NULL OR "SCD30_Humidity" IS NOT NULL OR "SCD30_Temperature" IS NOT NULL)
"""

#-------- INFLUXDB CONNECTIONS --------

client_Mycodash = InfluxDBClient3(
    token="8w-iWRvCbi7o_G83uZ2QteMHbE677ioKImXetJv5ActAKttDzb2jolr7AaQO_zpzWcOIxSEpoReQS8tmH_ncpw==",  #Read buckets Infra_Fungarium
    host="https://eu-central-1-1.aws.cloud2.influxdata.com",
    org="c46a66937900cfee",
    database="Infra_Fungarium",
    flight_client_options=flight_client_options(
        tls_root_certs=cert))


def main_plotter(query, name, model):
    info = client_Mycodash.query(
        query=query,
        language="sql")
    df = info.to_pandas()
    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05)
    
    fig.add_trace(go.Scatter(x=df['time'], y=df[f'{model}_CO2'], mode='lines', name='CO2'),row=1, col=1)
    fig.add_trace(go.Scatter(x=df['time'], y=df[f'{model}_CO2'].rolling(window=25).mean(), mode='lines', name='Avg.CO2'),row=1, col=1)
    fig.update_yaxes(title_text="CO2 (ppm)", showgrid=True, row=1, col=1)
    fig.add_trace(go.Scatter(x=df['time'], y=df[f'{model}_Temperature'], mode='lines', name='Temperature'),row=2, col=1)
    fig.add_trace(go.Scatter(x=df['time'], y=df[f'{model}_Temperature'].rolling(window=25).mean(), mode='lines', name='Avg.Temp.'),row=2, col=1)
    fig.update_yaxes(title_text="Temperature (C)", showgrid=True, row=2, col=1)
    fig.add_trace(go.Scatter(x=df['time'], y=df[f'{model}_Humidity'], mode='lines', name='Humidity'),row=3, col=1)
    fig.add_trace(go.Scatter(x=df['time'], y=df[f'{model}_Humidity'].rolling(window=25).mean(), mode='lines', name='Avg. Hum.'),row=3, col=1)
    fig.update_yaxes(title_text="Humidity (%)", showgrid=True, row=3, col=1)
    fig.update_layout( title_text=name + '_' + model)
    return fig


def indicator(query, name, model):
    # Query data
    info = client_Mycodash.query(query=query, language="sql")
    df = info.to_pandas()

    # Initialize the figure
    fig = go.Figure()

    try:
        # Retrieve the latest values for the indicators
        co2_value = df[f'{model}_CO2'].iloc[-1]
        temp_value = df[f'{model}_Temperature'].iloc[-1]
        humidity_value = df[f'{model}_Humidity'].iloc[-1]
        time_label = str(df['time'].iloc[-1])
        
    except (IndexError, KeyError):
        # Handle missing data
        co2_value = np.nan
        temp_value = np.nan
        humidity_value = np.nan
        time_label = "No data available"

    # Add CO2 Indicator
    fig.add_trace(go.Indicator(
        mode="number",
        value=co2_value,
        title="CO2",
        number={"font": {"size": 50}},
        domain={'row': 0, 'column': 0}))

    # Add Temperature Indicator
    fig.add_trace(go.Indicator(
        mode="number",
        value=temp_value,
        title="Temperature",
        number={"font": {"size": 50}},
        domain={'row': 1, 'column': 0}))

    # Add Humidity Indicator
    fig.add_trace(go.Indicator(
        mode="number",
        value=humidity_value,
        title="Humidity",
        number={"font": {"size": 50}},
        domain={'row': 2, 'column': 0}))

    # Update layout
    fig.update_layout(
        title_text=f'{name}_{model}_{time_label}',
        grid={'rows': 3, 'columns': 1, 'pattern': "independent"},
        template={'data': {'indicator': [{'mode': "number+delta+gauge",
                                          'delta': {'reference': 10},
                                          'gauge': {'shape': "bullet"}}]},
                  'layout': {'width': 300, 'height': 800}}
    )

    return fig
