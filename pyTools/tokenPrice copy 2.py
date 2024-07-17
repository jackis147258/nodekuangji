import requests

# 设置API密钥
api_key = 'c86ad6d1-d509-4c15-b707-b293e0db9c59'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

# 目标合约地址
contract_address = '0x4339e7C4D7C9495c704BC7818b2032F4b72c8dD9'

# 查找合约地址相关信息的URL
url_info = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
parameters_info = {
    'address': contract_address,
}

# 发出请求获取合约地址相关信息
response_info = requests.get(url_info, headers=headers, params=parameters_info)
data_info = response_info.json()

# 打印返回的JSON响应以便调试
print("Info response JSON:", data_info)

# 检查是否存在'data'字段
if 'data' in data_info:
    token_symbol = list(data_info['data'].keys())[0]
    print(f"Token symbol: {token_symbol}")

    # 获取token价格的URL
    url_price = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters_price = {
        'symbol': token_symbol,
    }

    # 发出请求获取token价格
    response_price = requests.get(url_price, headers=headers, params=parameters_price)
    data_price = response_price.json()

    # 打印返回的JSON响应以便调试
    print("Price response JSON:", data_price)

    # 检查是否存在价格信息
    if 'data' in data_price and token_symbol in data_price['data']:
        price = data_price['data'][token_symbol]['quote']['USD']['price']
        print(f"Token {token_symbol} 的最新价格是: ${price}")
    else:
        print("无法获取价格信息")
else:
    print("无法获取合约地址的相关信息")
