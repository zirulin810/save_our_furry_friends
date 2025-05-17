import pandas as pd


# 讀取資料
file_path = 'COA_OpenData.csv'
df = pd.read_csv(file_path)

# # 篩選出 animal_kind 是 "狗" 的資料
# dog_df = df[df['animal_kind'] == '狗']

# # 新增自訂的收容所編號
# # dog_df = dog_df.reset_index(drop=True)
# # dog_df['shelter_id'] = dog_df.index + 1

# # 從地址中擷取縣市資訊
# dog_df['city'] = dog_df['shelter_address'].str[:3]

# # 篩選出所需的欄位
# result_df = dog_df[['animal_shelter_pkid', 'city', 'shelter_name', 'shelter_address', 'shelter_tel']]

# # 顯示結果
# print(result_df.head())   # 顯示前五筆

# # 匯出成 CSV 檔案
# result_df.to_csv('Shelter_Dogs_Data.csv', index=False, encoding='utf-8-sig')


# 篩選出狗的資料
dog_df = df[df['animal_kind'] == '狗']

# 提取所需欄位
result_df = dog_df[['animal_shelter_pkid', 'shelter_name', 'shelter_address', 'shelter_tel']].drop_duplicates()

# 增加縣市欄位，從地址中擷取出來
result_df['county'] = result_df['shelter_address'].str[:3]

# 排序
result_df = result_df.sort_values(by='animal_shelter_pkid').reset_index(drop=True)

# 顯示結果
print(result_df.head())   # 顯示前五筆

# 匯出成 CSV 檔案
result_df.to_csv('Shelter_Dogs_Data.csv', index=False, encoding='utf-8-sig')