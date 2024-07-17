import coinmarketcapapi
import os

# 设置API密钥
api_key = 'c86ad6d1-d509-4c15-b707-b293e0db9c59'
cmc_client = coinmarketcapapi.CoinMarketCapAPI(api_key)

# 获取特定加密货币的最新市场报价
response = cmc_client.cryptocurrency_quotes_latest(symbol='MATIC')
price = response.data['MATIC']['quote']['USD']['price']
print(f"Polygon (MATIC) 的最新价格是: ${price}")
