import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv

# 載入環境檔
dotenv_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path)

# 連接資料庫
def get_connection():
    conn = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            database = os.getenv("DB_NAME")
        )
    
    return conn