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

st.title("原鄉部落座標與資訊")

# Leafmap map object initialization
m = leafmap.Map(center=[23.97565, 120.9738819], zoom=4)

# Load the tribes data
tribes = "https://github.com/8048-kh/test02/raw/refs/heads/main/tribe.csv"
tribes_df = pd.read_csv(tribes)
tribe_names = tribes_df['N_Tribe'].dropna().unique().tolist()
tribe_names.sort()

# Streamlit interface
selected_tribe = st.selectbox(
    "選擇主要部落 (N_Tribe)", tribe_names, key="selectbox_tribe"
)

# Assumed column names
N_LAT_COL = 'NT_lat'
N_LON_COL = 'NT_lon'
O_LAT_COL = 'OT_lat'
O_LON_COL = 'OT_lon'
O_NAME_COL = 'O_Tribe'

# Filter data
selected_data = tribes_df[tribes_df['N_Tribe'] == selected_tribe].copy()

# Add shapefile layer
m.add_shp("https://github.com/8048-kh/Debris-rep/raw/refs/heads/master/Data/Full_Nantou_Tribe.shp")

st.header(f"探索 {selected_tribe}")

# --- 1. Mark Main Tribe (N_Tribe) ---
if N_LAT_COL in selected_data.columns and N_LON_COL in selected_data.columns and not selected_data.empty:
    main_tribe_data = selected_data.iloc[0]
    n_lat = main_tribe_data[N_LAT_COL]
    n_lon = main_tribe_data[N_LON_COL]

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
else:
    n_lat, n_lon = None, None # Fallback

st.write(f"您選擇的主要部落是：**{selected_tribe}**")

# --- 2. Mark Sub Tribes (O_Tribe) ---

# Filter sub-tribe data
o_tribe_data = selected_data.dropna(subset=[O_NAME_COL, O_LAT_COL, O_LON_COL])

if not o_tribe_data.empty:
    
    # Purple Pin Icon for Sub Tribes
    sub_icon = folium.Icon(color='purple', icon='map-pin', prefix='fa')

    o_tribe_names_list = []
    
    # Iterate and add markers for O_Tribe
    for index, row in o_tribe_data.iterrows():
        o_lat = row[O_LAT_COL]
        o_lon = row[O_LON_COL]
        o_name = row[O_NAME_COL]

        # Check if the location is approximately the same as the main tribe
        is_main_location = (n_lat is not None and abs(o_lat - n_lat) < 0.0001 and abs(o_lon - n_lon) < 0.0001)
        
        if o_name and not is_main_location:
            m.add_marker(
                location=(o_lat, o_lon),
                tooltip=f"子部落: {o_name}",
                popup=f"📍 子部落：{o_name}<br>經度: {o_lon:.4f}<br>緯度: {o_lat:.4f}",
                icon=sub_icon
            )
            o_tribe_names_list.append(o_name)

    # --- 3. List O_Tribe Names and Display Data ---
    unique_o_tribe_names = pd.Series(o_tribe_names_list).unique().tolist()
    
    if unique_o_tribe_names:
        st.subheader("📌 隸屬的子部落 (O_Tribe) 列表")
        st.info("、".join(unique_o_tribe_names))
    
    st.subheader(f"「{selected_tribe}」所有地點資訊")
    
    default_cols = [N_LAT_COL, N_LON_COL, O_NAME_COL, O_LAT_COL, O_LON_COL]
    display_cols = [col for col in selected_data.columns if col in ['N_Tribe'] + default_cols]

    st.dataframe(selected_data[display_cols].fillna('-'))
    
else:
    # Display main tribe info if no sub-tribe data is available
    st.subheader(f"「{selected_tribe}」主要資訊")
    if not selected_data.empty:
        st.dataframe(selected_data.head(1).T)


# Display the map
m.to_streamlit(height=700)
