import streamlit as st

# 需要登入
def require_login():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("請先登入")
        st.stop()


# 初始化session_state
def state_initialization():
    st.session_state.page = 'start_page'
    st.session_state.ans_adaptability = []
    st.session_state.ans_info = []
    st.session_state.ans_area = []
    st.session_state.dog_result = []
    st.session_state.dog_result_index = 0

    