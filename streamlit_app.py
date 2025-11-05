import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

#TEST

import leafmap.foliumap as leafmap
import pandas as pd
st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Web App URL: <https://nantoudebris.streamlit.app/>
GitHub Repository: <https://github.com/8048-kh/Debris-rep/tree/master>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://s3-ap-northeast-1.amazonaws.com/lazybusiness/data/nellhung_175/images/2023/08/0806/1.jpeg"
st.sidebar.image(logo)

# Customize page title
st.title("南投原鄉部落與土石流分布")

st.markdown(
    """
    南投原鄉部落與土石流潛勢溪流、土石流潛勢溪流範圍分布
    """
)

st.header("目錄")

markdown = """
1. 原鄉部落座標與資訊
2. 原鄉部落與土石流潛勢溪流
3. 原鄉部落與土石流潛勢溪流範圍
4. 土石流潛勢溪流範圍熱區圖

"""

st.markdown(markdown)


#m = leafmap.Map(center=[23.932630, 120.986852], zoom=10)
#tribes = "https://github.com/8048-kh/Debris-rep/raw/refs/heads/master/Data/Nantou_Tribe.csv"
tribes_df = pd.read_csv("https://github.com/8048-kh/Debris-rep/raw/refs/heads/master/Data/Nantou_Tribe.csv")
st.header("部落名稱")
st.table(tribes_df[["tribe name"]])
