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
tribes = "https://github.com/8048-kh/test02/raw/refs/heads/main/old_tribe.csv"
tribes_df = pd.read_csv(tribes, encoding='latin-1')
tribes_df = pd.read_csv(tribes)
tribes_df = pd.read_csv(tribes, encoding='latin-1')
tribe_names = tribes_df['N_Tribe'].tolist()

# Add points to the map
# Create a selectbox for tribe names
selected_tribe = st.selectbox(
    "選擇部落", tribe_names, key="selectbox_tribe"
)

# Get the data of the selected tribe
selected_tribe_data = tribes_df[tribes_df['tribe name'] == selected_tribe].iloc[0]

# Get coordinates from 'latitude' and 'longitude'
latitude = selected_tribe_data['NT_lat']
longitude = selected_tribe_data['NT_lon']
m.add_shp("https://github.com/8048-kh/Debris-rep/raw/refs/heads/master/Data/Full_Nantou_Tribe.shp")
# Recenter and zoom to the selected tribe
m.set_center(longitude, latitude, zoom=15) 
m.add_marker(location=(latitude, longitude), tooltip=selected_tribe, popup=f"{selected_tribe}")
# Display the map in Streamlit
st.write(f"您選擇的部落是：{selected_tribe}")
st.table(selected_tribe_data)
m.to_streamlit(height=700)
