import streamlit as st
import requests
import pandas as pd
import datetime

st.set_page_config(page_title="基金助手进阶版", layout="centered")
st.title("📈 基金实时查询 + 业绩走势 + 新闻")

code = st.text_input("请输入基金代码（例如 005827）", "005827")

# ========== 插件：获取每日净值数据 ==========
def get_latest_nav(code):
    try:
        url = f"https://fundgz.1234567.com.cn/js/{code}.js"
        resp = requests.get(url)
        text = resp.text
        # 解析前端返回的 JS 数据
        name = text.split('name":"')[1].split('"')[0]
        nav = text.split('dwjz":"')[1].split('"')[0]
        growth = text.split('gszzl":"')[1].split('"')[0]
        date = text.split('gztime":"')[1].split('"')[0]
        return {"name":name, "nav":nav, "growth":growth, "date":date}
    except Exception as e:
        return None

# ========== 简单历史走势抓取 ==========
def get_history_nav(code, days=30):
    records = []
    base_date = datetime.date.today()
    for i in range(days):
        d = base_date - datetime.timedelta(days=i+1)
        d_str = d.strftime("%Y-%m-%d")
        # fundgz 不提供历史，但我们可以通过循环验算可用免费接口/你可以取消
        try:
            url = f"https://fundgz.1234567.com.cn/js/{code}.js?date={d_str}"
            resp = requests.get(url)
            text = resp.text
            if "nav" in text:
                nav = text.split('dwjz":"')[1].split('"')[0]
                records.append({"date": d_str, "nav": float(nav)})
        except:
            pass
    df = pd.DataFrame(records)
    return df[::-1]  # 倒序

# ========== 新闻抓取 ==========
def get_news(keyword="基金"):
    # 用 Google News RSS
    rss_url = f"https://news.google.com/rss/search?q={keyword}"
    feed = feedparser.parse(rss_url)
    items = []
    for entry in feed.entries[:10]:
        items.append({"title":entry.title, "link":entry.link})
    return items

# 查询按钮
if st.button("查询"):
    data = get_latest_nav(code)
    if not data:
        st.error("基金代码无效或获取失败")
    else:
        st.success(f"基金名称：{data['name']}")
        st.write(f"📅 日期：{data['date']}")
        st.write(f"💰 最新净值：{data['nav']}")
        st.write(f"📊 预估涨跌幅：{data['growth']}%")

        # 历史净值图
        df_hist = get_history_nav(code, days=30)
        if not df_hist.empty:
            st.line_chart(df_hist.set_index("date")["nav"])
        else:
            st.write("暂无历史数据（免费接口限制）")

        # 新闻
        st.write("📰 相关新闻（免费 Google News RSS）：")
        news = get_news_rss(data['name'])
        for item in news:
            st.markdown(f"- [{item['title']}]({item['link']})")

st.write("---")
st.write("📌 提示：此页面使用免费数据抓取，数据更新可能延迟。")
import requests
import xml.etree.ElementTree as ET

def get_news_rss(keyword="基金"):
    url = f"https://news.google.com/rss/search?q={keyword}"
    resp = requests.get(url)
    root = ET.fromstring(resp.content)
    news_items = []
    for item in root.findall(".//item")[:10]:
        title = item.find("title").text
        link = item.find("link").text
        news_items.append({"title": title, "link": link})
    return news_items