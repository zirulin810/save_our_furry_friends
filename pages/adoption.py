import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("adoption.csv")

df = load_data()

st.title("🐾 認領養資料")

for index, row in df.iterrows():
    with st.container(border=True):
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(row['album_file'], width=150, caption="點我看大圖")
        with cols[1]:
            st.subheader(f"編號：{row['animal_id']} / {row['animal_Variety']}")
            st.markdown(f"""
            - **性別**：{row['animal_sex']}　**體型**：{row['animal_bodytype']}　**年齡**：{row['animal_age']}
            - **毛色**：{row['animal_colour']}　**是否絕育**：{row['animal_sterilization']}
            - **來源地點**：{row['animal_foundplace']}
            - **收容所**：{row['shelter_name']}
            - 📍 地址：{row['shelter_address']}
            - ☎️ 電話：{row['shelter_tel']}
            """)
