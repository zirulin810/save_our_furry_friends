import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def clean_symptom(symptom):
    symptom = re.sub(r'\[\d+\](, )?', '', symptom)  # 移除 [n] 和可能的逗號+空格
    symptom = re.sub(r'^\"|\"$', '', symptom)       # 移除前後引號
    symptom = re.sub(r',+', ',', symptom)           # 移除多餘逗號
    symptom = symptom.strip(',').strip()            # 移除開頭結尾的逗號
    return symptom

# 主頁面 URL
base_url = "https://doghealth.east.org.tw/purebred-dogs-genetic-diseases/"
response = requests.get(base_url)

# 檢查是否連接成功
if response.status_code == 200:
    print("連接成功！正在擷取資料...")
else:
    print(f"連接失敗，狀態碼：{response.status_code}")
    exit()

# 解析 HTML
soup = BeautifulSoup(response.text, "html.parser")

# 取得所有狗品種與連結
dog_links = []
for item in soup.find_all("h4", class_="entry-title"):
    link = item.find("a")
    if link:
        dog_links.append({
            "breed": link.text.strip(),
            "url": link['href']
        })

# 顯示找到的連結
print(f"共找到 {len(dog_links)} 隻狗的健康資料。")

# 初始化 DataFrame
all_diseases = []

# 遍歷所有狗的頁面
for dog in dog_links:
    dog_name = dog["breed"]
    dog_url = dog["url"]
    print(f"正在抓取 {dog_name} 的資料...")

    try:
        # 進入狗的詳細頁面
        dog_response = requests.get(dog_url)
        dog_soup = BeautifulSoup(dog_response.text, "html.parser")
        
        # 找到所有疾病資訊
        disease_items = dog_soup.find_all("div", class_="disease-item")
        for item in disease_items:
            category = item.find("h4").text.strip() if item.find("h4") else ""
            symptoms = item.find("p").text.strip() if item.find("p") else ""
            
            # 分割症狀並逐一新增
            symptom_list = symptoms.split("、")
            for symptom in symptom_list:
                clean_text = clean_symptom(symptom)
                if clean_text:  # 過濾掉空字串
                    all_diseases.append({
                        "Dog Breed": dog_name,
                        "Category": category,
                        "Symptom": clean_text
                    })
    except Exception as e:
        print(f"Failed to fetch {dog_name}: {e}")

# 轉換成 DataFrame 顯示
df = pd.DataFrame(all_diseases)
df.to_csv("dog_health_diseases_cleaned.csv", index=False, encoding='utf-8-sig')
print("資料已儲存到 dog_health_diseases_cleaned.csv")
