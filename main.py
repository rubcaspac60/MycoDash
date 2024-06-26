import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import influxdb_client_3
from influxdb_client_3 import InfluxDBClient3, Point
from influxdb_client_3 import flight_client_options
import certifi
from queries import *
from PIL import Image
from streamlit_option_menu import option_menu

#pd.options.display.float_format = '{:,.2f}'.format
#plt.rcParams['figure.figsize'] = [10.0, 10.0]
#plt.rcParams['figure.dpi'] = 300

fh = open(certifi.where(), "r")
cert = fh.read()
#fh.close()
#----------------------------------------------------------------------------------------------------------------------------
#--- INFLUXDB CONNECTIONS ---


#setting up main page
st.set_page_config(page_title="MycoDashboard", page_icon=":bar_chart:", layout="wide")

#----- Header -----
with st.container():
    #st.subheader("Infra_Fungarium Dashboard")
    Logo = Image.open("images/Fungarium_Logo_1.jpg")
    st.image(Logo, use_column_width=True)
    st.title("Atmospheric Conditions")
    st.write("Welcome to the Fungarium MycoDashboard! This dashboard is designed to provide real-time data on the atmospheric conditions within the Fungarium. The Fungarium is a controlled environment for growing mushrooms, and this dashboard will provide data on temperature, humidity, and CO2 levels within the Fungarium.")
    st.write('Raw data can be directly downloaded from this link [InfluxDataNavigator](https://eu-central-1-1.aws.cloud2.influxdata.com/orgs/c46a66937900cfee/data-explorer?fluxScriptEditor)')

#with st.sidebar:
selected = option_menu(
    menu_title = None,
    options = ["Actual Data", "Last 24 hrs"],
    icons = ["📊", "📈"],
    menu_icon = "📊",
    default_index = 0,
    orientation="horizontal"
)


if selected == "Actual Data":
    #---Buildings ---
    with st.container():
        st.write('---')
        Lab_1, Lab_2 = st.columns(2)
        with Lab_1:
            fig_Lab_1 = indicator(query_Lab_1_Spy_1, "Lab_1_Spy_1", "SCD41")
            st.plotly_chart(fig_Lab_1, use_container_width=True)
        with Lab_2:
            #st.write("Graphs")
            fig_Lab_2 =indicator(query_Lab_2_Spy_1, "Lab_2_Spy_1", "SCD30")
            st.plotly_chart(fig_Lab_2,use_container_width=True)
            
            
        #--- Tents ---
        with st.container():
                    st.write('---')
        Tent_1, Tent_2, Tent_3, Tent_4 = st.columns(4)
        with Tent_1:
            fig_Tent_1 = indicator(query_Tent_1_Spy_1, "Tent_1_Spy_1", "SCD30")
            st.plotly_chart(fig_Tent_1,use_container_width=True)
        with Tent_2:
            fig_Tent_2 = indicator(query_Tent_2_Spy_1, "Tent_2_Spy_1", "SCD30")
            st.plotly_chart(fig_Tent_2,use_container_width=True)
        with Tent_3:
            fig_Tent_3 = indicator(query_Test_3_Spy_1, "Test_3_Spy_1", "AM2315C")
            st.plotly_chart(fig_Tent_3,use_container_width=True)
        with Tent_4:
            fig_Tent_4 = indicator(query_Tent_4_Spy_1, "Tent_4_Spy_1", "SCD30")
            st.plotly_chart(fig_Tent_4,use_container_width=True)
    
if selected == "Last 24 hrs":
    #---Buildings ---
    with st.container():
        st.write('---')
        Lab_1, Lab_2 = st.columns(2)
        with Lab_1:
            fig_Lab_1 = main_plotter(query_Lab_1_Spy_1, "Lab_1_Spy_1", "SCD41")
            st.plotly_chart(fig_Lab_1, use_container_width=True)
        with Lab_2:
            #st.write("Graphs")
            fig_Lab_2 = main_plotter(query_Lab_2_Spy_1, "Lab_2_Spy_1", "SCD30")
            st.plotly_chart(fig_Lab_2,use_container_width=True)
            
            
    #--- Tents ---
    with st.container():
        st.write('---')
        Tent_1, Tent_2, Tent_3, Tent_4 = st.columns(4)
        with Tent_1:
            fig_Tent_1 = main_plotter(query_Tent_1_Spy_1, "Tent_1_Spy_1", "SCD30")
            st.plotly_chart(fig_Tent_1,use_container_width=True)
        with Tent_2:
            fig_Tent_2 = main_plotter(query_Tent_2_Spy_1, "Tent_2_Spy_1", "SCD30")
            st.plotly_chart(fig_Tent_2,use_container_width=True)
        with Tent_3:
            fig_Tent_3 = main_plotter_AM2315C(query_Test_3_Spy_1, "Test_3_Spy_1", "AM2315C")
            st.plotly_chart(fig_Tent_3,use_container_width=True)
        with Tent_4:
            fig_Tent_4 = main_plotter(query_Tent_4_Spy_1, "Tent_4_Spy_1", "SCD30")
            st.plotly_chart(fig_Tent_4,use_container_width=True)
            

fh.close()