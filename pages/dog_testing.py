import connect
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

## 問題設計
# 狗狗適應性問題
adaptability_questions = [
    {'question':'狗狗適應公寓的能力', 'key':'apartment'},
    {'question':'狗狗的敏感度', 'key':'sensitivity'},
    {'question':'狗狗需要運動的程度','key':'exercise_need'},
    {'question':'適合新手程度', 'key':'novice_owner'}
]
# 狗狗資訊問題
info_questions = [
    {'question':'狗狗的種類', 'key':'dog_breed_group', 'options':['混合犬','伴侶犬','獵犬','梗類犬','工作犬','牧羊犬','其他']},
    {'question':'狗狗的體型', 'key':'dog_size', 'options':[1, 2, 3, 4, 5]}
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
    #標題
    st.markdown(
        """
        <div style="font-size:36px; font-style: normal; font-weight: bold; white-space:nowrap;"> 
            <span style="color:orange">🐶狗狗測驗</span>
            <span style="color:white">- 找出你的夢中情狗</span>
        </div>
        <div style="font-size:18px; font-style: normal; font-weight: normal">
            <p>接下來會有幾題測驗<br>幫助您選出最適合的狗狗類型</p>
        </div>
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
        for i in range(4):
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
        for i in range(2):
            st.markdown(f"""<div style="font-size:20px; font-weight:bold;">{i+1}.{info_questions[i]['question']}</div>"""
                    , unsafe_allow_html=True)
            info.append(st.radio("選擇題", info_questions[i]['options'], key = info_questions[i]['key'],  label_visibility = 'hidden'))
    
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
    query = f"SELECT dog_kind FROM dogs_adaptability WHERE apartment = {int(st.session_state.ans_adaptability[0])} AND sensitivity = {int(st.session_state.ans_adaptability[1])} AND exercise_need = {int(st.session_state.ans_adaptability[2])} AND novice_owner = {int(st.session_state.ans_adaptability[3])};"

    st.session_state.cur.execute(query)
    result = st.session_state.cur.fetchall()
    if result == [ ]:
        st.write("查無狗狗")
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

