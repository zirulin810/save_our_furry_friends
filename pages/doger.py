import streamlit as st
import pandas as pd

# 問題與欄位
questions = [
    {"question": "你希望狗狗多適應公寓生活？", "options": [1, 2, 3, 4, 5], "column": "Adapts Well To Apartment Living"},
    {"question": "你喜歡狗狗的品種？", "options": ["Mixed Breed Dogs", "Companion Dogs", "Hound Dogs", "Terrier Dogs", "Working Dogs"], "column": "Dog Breed Group"},
    {"question": "你希望狗狗的聰明程度？", "options": [1, 2, 3, 4, 5], "column": "Intelligence"}
]

# 初始化狀態
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.answers = {}

# 載入資料
@st.cache_data
def load_data():
    return pd.read_csv("dogs.csv",  encoding="cp1252")
    #return pd.read_csv("dogs_example.csv")
data = load_data()

# 顯示目前題目
current_index = st.session_state.question_index
if current_index < len(questions):
    q = questions[current_index]
    st.markdown(
    "<h1 style='text-align: left;'>🐶 選擇你的夢中情狗</h1>",
    unsafe_allow_html=True)
    st.write(f"#### 第 {current_index + 1} 題")
    selected = st.radio(q['question'], q["options"], key=f"q{current_index}")

    col1, col2 = st.columns(2)
    with col1:
        if current_index > 0:
            if st.button("上一題"):
                st.session_state.question_index -= 1
                st.rerun()

    with col2:
        if st.button("下一題" if current_index < len(questions) - 1 else "查看結果"):
            col_name = q["column"]
            st.session_state.answers[col_name] = selected
            st.session_state.question_index += 1
            st.rerun()
    

else:
    st.title("🎉你的夢中情狗是...")

    # 根據題目選擇篩選資料
    filtered = data.copy()
    for key, val in st.session_state.answers.items():
        filtered = filtered[filtered[key] == val]

    if not filtered.empty:
        dog = filtered.sample(1).iloc[0]
        
        try:
            st.image(dog["Image_url"], use_column_width=True)
        except:
            st.warning("找不到圖片")

        with st.container():
            st.markdown(f"""
            ---

            ### 🐾 **你的夢中情狗是： {dog['Name']}**

            - **品種類別**： *<b style = "color:red; font-size:20px">{dog['Dog Breed Group']}</b>*  
            - **適應公寓程度**：{'★' * int(dog['Adapts Well To Apartment Living'])}  
            - **聰明程度**：{'🧠' * int(dog['Intelligence'])}  

            🔗 **更多資訊**：[前往狗狗資訊網頁]({dog['Detailed Description Link']})

            ---
            """, unsafe_allow_html=True)

    else:
        st.warning("抱歉，找不到完全符合的狗狗品種喔qqqqq")

    # 顯示使用者選項
    with st.expander("你的選擇回顧"):
        for k, v in st.session_state.answers.items():
            st.write(f"🔹 {k}: {v}")

    col3, col4 = st.columns(2)
    with col3:
        # 重新開始
        if st.button("重新測驗"):
            del st.session_state.question_index
            del st.session_state.answers
            st.rerun()
    
    with col4:
        if st.button("前往查看收容所資訊"):
            st.write("## 等討論過後再看看怎麼接在一起")
