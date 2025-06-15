import streamlit as st
import pandas as pd

st.title("❤️ 我的最愛")

if 'logged_in' not in st.session_state or st.session_state.logged_in == False:
    st.warning("請先登入")
    st.stop()  # 停止載入頁面內容
    
favorites = st.session_state.get("favorites", [])

if favorites:
    for fav in favorites:
        with st.container(border=True):
            cols = st.columns([1, 2])
            with cols[0]:
                if 'picture' in fav and pd.notna(fav['picture']):
                    st.image(fav['picture'], width=150)
            with cols[1]:
                st.subheader(f"編號：{fav['animal_id']} / {fav['animal_Variety']}")
                st.markdown(f"""
                - **性別**：{fav['animal_sex']}　**體型**：{fav['animal_bodytype']}　**年齡**：{fav['animal_age']}
                - **毛色**：{fav['animal_colour']}　**是否絕育**：{fav['animal_sterilization']}
                - 📝 備註：{fav.get('animal_remark', '無')}
                - 🏠 收容所：{fav['shelter_name']}
                - 📍 地址：{fav['shelter_address']}
                - ☎️ 電話：{fav['shelter_tel']}
                """)
else:
    st.info("你目前尚未加入任何最愛。")
