import requests
import json

def get_token_price( contract_address):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {
        'contract_address': contract_address,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'c86ad6d1-d509-4c15-b707-b293e0db9c59',
    }
    
    response = requests.get(url, headers=headers, params=parameters)
    data = json.loads(response.text)
    
    if 'data' in data and len(data['data']) > 0:
        token_info = list(data['data'].values())[0]
        price = token_info['quote']['USD']['price']
        return price
    else:
        return None

# 在这里替换你的 CoinMarketCap API 密钥
api_key = 'your_api_key_here'
# 替换为你要查询的代币的合约地址
contract_address = '0x4339e7c4d7c9495c704bc7818b2032f4b72c8dd9'

price = get_token_price( contract_address)
if price:
    print(f"The price of the token is ${price:.2f}")
else:
    print("Token not found or API request failed.")
