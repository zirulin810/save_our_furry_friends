import pandas as pd

# 讀取已經建立好的CSV檔案
df = pd.read_csv("dog_health_diseases_cleaned.csv", encoding="utf-8-sig")


# 先將 "迷你、玩具貴賓犬" 的品種名稱標準化為 "貴賓犬"
df["Dog Breed"] = df["Dog Breed"].replace("迷你、玩具貴賓犬", "貴賓犬")

# 中文品種名稱對應的英文翻譯（可依需要擴充）
breed_translation = {
    "吉娃娃": "Chihuahua",
    "臘腸狗": "Dachshund",
    "黃金獵犬": "Golden Retriever",
    "鬆獅犬": "Chow Chow",
    "貴賓狗": "Poodle",
    "拉布拉多": "Labrador Retriever",
    "邊境牧羊犬": "Border Collie",
    "米格魯": "Beagle",
    "哈士奇": "Siberian Husky",
    "博美犬": "Pomeranian",
    "柴犬": "Shiba Inu",
    "馬爾濟斯": "Maltese",
    "西施犬": "Shih Tzu",
    "約克夏": "Yorkshire Terrier",
    "巴哥犬": "Pug",
    "可卡犬": "Cocker Spaniel",
    "牛頭梗": "Bull Terrier",
    "杜賓犬": "Doberman Pinscher",
    "羅威納": "Rottweiler",
    "德國狼犬": "German Shepherd",
    "拳師犬": "Boxer",
    "大麥町": "Dalmatian",
    "雪納瑞": "Schnauzer",
    "聖伯納犬": "Saint Bernard",
    "阿富汗獵犬": "Afghan Hound",
    "蝴蝶犬": "Papillon",
    "北京犬": "Pekingese",
    "比熊犬": "Bichon Frise",
    "貴賓犬": "Poodle",
    "迷你雪納瑞": "Miniature Schnauzer",
    "查理士小獵犬": "Cavalier King Charles Spaniel",
    "西高地白㹴": "West Highland White Terrier",
    "臘腸犬": "Dachshund",
    "法國鬥牛犬": "French Bulldog",
    "威爾斯柯基犬": "Welsh Corgi",
    "喜樂蒂牧羊犬": "Shetland Sheepdog",
    "英國鬥牛犬": "English Bulldog",
    "薩摩耶": "Samoyed",
    "拉不拉多": "Labrador Retriever",
    "大白熊犬": "Great Pyrenees"
}

# 加上翻譯欄位
df["Breed (EN)"] = df["Dog Breed"].map(breed_translation).fillna("")

# 儲存為新的CSV
output_path = "dog_health_diseases_with_english.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

# 顯示檔案路徑
output_path
