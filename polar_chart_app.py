# Import dependencies
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import plotly.graph_objects as go

## read the data
_df = pd.read_csv("./data.csv")

# set the page config is wide mode default
st.set_page_config(layout="wide")
# 設定網頁標題
st.title("空氣品質監測")
st.subheader("相對溼度對PM2.5、PM10的影響")

# set sidebar and selectbox
# two layers selectbox，choose the area firdt then location
Location = ['北部空品區','中部空品區','南部空品區','東部空品區']
selected_area = st.sidebar.selectbox('選一個空品區', Location)
central = ['大城','埔里','竹山','南投','二林','線西','彰化','西屯','忠明','大里','沙鹿','豐原']
north = ['富貴角','永和','中壢','三重','陽明','龍潭','平鎮','觀音','大園','桃園','大同','松山','古亭','萬華','中山','士林','淡水','林口','菜寮','新莊','板橋','土城','新店','萬里','汐止','基隆']
sorth = ['復興','恆春','潮州','屏東','小港','前鎮','前金','左營','楠梓','林園','大寮','鳳山','仁武','橋頭','美濃']
east = ['關山','冬山','宜蘭','花蓮','臺東']

if selected_area == '北部空品區':
    location = st.sidebar.selectbox('選擇地區', north)
elif selected_area == '中部空品區':
    location = st.sidebar.selectbox('選擇地區', central)
elif selected_area == '南部空品區':
    location = st.sidebar.selectbox('選擇地區', sorth)
elif selected_area == '東部空品區':
    location = st.sidebar.selectbox('選擇地區', east)

st.write('**地區** : ', selected_area, "-",location)

### 針對選擇的地區繪製極地圖
# 設定初始化顯示內容（當使用者沒有選擇任何東西時）
if len(location) == 0:
    st.text('請選擇一項開始繪圖！')

# 當使用者選擇至少一項內容時
else:
    # 建立字典，將年月份對應到角度
    month_labels = ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01', '2021-06-01',
                '2021-07-01', '2021-08-01', '2021-09-01', '2021-10-01', '2021-11-01', '2021-12-01',
                '2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01', '2022-05-01', '2022-06-01',
                '2022-07-01', '2022-08-01', '2022-09-01', '2022-10-01', '2022-11-01', '2022-12-01']
    angle_mapping = [(i * 15) % 360 for i in range(len(month_labels))]
    dict_date_angle = dict(zip(month_labels, angle_mapping))
    def transform(text):
        text = str(text)
        year = text[:4]
        month = text[-2:]
        return year + "-" + month
    # 將日期轉換為角度
    def date_to_angle(date):
        date = date.strftime("%Y-%m-%d")
        return dict_date_angle[date]
    _df['monitormonth'] = pd.to_datetime(_df["monitormonth"].apply(lambda x: transform(x)), format='%Y-%m')
    # 日期範圍 : 2021-01 ~ 2022-12
    start_date = pd.to_datetime('2021-01', format='%Y-%m')
    end_date = pd.to_datetime('2022-12', format='%Y-%m')
    filtered_df = _df[(_df['monitormonth'] >= start_date) & (_df['monitormonth'] <= end_date)]
    # 篩選地區
    loc = filtered_df[filtered_df['sitename']==location]
    loc = loc.replace('x', 0)
    loc = loc.fillna(0)
    loc = pd.pivot_table(loc, values='concentration', index=loc['monitormonth'], columns='itemname')
    loc = loc.reset_index()
    df_location = loc[['monitormonth', '細懸浮微粒', '懸浮微粒', '一氧化氮', '相對濕度']]
    df_location['angle'] = df_location.monitormonth.apply(lambda x: date_to_angle(x))



    # 自定義的年月份標籤
    show_date_chart = ['2021/01', '2021/02', '2021/03', '2021/04', '2021/05', '2021/06',
                '2021/07', '2021/08', '2021/09', '2021/10', '2021/11', '2021/12',
                '2022/01', '2022/02', '2022/03', '2022/04', '2022/05', '2022/06',
                '2022/07', '2022/08', '2022/09', '2022/10', '2022/11', '2022/12']

    # 創建 Polar Charts
    fig = go.Figure()

    # 添加數據到圖表，並設定標籤文本
    fig.add_trace(go.Scatterpolar(
        name='相對濕度',
        r=df_location['相對濕度'].tolist(),
        theta=show_date_chart,
        mode='markers',  # 使用 'lines+markers' 顯示線段和點
        marker=dict(
            size=12,
            color=df_location['相對濕度'].tolist(),  # 根據 r 值設定顏色
            colorscale='Blues',  # 設定顏色漸層
            colorbar=dict(
                title='相對濕度',
                len=0.4,
                y=0.30,
                x=1.1,
                tickfont=dict(
                    size=10,
                )
            ),
            cmin=0.9*min(df_location['相對濕度'].tolist()),  # 設定顏色漸層最小值
            cmax=max(df_location['相對濕度'].tolist())  # 設定顏色漸層最大值
        ),
        
        line=dict(
            color='blue',
            width=1
        ),
        text=show_date_chart,  # 設定標籤文本為年月份
        hovertemplate="日期: %{text}<br>percent: %{r} %<br>",  # 定義 hover 顯示的文本格式
    ))
    fig.add_trace(go.Scatterpolar(
        name='細懸浮微粒',
        r=df_location['細懸浮微粒'].tolist(),
        theta=show_date_chart,
        mode='markers',  # 使用 'lines+markers' 顯示線段和點
        marker=dict(
            size=12,
            color=df_location['細懸浮微粒'].tolist(),  # 根據 r 值設定顏色
            colorscale='Reds',  # 設定顏色漸層,
            colorbar=dict(
                title='細懸浮微粒',
                len=0.4,
                y=0.30,
                x=0.9,
                tickfont=dict(
                    size=10,
                )
            ),
            cmin=0.9*min(df_location['細懸浮微粒'].tolist()),  # 設定顏色漸層最小值
            cmax=max(df_location['細懸浮微粒'].tolist())  # 設定顏色漸層最大值
        ),
        line=dict(
            color='blue',
            width=1
        ),
        text=show_date_chart,  # 設定標籤文本為年月份
        hovertemplate="日期: %{text}<br>μg/m3: %{r}<br>",  # 定義 hover 顯示的文本格式
    ))
    fig.add_trace(go.Scatterpolar(
        name='懸浮微粒',
        r=df_location['懸浮微粒'].tolist(),
        theta=show_date_chart,
        mode='markers',  # 使用 'lines+markers' 顯示線段和點
        marker=dict(
            size=12,
            color=df_location['懸浮微粒'].tolist(),  # 根據 r 值設定顏色
            colorscale='Greens',  # 設定顏色漸層
            colorbar=dict(
                title='懸浮微粒',
                len=0.4,
                y=0.30,
                x=1,
                tickfont=dict(
                    size=10,
                )
            ),
            cmin=min(df_location['懸浮微粒'].tolist()),  # 設定顏色漸層最小值
            cmax=0.9*max(df_location['懸浮微粒'].tolist())  # 設定顏色漸層最大值
        ),
        line=dict(
            color='blue',
            width=1
        ),
        text=show_date_chart,  # 設定標籤文本為年月份
        hovertemplate="日期: %{text}<br>μg/m3: %{r}<br>",  # 定義 hover 顯示的文本格式 
    ))

    # 設定角度刻度和標籤，並且顏色填充用藍色根據r值由小到大漸層
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                angle=0,
                tickvals=angle_mapping,
                ticks="outside",
                tickmode='array',
                tickfont=dict(
                    size=10,
                )
            )
        ),
        height=600,
        # showlegend=False
    )

    # # 顯示圖表
    # fig.show()
    st.plotly_chart(fig, use_container_width=True, layout="wide")
    