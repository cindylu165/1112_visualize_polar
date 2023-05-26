# Import dependencies
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import plotly.graph_objects as go

# 設定網頁config
st.set_page_config(page_title="Air Quality Monitoring", page_icon="⛅", layout="wide")
# 設定網頁標題
st.title("Effect of relative humidity on PM2.5 and PM10")

st.sidebar.title('parameter setting')

Location = ['北部空品區','中部空品區','南部空品區','東部空品區']
selected_area = st.sidebar.selectbox('Please choose an Area', Location)
central = ['大城','埔里','竹山','南投','二林','線西','彰化','西屯','忠明','大里','沙鹿','豐原']
north = ['富貴角','永和','中壢','三重','陽明','龍潭','平鎮','觀音','大園','桃園','大同','松山','古亭','萬華','中山','士林','淡水','林口','菜寮','新莊','板橋','土城','新店','萬里','汐止','基隆']
sorth = ['復興','恆春','潮州','屏東','小港','前鎮','前金','左營','楠梓','林園','大寮','鳳山','仁武','橋頭','美濃']
east = ['關山','冬山','宜蘭','花蓮','臺東']

if selected_area == '北部空品區':
    location = st.sidebar.selectbox('Please choose a location', north)
elif selected_area == '中部空品區':
    location = st.sidebar.selectbox('Please choose a location', central)
elif selected_area == '南部空品區':
    location = st.sidebar.selectbox('Please choose a location', sorth)
elif selected_area == '東部空品區':
    location = st.sidebar.selectbox('Please choose a location', east)

st.write('**Location** : ', selected_area, "-",location)
_df = pd.read_csv("./data.csv")
st.dataframe(_df, use_container_width = True)