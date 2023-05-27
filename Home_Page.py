import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import plotly.graph_objects as go
import numpy as np

# 設定網頁config
st.set_page_config(page_title="Air Quality Monitoring", page_icon="⛅", layout="wide")
# 設定網頁標題
st.title("Air Quality Monitoring")

# 使用 st.markdown 設定標籤的字體大小
st.markdown("<style> .stTab > button { font-size: 24px; } </style>", unsafe_allow_html=True)

st.sidebar.success('Please choose an Question above')

st.markdown(
    """ ### Introduction 
    - Currently, air pollution has become an urgent environmental issue that needs to be addressed.The haze caused by ozone, sulfur dioxide, and other PM2.5 pollutants can lead to other environmental problems. Acid rain is one of the major issues caused by industrial areas, and almost the entire Taiwan is now affected by acid rain. Therefore, we have decided to analyze the current trends of air pollution and acid rain, hoping to encourage everyone to take concrete actions to protect the environment.  
    """, unsafe_allow_html=True)



_df = pd.read_csv("./data.csv")
_df = _df.replace('x', np.nan)
_df = _df.dropna()

st.markdown(
    f""" ### Dataset
    - The dataset is from [Air Quality Monitoring Network](https://data.epa.gov.tw/dataset/detail/AQX_P_08 )
    - The dataset contains {_df.shape[1]} columns and {_df.shape[0]} rows
    - The date range of the dataset is from 1982/07 to 2023/04
    - Quality:
        - Missing value Percentage: 1.4%
        - From the government

    """, unsafe_allow_html=True)
_df = _df[['sitename','itemname','itemengname','itemunit','monitormonth','concentration']]
st.dataframe(_df, use_container_width = True)

st.markdown(
    f""" ### Question
    1. Effect of relative humidity on PM2.5 and PM10
    2. Do different regions and temperature conditions contribute to an increase in the concentrations of acid rain precursors (NOx, SO2)?
    3. Question3

    """, unsafe_allow_html=True)