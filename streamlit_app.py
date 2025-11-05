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

# Leafmap map object initialization 確保 m 始終被定義
m = leafmap.Map(center=[23.97565, 120.9738819], zoom=7)

# Load the tribes data
tribes = "https://github.com/8048-kh/test02/raw/refs/heads/main/tribe.csv"
try:
    tribes_df = pd.read_csv(tribes)
    
    # Add shapefile layer - 提前處理，避免被 try/except 區塊影響
    try:
        m.add_shp("https://github.com/8048-kh/Debris-rep/raw/refs/heads/master/Data/Full_Nantou_Tribe.shp")
    except Exception as e:
        st.warning(f"無法載入 Shapefile 圖層: {e}")

except Exception as e:
    # 如果資料載入失敗，顯示錯誤信息，顯示地圖（可能是空圖），然後停止執行
    st.error(f"無法載入部落資料，應用程式無法繼續：{e}")
    m.to_streamlit(height=700)
    st.stop() 

# 確保程式碼只有在 tribes_df 成功載入後才會繼續執行
tribe_names = tribes_df['N_Tribe'].dropna().unique().tolist()
tribe_names.sort()

# Streamlit interface
selected_tribe = st.selectbox(
    "選擇部落：", tribe_names, key="selectbox_tribe"
)

# Filter data
selected_data = tribes_df[tribes_df['N_Tribe'] == selected_tribe].copy()

# 初始化座標
n_lat, n_lon = None, None

# --- 1. Mark Main Tribe (N_Tribe) ---
if N_LAT_COL in selected_data.columns and N_LON_COL in selected_data.columns and not selected_data.empty:
    n_lat = selected_data[N_LAT_COL].iloc[0]
    n_lon = selected_data[N_LON_COL].iloc[0]

    # Blue Star Icon for Main Tribe
    main_icon = folium.Icon(color='blue', icon='star', prefix='fa')

    m.add_marker(
        location=(n_lat, n_lon),
        tooltip=f"{selected_tribe}",
        popup=f"**{selected_tribe}**<br>經度: {n_lon:.4f}<br>緯度: {n_lat:.4f}",
        icon=main_icon
    )
    m.set_center(n_lon, n_lat, zoom=15)

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
    unique_o_tribe_names = sorted(list(set(o_tribe_names_list)))
    
    if unique_o_tribe_names:
        st.subheader(f"📌 {selected_tribe} 居民原居地：") 
        st.info("、".join(unique_o_tribe_names))
    
else:
    # 顯示主要部落資訊，如果沒有子部落資料
    st.subheader(f"📌 {selected_tribe} 主要資訊 (無子部落紀錄)")
    if not selected_data.empty:
        st.dataframe(selected_data.head(1).T.fillna('-'))


# Display the map
m.to_streamlit(height=700)
