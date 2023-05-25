import streamlit as st

# 設定網頁標題
st.title("Air Quality Monitoring")

# 使用 st.markdown 設定標籤的字體大小
st.markdown("<style> .stTab > button { font-size: 24px; } </style>", unsafe_allow_html=True)


with st.container():
    tabs = st.tabs(["chat1", "chat2", "chat3"])
    
    if tabs[0]:
        with st.sidebar:
            st.write("Sidebar for Tab 1")
        
        st.write("Content of Tab 1")
        
    elif tabs[1]:
        with st.sidebar:
            st.write("Sidebar for Tab 2")
        
        st.write("Content of Tab 2")
        
    elif tabs[2]:
        with st.sidebar:
            st.write("Sidebar for Tab 3")
        
        st.write("Content of Tab 3")