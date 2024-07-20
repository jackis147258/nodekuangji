import requests
from bs4 import BeautifulSoup

# 目标页面URL
# url = 'https://coinmarketcap.com/dexscan/zh/polygon/0x2e6ee934c0bb2a8446c50acef58e9caa47a39dcd/'
url = 'https://ave.ai/token/0x4339e7c4d7c9495c704bc7818b2032f4b72c8dd9-polygon?from=Home'

# 发出请求
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 查找价格信息
# 查找价格信息
# 由于你提供的示例中包含价格信息的标签为 <span class="sc-d1ede7e3-0 hEkrmt base-text">
price_span = soup.find('span', class_='sc-d1ede7e3-0 hEkrmt base-text')

if price_span:
    price = price_span.get_text()
    print(f"AMT价格是: {price}")
else:
    print("未找到价格信息")
