import streamlit as st
import mysql.connector
import pandas as pd

# MySQL 連線設定
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        port=3306,
        password="", # <--- 改成你的密碼
        database="save_our_furry_friends"
    )

# 查詢資料表內容
def fetch_dog_breeds():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DOG_BREED")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    cursor.close()
    conn.close()
    return df

# Streamlit 畫面
st.title("🐶 狗狗資料展示系統")

if st.button("載入 DOG_BREED 資料"):
    try:
        df = fetch_dog_breeds()
        st.success(f"成功載入 {len(df)} 筆資料")
        st.dataframe(df)
    except Exception as e:
        st.error(f"發生錯誤：{e}")
