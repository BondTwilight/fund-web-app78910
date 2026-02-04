import streamlit as st
from fund_data import get_fund_data

st.set_page_config(page_title="基金助手", layout="centered")

st.title("📈 我的基金助手")

code = st.text_input("请输入基金代码（例如 005827）", "005827")

if st.button("查询"):
    try:
        data = get_fund_data(code)
        st.success(f"基金名称：{data['name']}")
        st.write(f"📅 时间：{data['date']}")
        st.write(f"💰 最新净值：{data['nav']}")
        st.write(f"📊 预估涨跌：{data['growth']} %")
    except:
        st.error("基金代码有误，请重新输入")