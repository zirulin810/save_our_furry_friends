import Streamlit_MSQL_Server_Connection.connect as connect
import streamlit as st
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

# session_state說明:
    # 1. ans_adaptability: 記錄[adaptability_questions]測驗選擇
    # 2. ans_info: 記錄[info_questions]測驗選擇
    # 3. ans_area: 記錄[area_questions]測驗選擇
    # 4. dog_result: 記錄"有匹配查詢結果時"的狗狗結果
    # 5. dog_result_index: 在查看"有匹配查詢結果"時的狗狗索引，

## 函式庫
# 初始化session_state
def state_initialization():
        st.session_state.page = 'start_page'
        st.session_state.ans_adaptability = []
        st.session_state.ans_info = []
        st.session_state.ans_area = []
        st.session_state.dog_result = []
        st.session_state.dog_result_index = 0

def close_connection():
    if 'conn' in st.session_state:
        st.session_state.cur.close()
        st.session_state.conn.close()

def degree_transform(val):
    if val < 3 and val > 0:
        return '低'
    elif val == 3:
        return '中'
    else:
        return '高'

# 確認是否登入
if 'logged_in' not in st.session_state or st.session_state.logged_in == False:
    st.warning("請先登入")
    st.stop()  # 停止載入頁面內容

# 登出功能按鍵
col1, col2 = st.columns([7, 1])
with col2:
    if st.button("登出"):
        state_initialization()
        st.session_state.logged_in = False
        st.switch_page("首頁.py")

## 問題設計
# 狗狗適應性問題
adaptability_questions = [
    {'question':'狗狗適應公寓的能力', 'key':'apartment'},
    {'question':'適合新手程度', 'key':'novice_owner'},
    {'question':'狗狗需要運動的程度','key':'exercise_need'},
    {'question':'狗狗易訓練程度', 'key':'easy_to_train'} 
]
# 狗狗資訊問題
info_questions = [
    {'question':'狗狗的顏色', 'key':'dog_breed_group', 'options':['黑色', '白色', '其他']},
    {'question':'狗狗的體型', 'key':'dog_size', 'options':[1, 2, 3, 4, 5]},
    {'question':'狗狗的年紀', 'key':'dog_age', 'options':['ADULT', 'CHILD']},
    {'question':'狗狗的性別', 'key':'dog_sex', 'options':['F', 'M']},
    {'question':'狗狗是否絕育', 'key':'sterilization', 'options':['是', '否']},
    {'question':'狗狗的智商', 'key':'dog_intelligence', 'options':[1, 2, 3, 4, 5]}
]
# 使用者問題
area_questions = [
    {'question':'您的所在地址', 'key':'user_address', 'options':['臺北市', '新北市', '桃園市', '臺南市', '基隆市', '臺中市', '新竹市', '新竹縣', '彰化縣', '南投縣', '嘉義市', '高雄市', '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '連江縣', '金門縣', '澎湖縣', '雲林縣', '苗栗縣']}
]

## CSS Style
st.markdown(
    """
    <style>
    .container {
        display: flex;
        flex-direction: column;
    }
    .top {
        height: 50%;
        background-color: lightcoral;
        padding: 10px;
    }
    .bottom {
        height: 50%;
        background-color: lightyellow;
        padding: 10px;
    }
    @keyframes breathing {
        0%   { transform: scale(1.4); }
        50%  { transform: scale(1.7); }
        100% { transform: scale(1.4); }
    }
    .breathing-text {
        color:red;
        animation: breathing 3s ease-in-out infinite;
    }
    </style>
    """
    ,True
)

# 確認連接資料庫
if 'conn' not in st.session_state:
    st.session_state.conn = connect.get_connection()
    st.session_state.cur = st.session_state.conn.cursor()

cursor = st.session_state.cur
conn = st.session_state.conn

## 頁面初始化
if 'page' not in st.session_state:
    state_initialization()

## 說明頁面
if st.session_state.page == 'start_page':
    
    #標題
    if 'user_name' in st.session_state:
        st.markdown(
            f"""
            <div style="font-size:36px; font-style: normal; font-weight: bold; white-space:nowrap;"> 
                <span style="color:orange">🐶狗狗測驗</span>
                <span style="color:white">- 找出你的夢中情狗</span>
            </div>
            <br>
            <div>
                <span style="font-size:24px;">歡迎</span>
                <span style="font-emphasis:filled; color:#FF9224; font-size:28px;">{st.session_state.user_name}</span>
            </div>
            <br>
            <div style="font-size:22px; font-style: normal; font-weight: normal">
                <span>接下來會有幾題測驗<br>幫助您選出最適合的狗狗類型<br></span>
            </div>
            <br>
            """
            , True)
    
    if st.button("下一頁"):
        st.session_state.page = 'stage1'
        st.rerun()

## 狗狗適應性問題
elif st.session_state.page == 'stage1':
    st.markdown(
        """
        <div style="font-size:36px; font-style: normal; font-weight: bold; white-space:nowrap;"> 
            <span style="color:white">Part1. 對狗狗</span><span style="color:orange">適應性</span><span style="color:white">的期望...</span>
        </div>
        <br>
        """
        , True
    )
    
    adaptability = []
    with st.container():
        for i in range(len(adaptability_questions)):
            st.markdown(f"""<div style="font-size:20px; font-weight:bold;">{i+1}. {adaptability_questions[i]['question']}</div>"""
                        , unsafe_allow_html=True)
            adaptability.append(st.slider("選擇分數", 1, 5, key = adaptability_questions[i]['key'],  label_visibility = 'hidden'))

    column1, column2= st.columns([7, 1])
    with column1:
        if st.button("⬅ 返回"):
            st.session_state.page = 'start_page'
            st.rerun()
    with column2:
        if st.button("下一頁"):
            st.session_state.page = 'stage2'
            st.session_state.ans_adaptability = adaptability
            st.rerun()


## 狗狗基本資訊問題
if st.session_state.page == 'stage2':
    st.markdown(
        """
        <div style="font-size:36px; font-style: normal; font-weight: bold; white-space:nowrap;"> 
            <span style="color:white">Part2. 對狗狗</span><span style="color:orange">基本資訊</span><span style="color:white">的選擇...</span>
        </div>
        <br>
        """
        , True
    )
    
    info = []
    with st.container():
        for i in range(len(info_questions)):
            st.markdown(f"""<div style="font-size:20px; font-weight:bold;">{i+1}.{info_questions[i]['question']}</div>"""
                    , unsafe_allow_html=True)
            info.append(st.radio("選擇題", info_questions[i]['options'], key = info_questions[i]['key'],  label_visibility = 'hidden', horizontal=True))
    
    column1, column2 = st.columns([7, 1])
    with column1:
        if st.button("⬅ 返回"):
            st.session_state.page = 'stage1'
            st.rerun()
    with column2:
        if st.button("下一頁"):
            st.session_state.page = 'stage3'
            st.session_state.ans_info = info
            st.rerun()

## 狗狗所在地區問題
if st.session_state.page == 'stage3':
    st.markdown(
        """
        <div style="font-size:36px; font-style: normal; font-weight: bold; white-space:nowrap;"> 
            <span style="color:white">Part3. 狗狗</span><span style="color:orange">所在地區</span><span style="color:white">的選擇...</span>
        </div>
        <br>
        """
        , True
    )
    area = st.selectbox("縣市", options=area_questions[0]['options'], key=area_questions[0]['key'])
    
    column1, column2 = st.columns([6, 1])
    with column1:
        if st.button("⬅ 返回"):
            st.session_state.page = 'stage2'
            st.rerun()
    with column2:
        if st.button("查詢結果"):
            st.session_state.page = 'stage4'
            st.session_state.ans_area = area
            
            query = """INSERT INTO user_test_record(user_name, loved_color, loved_size, 
                        loved_age, loved_gender, loved_sterilization, 
                        user_lived_city, apartment, rookie, exercise_need, 
                        easy_to_train, intelligence) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            params = (st.session_state.user_name, st.session_state.ans_info[0], st.session_state.ans_info[1], 
                      st.session_state.ans_info[2], st.session_state.ans_info[3], st.session_state.ans_info[4], 
                      st.session_state.ans_area[0], st.session_state.ans_adaptability[0], st.session_state.ans_adaptability[1], 
                      st.session_state.ans_adaptability[2], st.session_state.ans_adaptability[3], st.session_state.ans_info[5])
            
            cursor.execute(query, params=params)
            conn.commit()

            st.rerun()
    

## 結果頁面
if st.session_state.page == 'stage4':
    
    # 查詢匹配結果
    query = """
            SELECT A.dog_kind FROM dogs_adaptability A
            JOIN dog_kind_info I ON A.dog_kind = I.dog_kind
            JOIN dogs_training_ability T ON A.dog_kind = T.dog_kind
            WHERE A.apartment = %s 
            AND A.novice_owner = %s
            AND A.exercise_need = %s 
            AND T.easy_to_train = %s
            AND I.dog_size = %s
            AND T.intelligence = %s
            ;
        """
    params = (int(st.session_state.ans_adaptability[0]),
            int(st.session_state.ans_adaptability[1]),
            int(st.session_state.ans_adaptability[2]),
            int(st.session_state.ans_adaptability[3]),
            int(st.session_state.ans_info[1]),
            int(st.session_state.ans_info[5])
            )
    cursor.execute(query, params=params)
    result = cursor.fetchall()
    
    # 查無匹配狗狗
    if result == [ ]:
        st.markdown(
            """
            <style>
            .blinking {
                animation: blinker 2s linear infinite;
                color: red;
                font-size: 36px;
                font-weight: bold;
                text-align: center;
            }

            @keyframes blinker {
                50% { opacity: 0; }
            }
            </style>

            <p class="blinking">🚨 查無匹配狗狗qqq</p>
            """
            , True
        )
        
        df = pd.read_sql("SELECT A.dog_kind, apartment, novice_owner, exercise_need, easy_to_train, dog_size, intelligence FROM dogs_adaptability A JOIN dogs_training_ability T ON A.dog_kind = T.dog_kind JOIN dog_kind_info I ON A.dog_kind = I.dog_kind", conn)
        
        condition = []
        for i in range(len(st.session_state.ans_adaptability)):
            condition.append(int(st.session_state.ans_adaptability[i]))
        condition.append(int(st.session_state.ans_info[1]))
        condition.append(int(st.session_state.ans_info[5]))

        #相似度計算
        def compute_distance(row):
            dog_features = [row['apartment'], row['novice_owner'], row['exercise_need'], row['easy_to_train'], row['dog_size'], row['intelligence']]
            return np.linalg.norm(np.array(condition) - np.array(dog_features))
        
        df['distance'] = df.apply(compute_distance, axis=1)
        

        recommended_dog = df.sort_values(by = 'distance').head(3)

        if 'recommend_index' not in st.session_state:
            st.session_state.recommend_index = 0

        index = st.session_state.recommend_index
        query = """SELECT A.dog_kind, A.apartment, A.novice_owner, A.sensitivity, A.exercise_need,
                    T.intelligence, T.easy_to_train,
                    I.dog_breed_group, I.dog_size, I.lower_height, I.upper_height,
                    I.lower_weight, I.upper_weight, I.lower_life_span, I.upper_life_span,
                    I.more_detail_website, bark_tendency, shedding
                    FROM dogs_adaptability A 
                    JOIN dogs_training_ability T ON A.dog_kind = T.dog_kind 
                    JOIN dog_kind_info I ON A.dog_kind = I.dog_kind 
                    WHERE A.dog_kind = %s;"""
        params = (recommended_dog.iloc[index, 0], )
        df = pd.read_sql_query(query, conn, params=params)
        
        # 爬蟲->狗狗的照片
        url = df.loc[0, 'more_detail_website'] # more_detail_website
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")
        if images:
            img_url = images[0]['src']

        sens = degree_transform(df.loc[0, 'sensitivity'])
        bark = degree_transform(df.loc[0, 'bark_tendency'])
        shedding = degree_transform(df.loc[0, 'shedding'])

        #介面設計
        st.markdown(
            f"""
            <div style="font-size:36px; text-align: center; font-style: normal; font-weight: bold; white-space:nowrap;"> 
                <span style="color:white">為您推薦</span><span style="color:#7FFFD4">相似地夢中情狗...🐶</span>
            </div>
            <br>
            <div style= "text-align:center;">
                <img src="{img_url}" alt="{"錯誤"}" style="width:60%; border-radius:15px 50px; box-shadow:4px 4px 15px rgba(0,0,0,0.3);">
            </div>
            <br>
            <div class="container">
                <div class="top" style = "text-align:center; font-weight:normal; background-color:#fff3e0; padding:20px; border-radius:15px; border:5px solid orange; box-shadow:2px 2px 10px rgba(0,0,0,0.2); width: 100%; ">
                    <p style = "color:black; font-size:28px; font-family:Georgia, serif; text-shadow: 2px 2px 5px #8B008B;"><strong>{recommended_dog.iloc[index, 0]}</strong></p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">身高:&nbsp{df.loc[0, 'lower_height']}&nbsp公分&nbsp~&nbsp{df.loc[0, 'upper_height']}公分</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">體重:&nbsp{df.loc[0, 'lower_weight']}&nbsp公斤&nbsp~&nbsp{df.loc[0, 'upper_weight']}公斤</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">壽命:&nbsp{df.loc[0, 'lower_life_span']}&nbsp歲&nbsp~&nbsp{df.loc[0, 'upper_life_span']}歲</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">犬種:&nbsp{df.loc[0, 'dog_breed_group']}</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">詳細資訊: <a href="{url}" target="_blank">🔗點我看詳細資訊</a></p>
                </div>
                <br>
                <div class="bottom" style = "font-family:fantasy; text-align:center; background-color:#FFE4E1; padding:20px; border-radius:15px; border:5px solid #DC143C; box-shadow:2px 2px 10px rgba(0,0,0,0.2); width: 100%;">
                    <p class="breathing-text" style = "font-size:24px;">⚠️狗狗注意事項⚠️</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">敏感度:&nbsp{sens}</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">吠叫程度:&nbsp{bark}</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">掉毛程度:&nbsp{shedding}</p>
                </div>
            </div>
            <br>
        """
        , True
        )

        query = "SELECT category, symptom FROM dogs_disease WHERE dog_kind_EN = %s"
        params = (recommended_dog.iloc[index, 0], )
        cursor.execute(query, params=params)
        disease_result = cursor.fetchall()
        if disease_result != []:
            with st.expander("狗狗潛在疾病", icon="☠️"):
                df_disease = pd.DataFrame(disease_result)
                df_disease.columns = ['部位', '症狀']
                st.dataframe(df_disease, use_container_width=True)
            table = df_disease.to_html(index=False)
            

        data = {
            '':['你的選擇', '推薦狗狗結果'],
            '適應公寓程度':[st.session_state.ans_adaptability[0], df.loc[0, 'apartment']],
            '適合新手程度':[st.session_state.ans_adaptability[1], df.loc[0, 'novice_owner']],
            '狗狗需要運動程度':[st.session_state.ans_adaptability[2], df.loc[0, 'exercise_need']],
            '狗狗易訓練程度':[st.session_state.ans_adaptability[3], df.loc[0, 'easy_to_train']],
            '狗狗體型':[st.session_state.ans_info[1], df.loc[0, 'dog_size']],
            '狗狗智商':[st.session_state.ans_info[5], df.loc[0, 'intelligence']]
        }
        df_compare = pd.DataFrame(data).set_index('').T

        with st.expander("你的測驗選擇與推薦狗狗的分數......"):
            st.dataframe(df_compare, use_container_width=True)
            
        column1, column2, column3, column4, column5 = st.columns(5)
        with column1:
            if st.button("⬅ 上一隻", disabled = st.session_state.recommend_index == 0):
                st.session_state.recommend_index -= 1
                st.rerun()
        with column5:
            if st.button("⇨ 下一隻", disabled = st.session_state.recommend_index == 2):
                st.session_state.recommend_index += 1
                st.rerun()
        

    # 成功找到匹配狗狗
    else:
        if not st.session_state.dog_result:
            for r in result:
                query = """SELECT A.dog_kind, dog_breed_group, lower_height, 
                        upper_height, lower_weight, upper_weight, 
                        lower_life_span, upper_life_span, more_detail_website,
                        sensitivity, bark_tendency, shedding
                        FROM dog_kind_info I JOIN dogs_adaptability A ON I.dog_kind = A.dog_kind
                        WHERE A.dog_kind = %s"""
                params = (r[0], )
                cursor.execute(query, params)
                fetched = cursor.fetchone()
                if fetched:
                    st.session_state.dog_result.append(fetched)
        
        total = len(st.session_state.dog_result)
        idx = st.session_state.dog_result_index
        dog = st.session_state.dog_result[idx]
        
        # 爬蟲抓狗狗圖片
        url = dog[8]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")
        if images:
            img_url = images[0]['src']

        #敏感度轉換(顯示資訊時以'低'、'中'、'高'顯示)
        sens = degree_transform(dog[9])
        bark = degree_transform(dog[10])
        shedding = degree_transform(dog[11])

        #吠叫程度轉換

        st.markdown(
            f"""
            <div style="font-size:36px; text-align: center; font-style: normal; font-weight: bold; white-space:nowrap;"> 
                <span style="color:white">您的</span><span style="color:red">夢中情狗...🐶</span>
            </div>
            <br>
            <div style= "text-align:center;">
                <img src="{img_url}" alt="{dog[0]}" style="width:60%; border-radius:15px 50px; box-shadow:4px 4px 15px rgba(0,0,0,0.3);">
            </div>
            <br>
            <div class="container">
                <div class="top" style = "text-align:center; font-weight:normal; background-color:#fff3e0; padding:20px; border-radius:15px; border:5px solid orange; box-shadow:2px 2px 10px rgba(0,0,0,0.2); width: 100%; ">
                    <p style = "color:black; font-size:28px; font-family:Georgia, serif; text-shadow: 2px 2px 5px #8B008B;"><strong>{dog[0]}</strong></p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">犬種:&nbsp{dog[1]}</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">身高:&nbsp{dog[2]}&nbsp公分&nbsp~&nbsp{dog[3]}公分</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">體重:&nbsp{dog[4]}&nbsp公斤&nbsp~&nbsp{dog[5]}公斤</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">壽命:&nbsp{dog[6]}&nbsp歲&nbsp~&nbsp{dog[7]}歲</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">詳細資訊: <a href="{url}" target="_blank">🔗點我看詳細資訊</a></p>
                </div>
                <br>
                <div class="bottom" style = "text-align:center; background-color:#FFE4E1; padding:20px; border-radius:15px; border:5px solid #DC143C; box-shadow:2px 2px 10px rgba(0,0,0,0.2); width: 100%;">
                    <p class="breathing-text" style = "color:black; font-size:28px; font-family:fantasy; color">⚠️狗狗注意事項⚠️</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">敏感度:&nbsp{sens}</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">吠叫程度:&nbsp{bark}</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">掉毛程度:&nbsp{shedding}</p>
                </div>
            </div>
            <br>
        """
        , True
        )
        query = "SELECT category, symptom FROM dogs_disease WHERE dog_kind_EN = %s"
        params = (dog[0], )
        cursor.execute(query, params=params)
        disease_result = cursor.fetchall()
        if disease_result != []:
            with st.expander("狗狗潛在疾病", icon="☠️"):
                df_disease = pd.DataFrame(disease_result)
                df_disease.columns = ['部位', '症狀']
                st.dataframe(df_disease, use_container_width=True)
            table = df_disease.to_html(index=False)

        with st.expander("你的測驗選擇......"):
            st.write(f"適應公寓程度: {st.session_state.ans_adaptability[0]}")
            st.write(f"適合新手程度: {st.session_state.ans_adaptability[1]}")
            st.write(f"狗狗需要運動程度: {st.session_state.ans_adaptability[2]}")
            st.write(f"狗狗易訓練程度: {st.session_state.ans_adaptability[3]}")
            st.write(f"狗狗體型: {st.session_state.ans_info[1]}")
            st.write(f"狗狗智商: {st.session_state.ans_info[5]}")
        

        column1, column2, column3, column4, column5 = st.columns(5)
        with column1:
            if st.button("⬅ 上一隻", disabled = idx == 0):
                st.session_state.dog_result_index -= 1
                st.rerun()
        with column5:
            if st.button("⇨ 下一隻", disabled = idx == total - 1):
                st.session_state.dog_result_index += 1
                st.rerun()
    
    ## 連接收容所功能
    if st.button("前往查看收容所狗狗"):
        st.switch_page("pages/2_收養配對.py")
    if st.button("重新測驗"):
        state_initialization()
        st.rerun()

    ## 關閉資料庫    
    # if st.button("結束"):
    #     close_connection()


