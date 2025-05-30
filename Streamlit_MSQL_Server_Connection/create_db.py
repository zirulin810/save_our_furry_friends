import mysql.connector
import pandas as pd

# 1️⃣ 讀取 CSV
df = pd.read_csv("dogs.csv", encoding="latin1")
df.rename(columns={"Dogs Kind": "Dog_breed"}, inplace=True)

# 2️⃣ 連接 MySQL 並建立資料庫
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=""  # <--- 改成你的密碼
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS save_our_furry_friends")
cursor.execute("USE save_our_furry_friends")

# 清除舊的 DOG_BREED 資料表（如果存在）
cursor.execute("DROP TABLE IF EXISTS DOG_BREED")

# 3️⃣ 建立 DOG_BREED 資料表（簡化範例，只包含幾欄，實際可擴展）
cursor.execute("""
CREATE TABLE IF NOT EXISTS DOG_BREED (
    Dog_breed VARCHAR(100) PRIMARY KEY,
    Dog_breed_group VARCHAR(100),
    Height TEXT,
    Weight TEXT,
    Life_span TEXT,
    Detail_description_link TEXT
)
""")

# 4️⃣ 插入資料
rows_inserted = 0  # 用來計算成功插入的行數
for _, row in df.iterrows():
    sql = """
    INSERT INTO DOG_BREED (Dog_breed, Dog_breed_group, Height, Weight, Life_span, Detail_description_link)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    val = (
        row["Dog_breed"],
        row.get("Dog Breed Group", None),
        row.get("Height", None),
        row.get("Weight", None),
        row.get("Life Span", None),
        row.get("Detailed Description Link", None)
    )
    try:
        cursor.execute(sql, val)
        rows_inserted += 1  # 每成功插入一筆就加一
    except mysql.connector.errors.IntegrityError:
        pass  # 若重複主鍵就跳過

conn.commit()
print("✅ 匯入完成，共匯入：", rows_inserted, "筆")
cursor.close()
conn.close()
