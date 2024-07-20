import requests

def get_usd_price(symbol, api_key):
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    if 'data' in data and symbol in data['data']:
        price = data['data'][symbol]['quote']['USD']['price']
        return price
    else:
        print("Failed to retrieve price data.")
        return None

# 替换为你的 API key
api_key = 'c86ad6d1-d509-4c15-b707-b293e0db9c59'

# api_key = 'your_coinmarketcap_api_key'
wpc_price = get_usd_price('WPC', api_key)
print(f"WPC Price: {wpc_price} USD")
