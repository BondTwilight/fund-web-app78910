import requests
from datetime import datetime

# ⚠ 这里先不填 API KEY，后面我会告诉你最简单的替代方案
def get_fund_data(code):
    url = f"https://fundgz.1234567.com.cn/js/{code}.js"
    resp = requests.get(url)
    text = resp.text

    # 解析数据（新手不用懂）
    name = text.split('name":"')[1].split('"')[0]
    nav = text.split('dwjz":"')[1].split('"')[0]
    growth = text.split('gszzl":"')[1].split('"')[0]
    date = text.split('gztime":"')[1].split('"')[0]

    return {
        "name": name,
        "nav": nav,
        "growth": growth,
        "date": date
    }