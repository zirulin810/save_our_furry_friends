import streamlit as st
import pandas as pd
from utils import streamlit_utils # type: ignore
import Streamlit_MSQL_Server_Connection.connect as connect # type: ignore

streamlit_utils.require_login()

# 測試資料
if "fur_color" not in st.session_state:
    st.session_state.fur_color = "白色"
if "gender" not in st.session_state:
    st.session_state.gender = "F"
if "size" not in st.session_state:
    st.session_state.size = "SMALL"

# 初始化
if "index" not in st.session_state:
    st.session_state.index = 0

def load_data():
    user_name = st.session_state.user_name
    conn = connect.get_connection()

    # 取出已經按過喜歡的 animal_id
    fav_sql = "SELECT animal_id FROM loved_dog_record WHERE user_name = %s"
    favorite_ids = pd.read_sql(fav_sql, conn, params=(user_name,))
    favorite_ids_list = favorite_ids['animal_id'].tolist()
    
    # 預設條件值
    color = st.session_state.fur_color
    gender = st.session_state.gender
    size = st.session_state.size

    # 查詢剩下的狗狗，並根據符合條件數排序
    base_sql = f"""
        SELECT d.animal_id, d.animal_Variety, d.animal_sex, d.animal_bodytype,
               d.animal_age, d.animal_colour, d.animal_sterilization, d.picture,
               d.animal_remark, s.shelter_name, s.shelter_address, s.shelter_tel,
               -- 計算匹配分數：每個符合條件加一分
               (CASE WHEN d.animal_colour = %s THEN 1 ELSE 0 END +
                CASE WHEN d.animal_sex = %s THEN 1 ELSE 0 END +
                CASE WHEN d.animal_bodytype = %s THEN 1 ELSE 0 END) AS match_score
        FROM shelter_dogs_info AS d
        JOIN shelter_info AS s ON d.shelter_id = s.shelter_id
    """

    # 加上排除 favorite 條件
    if favorite_ids_list:
        format_ids = ','.join(['%s'] * len(favorite_ids_list))
        base_sql += f" WHERE d.animal_id NOT IN ({format_ids})"
        params = [color, gender, size] + favorite_ids_list
    else:
        params = [color, gender, size]

    # 根據符合條件數倒序排序
    base_sql += " ORDER BY match_score DESC"

    df = pd.read_sql(base_sql, conn, params=params)
    conn.close()

    if df.empty:
        st.info("找不到符合條件的狗狗。")
    return df


def save_loved_dog(user_name: str, animal_id: int):
    conn = connect.get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO loved_dog_record (user_name, animal_id)
        VALUES (%s, %s)
    """
    cursor.execute(sql, (user_name, animal_id))
    conn.commit()

    cursor.close()
    conn.close()


if "df" not in st.session_state:
    st.session_state.df = load_data()


st.title("🐾 猜你喜歡...")

if st.session_state.index < len(st.session_state.df):
    row = st.session_state.df.iloc[st.session_state.index]

    with st.container(border=True):
        cols = st.columns([1, 2])
        with cols[0]:
            pic = row.get('picture', '')
            if pic:
                st.image(pic, width=150, caption="點我看大圖")
            else:
                st.markdown("📷 尚無圖片")
        with cols[1]:
            st.subheader(f"編號：{row['animal_id']} / {row['animal_Variety']}")
            st.markdown(f"""
            - **性別**：{row['animal_sex']}　**體型**：{row['animal_bodytype']}　**年齡**：{row['animal_age']}
            - **毛色**：{row['animal_colour']}　**是否絕育**：{row['animal_sterilization']}
            - 📝 備註：{row['animal_remark'] or "無"}
            - 🏠 收容所：{row['shelter_name']}
            - 📍 地址：{row['shelter_address']}
            - ☎️ 電話：{row['shelter_tel']}
            """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("❤️ 有興趣"):
            save_loved_dog(st.session_state.user_name, int(row["animal_id"]))
            st.session_state.index += 1
            st.rerun()
    with col2:
        if st.button("❌ 沒有興趣"):
            st.session_state.index += 1
            st.rerun()
else:
    st.success("你已經看完所有資料囉！")
