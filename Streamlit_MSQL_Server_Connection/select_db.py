import mysql.connector
import pandas as pd

# 建立連線（請改成你自己的資料庫密碼）
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",  # <--- 改成你的密碼
    database="save_our_furry_friends"
)

# 查詢 DOG_BREED 資料表
query = "SELECT * FROM DOG_BREED"
df = pd.read_sql(query, conn)

# 顯示前幾筆
print(df.head())

# 若你要顯示全部，也可以寫成：
# print(df.to_string())

conn.close()
