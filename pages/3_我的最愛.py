import streamlit as st
import pandas as pd
from utils import streamlit_utils # type: ignore
import Streamlit_MSQL_Server_Connection.connect as connect # type: ignore

streamlit_utils.require_login()

st.title("❤️ 我的最愛")
    
def get_favorites(user_name: str):
    conn = connect.get_connection()
    
    sql = """
        SELECT d.animal_id, d.animal_Variety, d.animal_sex, d.animal_bodytype,
               d.animal_age, d.animal_colour, d.animal_sterilization, d.picture,
               d.animal_remark, s.shelter_name, s.shelter_address, s.shelter_tel
        FROM loved_dog_record AS l
        JOIN shelter_dogs_info AS d ON l.animal_id = d.animal_id
        JOIN shelter_info AS s ON d.shelter_id = s.shelter_id
        WHERE l.user_name = %s
        ORDER BY l.created_at DESC
    """
    df = pd.read_sql(sql, conn, params=(user_name,))
    conn.close()
    return df

def delete_favorite(user_name: str, animal_id: str):
    conn = connect.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM loved_dog_record WHERE user_name = %s AND animal_id = %s",
        (user_name, animal_id)
    )
    conn.commit()
    conn.close()

favorites = get_favorites(st.session_state.user_name)

if not favorites.empty:
    for index, fav in favorites.iterrows():
        with st.container(border=True):
            cols = st.columns([1, 2])
            with cols[0]:
                if fav['picture']:
                    st.image(fav['picture'], width=150)
                else:
                    st.markdown("📷 尚無圖片")
            with cols[1]:
                st.subheader(f"編號：{fav['animal_id']} / {fav['animal_Variety']}")
                st.markdown(f"""
                - **性別**：{fav['animal_sex']}　**體型**：{fav['animal_bodytype']}　**年齡**：{fav['animal_age']}
                - **毛色**：{fav['animal_colour']}　**是否絕育**：{fav['animal_sterilization']}
                - 📝 備註：{fav['animal_remark'] or '無'}
                - 🏠 收容所：{fav['shelter_name']}
                - 📍 地址：{fav['shelter_address']}
                - ☎️ 電話：{fav['shelter_tel']}
                """)
            if st.button("🗑️ 移除最愛", key=f"delete_{index}"):
                delete_favorite(st.session_state.user_name, fav['animal_id'])
                st.success("已移除最愛 🐾")
                st.rerun()  # 重新整理頁面
else:
    st.info("你目前尚未加入任何最愛。")
