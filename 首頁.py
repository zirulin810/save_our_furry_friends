import streamlit as st
import Streamlit_MSQL_Server_Connection.connect as connect

st.title("🐾 拯救毛小孩")
# st.write("請使用左側側邊欄選擇頁面")

if 'conn' not in st.session_state:
    st.session_state.conn = connect.get_connection()
    st.session_state.cur = st.session_state.conn.cursor()

if 'user_state' not in st.session_state:
    st.session_state.user_state = 'new'

st.warning("如無帳號請先註冊", icon="⚠️")
username = st.text_input("使用者名稱:")

col1, col2 = st.columns([9, 1])
push_btn = 0
with col1:
    if st.button("登入"):
        push_btn = 1        
with col2:
    if st.button("註冊"):
        push_btn = 2

# 登入處理
if push_btn == 1:
    query = "SELECT * FROM user_test_record WHERE user_name = %s"
    params = (username,)
    cursor = st.session_state.cur
    cursor.execute(query, params=params)
    result = cursor.fetchall()

    if result == []:
        st.error("查無此使用者! 請先註冊", icon="🚨")
        st.session_state.logged_in = False
    else:
        st.success("登入成功", icon="✅")
        st.session_state.logged_in = True
        st.session_state.user_name = username
        st.session_state.user_state = 'old'
        st.switch_page("pages/1_尋找你的夢中情狗.py")

#註冊處理
elif push_btn == 2:
    query = "SELECT EXISTS (SELECT * FROM user_test_record WHERE user_name = %s);"
    params = (username,)
    cursor = st.session_state.cur
    cursor.execute(query, params=params)
    result = cursor.fetchone()

    if result[0] == True:
        st.error("使用者已存在", icon="🚨")
    else:
        st.session_state.logged_in = True
        st.session_state.user_name = username
        st.switch_page("pages/1_尋找你的夢中情狗.py")
            
            
            
# st.markdown(
#     """
#     <style>
#     .container {
#         display: flex;
#         height: 300px;
#         border: 2px solid #ccc;
#     }
#     .left-column{
#         width: 30%;
#         background-color:#FFF4C1;
#         padding: 20px;
#     }
#     .right-column{
#         width: 70%;
#         background-color: #E1C4C4;
#         padding: 20px;
#     }
#     </style>
#     <div class="container">
#     <div class="left-column" style="color:black">左欄</div>
#     <div class="right-column">右欄</div>
#     </div>
#     """ 
#     , unsafe_allow_html=True
# )