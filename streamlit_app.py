import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

#TEST
import leafmap.foliumap as leafmap
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.title("原鄉部落座標與資訊")

# Load the tribes data
tribes = "https://github.com/8048-kh/test02/raw/refs/heads/main/tribe.csv"

# --- 增加資料載入的錯誤處理 (建議) ---
try:
    tribes_df = pd.read_csv(tribes)
    tribe_names = tribes_df['N_Tribe'].tolist()
except Exception as e:
    st.error(f"無法載入部落資料：{e}")
    st.stop()
# ------------------------------------

# Create a Leafmap map object
m = leafmap.Map(center=[23.97565, 120.9738819], zoom=8) # 調整zoom為8，讓初始地圖更廣闊

# Create a selectbox for tribe names
selected_tribe = st.selectbox(
    "選擇部落", tribe_names, key="selectbox_tribe", index=tribe_names.index('清流部落') if '清流部落' in tribe_names else 0 # 預設選取清流部落
)

# Get the data of the selected tribe
selected_tribe_data = tribes_df[tribes_df['N_Tribe'] == selected_tribe].iloc[0]

# Get coordinates from 'latitude' and 'longitude'
latitude = selected_tribe_data['NT_lat']
longitude = selected_tribe_data['NT_lon']

# Add Shapefile layer (Ensure the URL is accessible and the file is a valid .shp)
m.add_shp("https://github.com/8048-kh/Debris-rep/raw/refs/heads/master/Data/Full_Nantou_Tribe.shp", name="南投部落界線", zoom_to_layer=False)

# Recenter and zoom to the selected tribe
m.set_center(longitude, latitude, zoom=15)
m.add_marker(location=(latitude, longitude), tooltip=selected_tribe, popup=f"**{selected_tribe}**")

# --- 顯示結果區塊 ---
st.header(f"您選擇的部落是：**{selected_tribe}**")

# 使用 Streamlit columns 顯示經緯度 (讓版面更美觀)
col1, col2 = st.columns(2)
col1.metric("📌 經度 (Longitude)", f"{longitude:.6f}")
col2.metric("📌 緯度 (Latitude)", f"{latitude:.6f}")

# 顯示選取部落的完整資訊
st.subheader("📊 部落詳細資料")
st.dataframe(selected_tribe_data.to_frame().T) # 轉置後顯示更像表格

# --- 核心修改：針對「清流部落」顯示所有 O_Tribe ---
if selected_tribe == "清流部落":
    st.markdown("---")
    st.subheader("📋 所有部落的原始名稱 (O_Tribe) 列表")
    
    # 篩選出 N_Tribe 和 O_Tribe 兩欄，並顯示
    o_tribe_data = tribes_df[['N_Tribe', 'O_Tribe']].drop_duplicates().reset_index(drop=True)
    
    # 重新命名欄位以符合中文語境
    o_tribe_data.columns = ['部落名稱 (N_Tribe)', '原始/舊名 (O_Tribe)']
    
    st.dataframe(o_tribe_data)
    st.info("💡 這是由於您特別要求，在選擇「清流部落」時額外顯示所有部落的原始名稱資訊。")
# ----------------------------------------------------

# Display the map in Streamlit
st.subheader("🗺️ 地圖顯示")
m.to_streamlit(height=700)
