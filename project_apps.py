import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import plotly.graph_objects as go
import numpy as np

_df = pd.read_csv("./data.csv")
_df = _df.replace('x', np.nan)
_df = _df.dropna()

# 設定網頁config
st.set_page_config(page_title="Air Quality Monitoring", page_icon="☁️", layout="wide")
# 設定網頁標題
st.title("Air Quality Monitoring")

# 使用 st.markdown 設定標籤的字體大小
st.markdown("<style> .stTab > button { font-size: 24px; } </style>", unsafe_allow_html=True)

st.sidebar.success('Please choose an Question above')

st.markdown(
    """ ### Introduction 
    - Currently, air pollution has become an urgent environmental issue that needs to be addressed.The haze caused by ozone, sulfur dioxide, and other PM2.5 pollutants can lead to other environmental problems. Acid rain is one of the major issues caused by industrial areas, and almost the entire Taiwan is now affected by acid rain. Therefore, we have decided to analyze the current trends of air pollution and acid rain, hoping to encourage everyone to take concrete actions to protect the environment.  
    """, unsafe_allow_html=True)
_df = _df[['sitename','itemname','itemengname','itemunit','monitormonth','concentration']]
st.dataframe(_df, width="100%")



st.markdown(
    f""" ### Dataset
    - The dataset is from [Air Quality Monitoring Network](https://data.epa.gov.tw/dataset/detail/AQX_P_08 )
    - The dataset contains {_df.shape[1]} columns and {_df.shape[0]} rows
    """, unsafe_allow_html=True)

