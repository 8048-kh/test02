import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

#TEST
import leafmap.foliumap as leafmap
import pandas as pd
import streamlit as st
import folium # 引入 folium 庫來設定標記顏色

st.set_page_config(layout="wide")

st.title("原鄉部落座標與資訊")

# Create a Leafmap map object
m = leafmap.Map(center=[23.97565, 120.9738819], zoom=4)

# Load the tribes data
tribes = "https://github.com/8048-kh/test02/raw/refs/heads/main/tribe.csv"
try:
    tribes_df = pd.read_csv(tribes)
    # 使用 unique() 確保選單中部落名稱不重複
    tribe_names = tribes_df['N_Tribe'].unique().tolist()
except Exception as e:
    st.error(f"無法載入部落資料：{e}")
    st.stop()

# Create a selectbox for tribe names
selected_tribe = st.selectbox(
    "選擇主要部落 (N_Tribe)", tribe_names, key="selectbox_tribe"
)

# 假設 CSV 檔案中的座標欄位
N_LAT_COL = 'NT_lat'
N_LON_COL = 'NT_lon'
O_LAT_COL = 'OT_lat'
O_LON_COL = 'OT_lon'
O_NAME_COL = 'O_Tribe' # 子部落名稱欄位

# 過濾出所有隸屬於選擇的 N_Tribe 的資料
selected_data = tribes_df[tribes_df['N_Tribe'] == selected_tribe].copy()

if selected_data.empty:
    st.warning(f"找不到 {selected_tribe} 的相關資料，請檢查 CSV 檔案。")
    m.to_streamlit(height=700)
    st.stop()

# 載入 Shapefile 圖層 (不論選擇哪個部落都顯示)
m.add_shp("https://github.com/8048-kh/Debris-rep/raw/refs/heads/master/Data/Full_Nantou_Tribe.shp")

# --- 1. 標記主要部落 N_Tribe ---

# 取得 N_Tribe 的單一座標 (取第一個匹配項)
main_tribe_data = selected_data.iloc[0]
n_lat = main_tribe_data[N_LAT_COL]
n_lon = main_tribe_data[N_LON_COL]

# 設定 N_Tribe (主要部落) 的標記圖示和顏色 (例如：藍色，星星圖示)
main_icon = folium.Icon(color='blue', icon='star', prefix='fa') 

# 添加主要部落標記
m.add_marker(
    location=(n_lat, n_lon), 
    tooltip=f"主要部落: {selected_tribe}", 
    popup=f"**🌟 主要部落：{selected_tribe}**",
    icon=main_icon
)

# 設置地圖中心點 (使用主要部落座標)
m.set_center(n_lon, n_lat, zoom=13)

st.write(f"您選擇的主要部落是：**{selected_tribe}**")

# --- 2. 標記子部落 O_Tribe ---

# 找出所有 O_Tribe 的唯一名稱
# 使用 .dropna() 過濾掉空值，確保只處理有子部落名稱的列
o_tribe_data = selected_data.dropna(subset=[O_NAME_COL, O_LAT_COL, O_LON_COL])

if not o_tribe_data.empty:
    
    # 設置 O_Tribe (子部落) 的標記圖示和顏色 (例如：紫色，地圖釘圖示)
    sub_icon = folium.Icon(color='purple', icon='map-pin', prefix='fa') 

    # 迭代添加子部落標記
    for index, row in o_tribe_data.iterrows():
        o_lat = row[O_LAT_COL]
        o_lon = row[O_LON_COL]
        o_name = row[O_NAME_COL]
        
        # 避免重複標記 N_Tribe (如果 N_Tribe 名稱剛好與 O_Tribe 相同)
        if o_name != selected_tribe:
            m.add_marker(
                location=(o_lat, o_lon), 
                tooltip=f"子部落: {o_name}", 
                popup=f"📍 子部落：{o_name}",
                icon=sub_icon # 使用不同的顏色
            )
            
    # --- 3. 列出所有 O_Tribe 名稱 ---
    o_tribe_names = o_tribe_data[O_NAME_COL].unique().tolist()
    st.subheader("📌 隸屬的子部落 (O_Tribe) 列表")
    st.info("、".join(o_tribe_names))
    
    # 顯示所有子部落地點資訊表格
    st.subheader(f"「{selected_tribe}」所有地點資訊 (包含子部落)")
    display_cols = [col for col in selected_data.columns if col in ['N_Tribe', O_NAME_COL, N_LAT_COL, N_LON_COL, O_LAT_COL, O_LON_COL]]
    st.dataframe(selected_data[display_cols].fillna(''))
else:
    st.info("此主要部落下沒有找到明確的子部落 (O_Tribe) 座標資料。地圖上只標記了主要部落中心點。")
    # 顯示單一主要部落資訊
    st.subheader(f"「{selected_tribe}」主要資訊")
    st.dataframe(main_tribe_data.to_frame().T)

# 顯示地圖
m.to_streamlit(height=700)
