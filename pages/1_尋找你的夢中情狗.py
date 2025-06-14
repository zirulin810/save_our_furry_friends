import Streamlit_MSQL_Server_Connection.connect as connect
import streamlit as st
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

if 'logged_in' not in st.session_state or st.session_state.logged_in == False:
    st.warning("請先登入")
    st.stop()  # 停止載入頁面內容

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
user_questions = [
    {'question':'您的所在地址', 'key':'user_address', 'options':['臺北市', '新北市', '桃園市', '臺南市', '基隆市', '臺中市', '新竹市', '新竹縣', '彰化縣', '南投縣', '嘉義市', '高雄市', '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '連江縣', '金門縣', '澎湖縣', '雲林縣', '苗栗縣']}
]

if 'conn' not in st.session_state:
    st.session_state.conn = connect.get_connection()
    st.session_state.cur = st.session_state.conn.cursor()

## 初始化session_state
if 'page' not in st.session_state:
    st.session_state.page = 'start_page'
    st.session_state.ans_adaptability = []
    st.session_state.ans_info = []
    st.session_state.dog_result = []
    st.session_state.dog_result_index = 0

def close_connection():
    if 'conn' in st.session_state:
        st.session_state.cur.close()
        st.session_state.conn.close()


## 說明頁面
if st.session_state.page == 'start_page':
    # 新用戶須先完成第一次測驗才會有紀錄
    if st.session_state.user_state == 'new':
        st.success(f"歡迎{st.session_state.user_name}! 接下來請完成首次狗狗測驗才能成功註冊喔!")
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
                <span style="font-emphasis:filled; color:#FF2D2D; font-size:28px;">{st.session_state.user_name}</span>
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
            <span style="color:white">Part1. 對狗狗</span>
            <span style="color:orange">適應性</span>
            <span style="color:white">的期望...</span>
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

    column1, column2, column3 = st.columns(3)
    with column1:
        if st.button("⬅ 返回"):
            st.session_state.page = 'start_page'
            st.rerun()
    with column3:
        if st.button("下一頁"):
            st.session_state.page = 'stage2'
            st.session_state.ans_adaptability = adaptability
            st.rerun()


## 狗狗基本資訊問題
if st.session_state.page == 'stage2':
    st.markdown(
        """
        <div style="font-size:36px; font-style: normal; font-weight: bold; white-space:nowrap;"> 
            <span style="color:white">Part2. 對狗狗</span>
            <span style="color:orange">基本資訊</span>
            <span style="color:white">的選擇...</span>
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
    
    column1, column2, column3 = st.columns(3)
    with column1:
        if st.button("⬅ 返回"):
            st.session_state.page = 'stage1'
            st.rerun()
    with column3:
        if st.button("下一頁"):
            st.session_state.page = 'stage3'
            st.session_state.ans_info = info
            st.rerun()

## 結果頁面
if st.session_state.page == 'stage3':
    
    query = """
            SELECT A.dog_kind FROM dogs_adaptability A
            JOIN dog_kind_info I ON A.dog_kind = I.dog_kind
            JOIN dogs_training_ability T ON A.dog_kind = T.dog_kind
            WHERE A.apartment = %s 
            AND A.novice_owner = %s
            AND A.exercise_need = %s 
            AND T.easy_to_train = %s
            AND I.dog_size = %s
            ;
        """
    params = (int(st.session_state.ans_adaptability[0]),
            int(st.session_state.ans_adaptability[1]),
            int(st.session_state.ans_adaptability[2]),
            int(st.session_state.ans_adaptability[3]),
            int(st.session_state.ans_info[1]))
    

    st.session_state.cur.execute(query, params=params)
    result = st.session_state.cur.fetchall()
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
        df = pd.read_sql("SELECT A.dog_kind, apartment, novice_owner, exercise_need, easy_to_train FROM dogs_adaptability A JOIN dogs_training_ability T ON A.dog_kind = T.dog_kind", st.session_state.conn)
        
        #相似度計算
        def compute_distance(row):
            dog_features = [row['apartment'], row['novice_owner'], row['exercise_need'], row['easy_to_train']]
            return np.linalg.norm(np.array(st.session_state.ans_adaptability) - np.array(dog_features))
        
        df['distance'] = df.apply(compute_distance, axis=1)

        recommended_dog = df.sort_values(by = 'distance').head(3)

        if 'recommend_index' not in st.session_state:
            st.session_state.recommend_index = 0
        index = st.session_state.recommend_index
        query = """SELECT A.dog_kind, A.apartment, A.novice_owner, A.sensitivity, A.exercise_need,
                    T.intelligence, T.easy_to_train,
                    I.dog_breed_group, I.dog_size, I.lower_height, I.upper_height,
                    I.lower_weight, I.upper_weight, I.lower_life_span, I.upper_life_span,
                    I.more_detail_website FROM dogs_adaptability A 
                    JOIN dogs_training_ability T ON A.dog_kind = T.dog_kind 
                    JOIN dog_kind_info I ON A.dog_kind = I.dog_kind 
                    WHERE A.dog_kind = %s;"""
        params = (recommended_dog.iloc[index, 0], )
        df = pd.read_sql_query(query, st.session_state.conn, params=params)
        url = df.loc[0, 'more_detail_website'] # more_detail_website
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")
        if images:
            img_url = images[0]['src']

        #介面設計
        st.markdown(
            """
            <style>
            
            .left-column{
                width: 30%;
                background-color:#FFF4C1;
                padding: 20px;
            }
            .right-column{
                width: 70%;
                background-color: #E1C4C4;
                padding: 20px;
            }
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
            f"""
            
            <div style="font-size:36px; text-align: center; font-style: normal; font-weight: bold; white-space:nowrap;"> 
                <span style="color:white">為您推薦</span>
                <span style="color:#7FFFD4">相似地夢中情狗...🐶</span>
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
                <div class="bottom" style = "text-align:center; background-color:#FFE4E1; padding:20px; border-radius:15px; border:5px solid #DC143C; box-shadow:2px 2px 10px rgba(0,0,0,0.2); width: 100%;">
                    <p class="breathing-text" style = "color:black; font-size:28px; font-family:fantasy; color">⚠️狗狗注意事項⚠️</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">敏感度:&nbsp{df.loc[0, 'lower_height']}&nbsp公分&nbsp~&nbsp{df.loc[0, 'upper_height']}公分</p>
                    <p style = "color:black; font-size:22px; font-family:fantasy;">:&nbsp{df.loc[0, 'lower_weight']}&nbsp公斤&nbsp~&nbsp{df.loc[0, 'upper_weight']}公斤</p>  
                </div>
            </div>
            <br>
        """
        , True
        )
        


    else:
        if not st.session_state.dog_result:
            for r in result:
                query = f"""SELECT dog_kind, height, weight, life_span, more_detail_website 
                        FROM dog_kind_info WHERE dog_kind = '{r[0]}'"""
                st.session_state.cur.execute(query)
                fetched = st.session_state.cur.fetchone()
                if fetched:
                    st.session_state.dog_result.append(fetched)
        
        total = len(st.session_state.dog_result)
        idx = st.session_state.dog_result_index
        dog = st.session_state.dog_result[idx]
        url = dog[4]
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")
        
        if images:
            img_url = images[0]['src']

        st.markdown(
            f"""
            <div style="font-size:36px; text-align: center; font-style: normal; font-weight: bold; white-space:nowrap;"> 
                <span style="color:white">您的</span>
                <span style="color:red">夢中情狗...🐶</span>
            </div>
            <br>
            <div style= "text-align:center;">
            <img src="{img_url}" alt="{dog[0]}" style="width:60%; border-radius:15px 50px; box-shadow:4px 4px 15px rgba(0,0,0,0.3);">
            </div>
            <br>
            <div style = "text-align:center; font-weight:normal; background-color:#fff3e0; padding:20px; border-radius:15px; border:5px solid orange; box-shadow:2px 2px 10px rgba(0,0,0,0.2); width: 100%;">
                <p style = "color:black; font-size:28px; font-family:Georgia, serif; text-shadow: 2px 2px 5px red;"><strong>{dog[0]}</strong></p>
                <p style = "color:black; font-size:22px; font-family:fantasy;">身高: {dog[1]}</p>
                <p style = "color:black; font-size:22px; font-family:fantasy;">體重: {dog[2]}</p>
                <p style = "color:black; font-size:22px; font-family:fantasy;">壽命: {dog[3]}</p>
                <p style = "color:black; font-size:22px; font-family:fantasy;">詳細資訊: <a href="{dog[4]}" target="_blank">🔗點我看詳細資訊</a></p>
            </div>
            <br>
        """
        , True
        )
        column1, column2, column3, column4, column5 = st.columns(5)
        with column1:
            if st.button("⬅ 上一隻", disabled = idx == 0):
                st.session_state.dog_result_index -= 1
                st.rerun()
        with column5:
            if st.button("⇨ 下一隻", disabled = idx == total - 1):
                st.session_state.dog_result_index += 1
                st.rerun()
        
        if st.button("結束"):
            close_connection()


