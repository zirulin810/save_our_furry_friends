import streamlit as st
import pandas as pd
from utils import streamlit_utils # type: ignore
import Streamlit_MSQL_Server_Connection.connect as connect # type: ignore

streamlit_utils.require_login()

# 初始化
if "index" not in st.session_state:
    st.session_state.index = 0

class LovedInfo:
    def __init__(self, color, size, age, gender, sterilization, city):
        self.color = color
        self.size = size
        self.age = age
        self.gender = gender
        self.sterilization = sterilization
        self.city = city

def load_raw_data():
    conn = connect.get_connection()

    query = """
        SELECT d.animal_id, d.animal_Variety, d.animal_sex, d.animal_bodytype,
               d.animal_age, d.animal_colour, d.animal_sterilization, d.picture,
               d.animal_remark, s.shelter_name, s.shelter_address, s.shelter_tel
        FROM shelter_dogs_info AS d
        JOIN shelter_info AS s ON d.shelter_id = s.shelter_id
        ORDER BY d.animal_id
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        st.info("目前資料庫中沒有狗狗資料。")
    return df

def load_data(info: LovedInfo, user_name: str):
    conn = connect.get_connection()

    # 查詢剩下的狗狗，並根據符合條件數排序
    base_sql = """
        SELECT d.animal_id, d.animal_Variety, d.animal_sex, d.animal_bodytype,
               d.animal_age, d.animal_colour, d.animal_sterilization, d.picture,
               d.animal_remark, s.shelter_name, s.shelter_address, s.shelter_tel,
               -- 計算匹配分數
               (CASE WHEN d.animal_colour = %s THEN 3 ELSE 0 END +
                CASE WHEN d.animal_sex = %s THEN 1 ELSE 0 END +
                CASE WHEN d.animal_bodytype = %s THEN 1 ELSE 0 END +
                CASE WHEN d.animal_age = %s THEN 1 ELSE 0 END +
                CASE WHEN d.animal_sterilization = %s THEN 1 ELSE 0 END +
                CASE WHEN s.shelter_address LIKE %s THEN 3 ELSE 0 END) AS match_score
        FROM shelter_dogs_info AS d
        JOIN shelter_info AS s ON d.shelter_id = s.shelter_id
        WHERE NOT EXISTS (
            SELECT 1 FROM loved_dog_record l
            WHERE l.animal_id = d.animal_id AND l.user_name = %s
        )
        ORDER BY match_score DESC
    """

    # 組合查詢參數 
    params = [
        info.color,
        info.gender,
        info.size,
        info.age,
        info.sterilization,
        f"%{info.city}%",
        user_name
    ]

    # 查詢並關閉連線
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

st.title("🐾 猜你喜歡...")

if "ans_info" in st.session_state and "ans_area" in st.session_state:
    # 絕育狀態轉換："是" → "T"，"否" → "F"
    sterilization = "T" if st.session_state.ans_info[4] == "是" else "F"

    # 體型轉換：1, 2 → SMALL；3, 4 → MEDIUM；5 → BIG
    size_map = {
        (1, 2): "SMALL",
        (3, 4): "MEDIUM",
        (5,): "BIG"
    }
    size_value = st.session_state.ans_info[1]
    size = next(v for k, v in size_map.items() if size_value in k)

    info = LovedInfo(
        color=st.session_state.ans_info[0],
        size=size,
        age=st.session_state.ans_info[2],
        gender=st.session_state.ans_info[3],
        sterilization=sterilization,
        city=st.session_state.ans_area[0]
    )

    st.session_state.df = load_data(info, st.session_state.user_name)

if "df" not in st.session_state:
    st.session_state.df = load_raw_data()

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
