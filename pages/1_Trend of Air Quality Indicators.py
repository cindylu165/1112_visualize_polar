import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 設定網頁config
st.set_page_config(page_title="Air Quality Monitoring", page_icon="⛅", layout="wide")
# 設定網頁標題
st.title("Which Air Quality Indicators have specific seasonal variations?\nWhat is the general trend of this indicator?\nDoes it improve or deteriorate from year to year?")
st.sidebar.title('Parameter Setting')
# -------------------------------------------------------- Load Data ------------------------------------------------------#
try:
    air_data = pd.read_csv('./rawData/空氣品質監測月值.csv')
    site_data = pd.read_csv('./rawData/監測站基本資料.csv')

# Save and read graph as HTML file (locally)
except:
    air_data = pd.read_csv('../rawData/空氣品質監測月值.csv')
    site_data = pd.read_csv('../rawData/監測站基本資料.csv')

# 實作下來式選單（回傳一個 list）
option_list = list(air_data['"itemengname"'].unique())
selected_option = st.sidebar.selectbox('Please choose an air indicator', option_list)


def transform(text):
    text = str(text)
    year = text[:4]
    month = text[-2:]
    return year + "-" + month

def process_data(data, site_data):
    new_col_names = {'"siteid"':'siteid', '"sitename"':'sitename', '"itemid"':'itemid', '"itemname"':'itemname', 
                '"itemengname"':'itemengname', '"itemunit"':'itemunit', '"monitormonth"':'monitormonth', '"concentration"':'concentration'}
    data = data.rename(columns=new_col_names)
    data = data[data['concentration'] != 'x']
    data[['concentration']] = data[['concentration']].astype(float)
    data[['monitormonth']] = data[['monitormonth']].astype('int')
    data['monitormonth'] = pd.to_datetime(data["monitormonth"].apply(lambda x: transform(x)), format='%Y-%m')
    # 取測站位置資料
    data = data.merge(site_data[['sitename', 'twd97lon', 'twd97lat']], on='sitename')
    data['month'] = data['monitormonth'].apply(lambda x: x.month)
    return data

def filter_data(data, option):
    
    for i in option:
        data = data[data['itemengname'] == i]
    return data

if (selected_option):
    a_data = process_data(air_data, site_data)
    
    # 過濾
    # a_data = filter_data(a_data, selected_option)
    a_data = a_data[a_data['itemengname'] == selected_option]


    # df = px.data.tips()
    fig1 = px.strip(a_data, x="concentration", y="month", color='itemengname', title=f'{selected_option} Monthly Concentration Distribution',
                    labels=dict(itemengname='Measurement Item', concentration='Concentration (ppb)', month='Month'))
    st.plotly_chart(fig1)

    df_mean = a_data.groupby(['monitormonth', 'itemname'])['concentration'].mean()
    df_mean = pd.DataFrame(df_mean).reset_index()
    # df_CO = df_mean[df_mean['itemname'] == "細懸浮微粒"]
    fig2 = px.line(df_mean, x='monitormonth', y='concentration', title=f'{selected_option} Time Series Change',
                   labels=dict(concentration='Concentration (ppb)', monitormonth='Monitor Time'))

    fig2.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    st.plotly_chart(fig2)



