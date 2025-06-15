import streamlit as st
import pandas as pd
from utils import streamlit_utils # type: ignore
import Streamlit_MSQL_Server_Connection.connect as connect # type: ignore

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
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# 逐步放寬條件
def load_data_by_fallback_conditions(base_sql, columns, values):
    conn = connect.get_connection()
    for i in range(len(columns) + 1):
        used_cols = columns[:len(columns) - i]
        used_vals = values[:len(values) - i]
        where_clause = " AND ".join([f"d.{col} = %s" for col in used_cols])
        full_sql = base_sql + (f" WHERE {where_clause}" if where_clause else "")
        df = pd.read_sql(full_sql, conn, params=used_vals)
        if len(df) > 0:
            if i > 0:
                st.warning(f"找不到完全符合條件的狗狗，已移除 {i} 個條件後顯示結果。")
            conn.close()
            return df
    st.info("找不到任何符合條件的狗狗。")
    conn.close()
    return pd.DataFrame()

# 撈資料
def load_data():
    base_sql = """
        SELECT d.animal_id, d.animal_Variety, d.animal_sex, d.animal_bodytype,
               d.animal_age, d.animal_colour, d.animal_sterilization, d.picture,
               d.animal_remark, s.shelter_name, s.shelter_address, s.shelter_tel
        FROM shelter_dogs_info AS d
        JOIN shelter_info AS s ON d.shelter_id = s.shelter_id
    """
    columns = ["animal_colour", "animal_sex", "animal_bodytype"]
    values = [st.session_state.fur_color, st.session_state.gender, st.session_state.size]
    return load_data_by_fallback_conditions(base_sql, columns, values)

if "df" not in st.session_state:
    st.session_state.df = load_data()


st.title("🐾 猜你喜歡...")

# ✅ 顯示資料卡片
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
            st.session_state.favorites.append(row.to_dict())
            st.session_state.index += 1
            st.rerun()
    with col2:
        if st.button("❌ 沒有興趣"):
            st.session_state.index += 1
            st.rerun()
else:
    st.success("你已經看完所有資料囉！")
