import streamlit as st

# 設定網頁config
st.set_page_config(page_title="Air Quality Monitoring", page_icon="☁️", layout="wide")
# 設定網頁標題
st.title("Air Quality Monitoring")

# 使用 st.markdown 設定標籤的字體大小
st.markdown("<style> .stTab > button { font-size: 24px; } </style>", unsafe_allow_html=True)

st.sidebar.success('Please choose an Question above')