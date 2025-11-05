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

st.set_page_config(layout="wide")

st.title("原鄉部落座標與資訊 📍")

# Assumed column names
N_LAT_COL = 'NT_lat'
N_LON_COL = 'NT_lon'
O_LAT_COL = 'OT_lat'
O_LON_COL = 'OT_lon'
O_NAME_COL = 'O_Tribe'

# Load the tribes data
tribes = "https://github.com/8048-kh/test02/raw/refs/heads/main/tribe.csv"
try:
    tribes_df = pd.read_csv(tribes)
except Exception as e:
    st.error(f"無法載入部落資料：{e}")
    st.stop() # 停止執行，避免後續錯誤

tribe_names = tribes_df['N_Tribe'].dropna().unique().tolist()
tribe_names.sort()

# Streamlit interface
selected_tribe = st.selectbox(
    "選擇主要部落 (N_Tribe)", tribe_names, key="selectbox_tribe"
)

# Filter data
selected_data = tribes_df[tribes_df['N_Tribe'] == selected_tribe].copy()

# Leafmap map object initialization (使用台灣中心點)
m = leafmap.Map(center=[23.97565, 120.9738819], zoom=7)

# Add shapefile layer
try:
    m.add_shp("https://github.com/8048-kh/Debris-rep/raw/refs/heads/master/Data/Full_Nantou_Tribe.shp")
except Exception as e:
    st.warning(f"無法載入 Shapefile 圖層: {e}")

# 初始化座標
n_lat, n_lon = None, None

# --- 1. Mark Main Tribe (N_Tribe) ---
if N_LAT_COL in selected_data.columns and N_LON_COL in selected_data.columns and not selected_data.empty:
    # 取用該 N_Tribe 記錄的第一組 NT_lat/NT_lon 作為主要座標
    n_lat = selected_data[N_LAT_COL].iloc[0]
    n_lon = selected_data[N_LON_COL].iloc[0]

    # Blue Star Icon for Main Tribe
    main_icon = folium.Icon(color='blue', icon='star', prefix='fa')

    m.add_marker(
        location=(n_lat, n_lon),
        tooltip=f"主要部落: {selected_tribe}",
        popup=f"**🌟 主要部落：{selected_tribe}**<br>經度: {n_lon:.4f}<br>緯度: {n_lat:.4f}",
        icon=main_icon
    )

    # Set map center
    m.set_center(n_lon, n_lat, zoom=13)

# --- 2. Mark Sub Tribes (O_Tribe) ---

# 過濾出有子部落名稱和座標的行
o_tribe_data = selected_data.dropna(subset=[O_NAME_COL, O_LAT_COL, O_LON_COL])
o_tribe_names_list = []

if not o_tribe_data.empty:
    
    # Purple Pin Icon for Sub Tribes
    sub_icon = folium.Icon(color='purple', icon='map-pin', prefix='fa')
    
    # Iterate and add markers for O_Tribe
    for index, row in o_tribe_data.iterrows():
        o_lat = row[O_LAT_COL]
        o_lon = row[O_LON_COL]
        o_name = row[O_NAME_COL]

        # 檢查子部落座標是否與主要部落座標幾乎相同
        is_main_location = (n_lat is not None and abs(o_lat - n_lat) < 0.0001 and abs(o_lon - n_lon) < 0.0001)
        
        # 僅標記名稱存在且與主要部落位置不同的子部落
        if o_name and not is_main_location:
            m.add_marker(
                location=(o_lat, o_lon),
                tooltip=f"子部落: {o_name}",
                popup=f"📍 子部落：{o_name}<br>經度: {o_lon:.4f}<br>緯度: {o_lat:.4f}",
                icon=sub_icon
            )
            o_tribe_names_list.append(o_name)

    # --- 3. List O_Tribe Names ---
    # 使用 set 進行去重並排序
    unique_o_tribe_names = sorted(list(set(o_tribe_names_list)))
    
    if unique_o_tribe_names:
        st.subheader(f"📌 {selected_tribe} 隸屬的子部落 (O_Tribe) 列表") # 將 {selected_tribe} 加入標題
        st.info("、".join(unique_o_tribe_names))
    
else:
    # 顯示主要部落資訊，如果沒有子部落資料
    st.subheader(f"📌 {selected_tribe} 主要資訊 (無子部落紀錄)")
    if not selected_data.empty:
        # 只顯示第一行的轉置資訊，更簡潔
        st.dataframe(selected_data.head(1).T.fillna('-'))


# Display the map
m.set_center(n_lon, n_lat, zoom=13)
m.to_streamlit(height=700)

