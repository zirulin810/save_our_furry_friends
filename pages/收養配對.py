import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("adoption.csv")

df = load_data()

# 初始化 session state
if "index" not in st.session_state:
    st.session_state.index = 0
if "favorites" not in st.session_state:
    st.session_state.favorites = []

st.title("🐾 猜你喜歡...")

if st.session_state.index < len(df):
    row = df.iloc[st.session_state.index]

    with st.container(border=True):
        cols = st.columns([1, 2])
        with cols[0]:
            if 'album_file' in row and pd.notna(row['album_file']):
                st.image(row['album_file'], width=150, caption="點我看大圖")
        with cols[1]:
            st.subheader(f"編號：{row['animal_id']} / {row['animal_Variety']}")
            st.markdown(f"""
            - **性別**：{row['animal_sex']}　**體型**：{row['animal_bodytype']}　**年齡**：{row['animal_age']}
            - **毛色**：{row['animal_colour']}　**是否絕育**：{row['animal_sterilization']}
            - **收容所**：{row['shelter_name']}
            - 📍 地址：{row['shelter_address']}
            - ☎️ 電話：{row['shelter_tel']}
            """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("❤️ 有興趣"):
            st.session_state.favorites.append(row.to_dict())
            st.session_state.index += 1
            st.rerun()
    with col2:
        if st.button("❌ 沒有興趣"):
            st.session_state.index += 1
            st.rerun()
else:
    st.success("你已經看完所有資料囉！")
