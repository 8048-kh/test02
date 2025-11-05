import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

#TEST
import leafmap.foliumap as leafmap
import pandas as pd
import streamlit as st
import folium

# 設定頁面與標題
st.set_page_config(layout="wide")
st.title("原鄉部落座標與資訊")

# 假設的座標欄位
N_LAT_COL = 'NT_lat'
N_LON_COL = 'NT_lon'
O_LAT_COL = 'OT_lat'
O_LON_COL = 'OT_lon'
O_NAME_COL = 'O_Tribe'

# 載入資料
tribes_url = "https://github.com/8048-kh/test02/raw/refs/heads/main/tribe.csv"
tribes_df = pd.read_csv(tribes_url)
tribe_names = tribes_df['N_Tribe'].dropna().unique().tolist()
tribe_names.sort()

# Streamlit 選單
selected_tribe = st.selectbox("選擇主要部落", tribe_names)

# 過濾資料
selected_data = tribes_df[tribes_df['N_Tribe'] == selected_tribe].copy()
if selected_data.empty:
    st.info("找不到相關資料。")
    st.stop()

# 初始化地圖
main_data = selected_data.iloc[0]
n_lat = main_data[N_LAT_COL]
n_lon = main_data[N_LON_COL]

m = leafmap.Map(center=[n_lat, n_lon], zoom=13)
m.add_shp("https://github.com/8048-kh/Debris-rep/raw/refs/heads/master/Data/Full_Nantou_Tribe.shp")

# --- 標記主要部落 (N_Tribe) ---
main_icon = folium.Icon(color='blue', icon='star', prefix='fa')
m.add_marker(
    location=(n_lat, n_lon),
    tooltip=selected_tribe,
    popup=f"N-Tribe: {selected_tribe}",
    icon=main_icon
)

# --- 標記子部落 (O_Tribe) ---
o_tribe_data = selected_data.dropna(subset=[O_NAME_COL, O_LAT_COL, O_LON_COL])
sub_icon = folium.Icon(color='purple', icon='map-pin', prefix='fa')
o_tribe_names_list = []

for index, row in o_tribe_data.iterrows():
    o_lat = row[O_LAT_COL]
    o_lon = row[O_LON_COL]
    o_name = row[O_NAME_COL]

    # 簡單避免與主要部落標記重疊的判斷
    if o_name and abs(o_lat - n_lat) > 0.0001 or abs(o_lon - n_lon) > 0.0001:
        m.add_marker(
            location=(o_lat, o_lon),
            tooltip=o_name,
            popup=f"O-Tribe: {o_name}",
            icon=sub_icon
        )
        o_tribe_names_list.append(o_name)

# --- 顯示資訊 ---
st.write(f"您選擇的部落：**{selected_tribe}**")

unique_o_tribe_names = pd.Series(o_tribe_names_list).unique().tolist()
if unique_o_tribe_names:
    st.markdown(f"**子部落 (O-Tribe)**： {', '.join(unique_o_tribe_names)}")

# 刪除標題，只保留資料框顯示
st.dataframe(selected_data.fillna('-'))

# 顯示地圖
m.to_streamlit(height=700)
