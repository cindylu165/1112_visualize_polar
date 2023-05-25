import streamlit as st

# 使用 st.markdown 設定標籤的字體大小
st.markdown("<style> .stTab > button { font-size: 24px; } </style>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])
