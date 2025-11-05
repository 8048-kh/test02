import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

#TEST
import leafmap.foliumap as leafmap
import pandas as pd

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

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
    "選擇部落", tribe_names, key="selectbox_tribe"
)

# 載入 Shapefile 圖層 (不論選擇哪個部落都顯示)
m.add_shp("https://github.com/8048-kh/Debris-rep/raw/refs/heads/master/Data/Full_Nantou_Tribe.shp")

st.write(f"您選擇的部落是：**{selected_tribe}**")

# --- 核心邏輯：根據選擇的部落進行不同處理 ---

if selected_tribe == "清流部落":
    # 專門處理「清流部落」：列出並標記所有 O_Tribe
    
    # 假設 O_Tribe 座標欄位為 OT_lat 和 OT_lon
    LAT_COL = 'OT_lat'
    LON_COL = 'OT_lon'
    NAME_COL = 'O_Tribe' # 子部落名稱欄位

    # 過濾出所有隸屬於「清流部落」的子部落資料
    qingliu_data = tribes_df[tribes_df['N_Tribe'] == "清流部落"].copy()

    if qingliu_data.empty:
        st.warning("「清流部落」資料中找不到子部落資訊，請檢查您的 CSV 檔案結構。")
    else:
        # 1. 列出所有 O_Tribe 名稱
        # 使用存在的欄位名稱，如果沒有 O_Tribe 就使用 N_Tribe
        o_tribe_names = qingliu_data.get(NAME_COL, qingliu_data['N_Tribe']).unique().tolist()
        st.markdown("##### 包含的子部落 (O_Tribe) 列表:")
        st.info("、".join(o_tribe_names))
        
        # 2. 標記所有 O_Tribe 的位置
        # 檢查假設的座標欄位是否存在，不存在則使用 N_Tribe 的座標
        lat_to_use = LAT_COL if LAT_COL in qingliu_data.columns else 'NT_lat'
        lon_to_use = LON_COL if LON_COL in qingliu_data.columns else 'NT_lon'
        name_to_use = NAME_COL if NAME_COL in qingliu_data.columns else 'N_Tribe'
        
        # 計算中心點
        center_lat = qingliu_data[lat_to_use].mean()
        center_lon = qingliu_data[lon_to_use].mean()
        
        # 設置中心點並放大
        m.set_center(center_lon, center_lat, zoom=14)
        
        # 迭代添加子部落標記
        for index, row in qingliu_data.iterrows():
            lat = row[lat_to_use]
            lon = row[lon_to_use]
            o_name = row[name_to_use]
            
            # 使用紅色標記來區分子部落
            m.add_marker(
                location=(lat, lon), 
                tooltip=o_name, 
                popup=f"📍 子部落：{o_name}",
            )
        
        # 3. 顯示相關資料表格
        st.subheader("「清流部落」所有子部落地點資訊")
        # 選擇顯示的欄位
        display_cols = [col for col in qingliu_data.columns if col in ['N_Tribe', name_to_use, lat_to_use, lon_to_use]]
        st.dataframe(qingliu_data[display_cols].fillna('')) 

else:
    # 處理其他部落：只標記單一主要 N_Tribe
    
    # 取第一個匹配的部落資料 (假設 N_Tribe 只有一個代表座標)
    selected_tribe_data = tribes_df[tribes_df['N_Tribe'] == selected_tribe].iloc[0]

    # 取得座標 (使用原有的 NT_lat 和 NT_lon)
    latitude = selected_tribe_data['NT_lat']
    longitude = selected_tribe_data['NT_lon']
    
    # 設置中心點並放大
    m.set_center(longitude, latitude, zoom=15) 
    
    # 添加單一主要部落標記
    m.add_marker(location=(latitude, longitude), tooltip=selected_tribe, popup=f"🌟 主要部落：{selected_tribe}")
    
    # 顯示資料表格
    st.subheader(f"「{selected_tribe}」主要資訊")
    # 將單行 Series 轉換為 DataFrame 轉置後顯示，更清晰
    st.dataframe(selected_tribe_data.to_frame().T)

# 顯示地圖
m.to_streamlit(height=700)
