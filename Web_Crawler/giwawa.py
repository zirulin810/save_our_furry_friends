import requests
from bs4 import BeautifulSoup
import pandas as pd

# 發送 HTTP 請求
url = "https://doghealth.east.org.tw/dogs/chihuahua/"
response = requests.get(url)

# 檢查是否連接成功
if response.status_code == 200:
    print("Successfully connected to the website.")
else:
    print(f"Failed to connect, status code: {response.status_code}")
    exit()

# 解析 HTML 內容
soup = BeautifulSoup(response.text, "html.parser")

# 找到所有 <div class="disease-item">
disease_items = soup.find_all("div", class_="disease-item")

# 建立資料清單
diseases = []
for item in disease_items:
    category = item.find("h4").text.strip()
    symptoms = item.find("p").text.strip()
    diseases.append({
        "Category": category,
        "Symptoms": symptoms
    })

print(diseases)