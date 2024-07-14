import requests

def get_amt_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=amateras&vs_currencies=usd,cny"
    response = requests.get(url)
    data = response.json()
    amt_usd_price = data["amateras"]["usd"]
    amt_cny_price = data["amateras"]["cny"]
    return amt_usd_price, amt_cny_price

usd_price, cny_price = get_amt_price()
print(f"AMT的USD价格：${usd_price:.2f}")
print(f"AMT的CNY价格：¥{cny_price:.5f}")
