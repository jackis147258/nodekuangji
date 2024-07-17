import requests

# 设置API密钥
api_key = 'c86ad6d1-d509-4c15-b707-b293e0db9c59'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

# 查找合约地址相关信息的URL
url_info = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
parameters_info = {
    'address': '0x2e6ee934c0bb2a8446c50acef58e9caa47a39dcd'
}

# 发出请求获取合约地址相关信息
response_info = requests.get(url_info, headers=headers, params=parameters_info)
data_info = response_info.json()

# 获取token的symbol
token_symbol = list(data_info['data'].keys())[0]

# 获取token价格的URL
url_price = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters_price = {
    'symbol': token_symbol,
}

# 发出请求获取token价格
response_price = requests.get(url_price, headers=headers, params=parameters_price)
data_price = response_price.json()

# 获取并打印价格
price = data_price['data'][token_symbol]['quote']['USD']['price']
print(f"Token {token_symbol} 的最新价格是: ${price}")


# import requests

# # 设置API密钥
# api_key = 'c86ad6d1-d509-4c15-b707-b293e0db9c59'
# headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY': api_key,
# }

# # 设置请求URL
# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
# parameters = {
#     'symbol': 'MATIC',
# }

# # 发出请求
# response = requests.get(url, headers=headers, params=parameters)
# data = response.json()

# # 获取并打印Polygon (MATIC)的最新价格
# price = data['data']['MATIC']['quote']['USD']['price']
# print(f"Polygon (MATIC) 的最新价格是: ${price}")
