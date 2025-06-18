import streamlit as st

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("請先登入")
    st.stop()

import pandas as pd
from datetime import datetime
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Streamlit_MSQL_Server_Connection")))
import connect

# 初始化 session state
for key in ["show_manage_dog", "show_add_diary", "show_my_diary", "show_add_dog"]:
    if key not in st.session_state:
        st.session_state[key] = False

st.title("🐶 狗狗中心")

# 🧭 功能選單（固定側邊欄）
with st.sidebar:
    st.markdown("### 📂 功能選單")
    if st.button("🏠 回首頁"):
        st.session_state.show_manage_dog = False
        st.session_state.show_add_diary = False
        st.session_state.show_my_diary = False
    if st.button("🐾 管理狗狗"):
        st.session_state.show_manage_dog = True
        st.session_state.show_add_diary = False
        st.session_state.show_my_diary = False
    if st.button("📝 撰寫日記"):
        st.session_state.show_add_diary = True
        st.session_state.show_manage_dog = False
        st.session_state.show_my_diary = False
    if st.button("📓 我的狗狗日記"):
        st.session_state.show_my_diary = True
        st.session_state.show_manage_dog = False
        st.session_state.show_add_diary = False


@st.cache_resource
def get_user_dog_options():
    try:
        conn = connect.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_name, dog_name FROM dog_owner_record")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"讀取狗狗列表失敗：{e}")
        return []

options = get_user_dog_options()

# 管理狗狗
if st.session_state.show_manage_dog:
    st.header("🐾 管理狗狗")
    user_name = st.session_state.user_name
    st.info(f"目前登入使用者：{user_name}")

    conn = connect.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT dog_name FROM dog_owner_record WHERE user_name = %s", (user_name,))
    dogs = cursor.fetchall()

    if dogs:
        st.markdown("### 🐶 我的狗狗列表")
        for dog in dogs:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"狗狗名字：{dog[0]}")
            with col2:
                if st.button(f"❌ 刪除 {dog[0]}", key=f"delete_{dog[0]}"):
                    try:
                        cursor.execute("DELETE FROM diary_record WHERE user_name = %s AND dog_name = %s", (user_name, dog[0]))
                        cursor.execute("DELETE FROM dog_owner_record WHERE user_name = %s AND dog_name = %s", (user_name, dog[0]))
                        conn.commit()
                        st.success(f"已刪除：{dog[0]} 及其所有日記紀錄")
                        st.rerun()
                    except Exception as e:
                        st.error(f"刪除失敗：{e}")
    else:
        st.info("此使用者尚未擁有狗狗")

    st.markdown("### ➕ 新增狗狗")
    new_dog = st.text_input("新狗狗名字")
    if st.button("新增狗狗"):
        if new_dog.strip():
            try:
                cursor.execute("INSERT INTO dog_owner_record (user_name, dog_name, created_at, updated_at) VALUES (%s, %s, NOW(), NOW())", (user_name, new_dog))
                conn.commit()
                st.success("新增成功！")
                st.cache_resource.clear()
                st.rerun()
            except Exception as e:
                st.error(f"新增失敗：{e}")
    cursor.close()
    conn.close()

# 撰寫日記
if st.session_state.show_add_diary:
    st.header("📝 撰寫狗狗日記")
    user_input = st.session_state.user_name
    st.info(f"目前登入使用者：{user_input}")

    matching_dogs = [row[1] for row in options if row[0] == user_input]
    with st.form("add_diary_form"):
        dog_input = st.selectbox("選擇狗狗", matching_dogs)
        mood = st.text_input("今天心情")
        content = st.text_area("日記內容")
        col1, col2 = st.columns([1, 1])
        submit = col1.form_submit_button("✍️ 儲存")
        cancel = col2.form_submit_button("取消")

        if submit:
            if dog_input and content.strip():
                now = datetime.now()
                conn = connect.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM dog_owner_record WHERE user_name = %s AND dog_name = %s", (user_input, dog_input))
                dog_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO diary_record (user_name, dog_name, dog_id, mood, date, time, content, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (user_input, dog_input, dog_id, mood, now.date(), now.strftime("%H:%M"), content, now, now)
                )
                conn.commit()
                st.success("日記儲存成功！")
                st.rerun()
            else:
                st.warning("請選擇狗狗並填寫內容")
        if cancel:
            st.session_state.show_add_diary = False

# 我的狗狗日記
if st.session_state.show_my_diary:
    st.header("📓 我的狗狗日記")
    selected_user = st.session_state.user_name
    st.info(f"目前登入使用者：{selected_user}")

    conn = connect.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, date, time, mood, content, dog_name FROM diary_record WHERE user_name = %s ORDER BY created_at DESC", (selected_user,))
    diaries = cursor.fetchall()
    cursor.close()
    conn.close()

    if diaries:
        for d in diaries:
            with st.container():
                st.subheader(f"🐶 {d['dog_name']}")
                st.write(f"🕒 {d['date']} {d['time']}　😊 {d['mood']}")
                st.markdown(f"📖 {d['content']}")
    else:
        st.info("尚無任何日記紀錄。")

# 所有日記（預設）
if not any([st.session_state.show_manage_dog, st.session_state.show_add_diary, st.session_state.show_my_diary]):
    st.header("📰 最新狗狗日記")
    conn = connect.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_name, dog_name, date, time, mood, content FROM diary_record ORDER BY created_at DESC LIMIT 10")
    recs = cursor.fetchall()
    cursor.close()
    conn.close()
    if recs:
        for d in recs:
            with st.container():
                st.subheader(f"👤 {d['user_name']}　🐶 {d['dog_name']}")
                st.write(f"🕒 {d['date']} {d['time']}　😊 {d['mood']}")
                st.markdown(f"📖 {d['content']}")
    else:
        st.info("目前沒有任何日記。")