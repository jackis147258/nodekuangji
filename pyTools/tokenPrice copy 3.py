# import requests
# import requests

# url = "https://www.oklink.com/api/v5/explorer/blockchain/summary?chainShortName=ETH"

# payload = ""
# headers = {
#   # apiKey
#   'Ok-Access-Key': 'e040c7ef-8aa2-4e02-a18b-782cbd05a158'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)



import requests

# OKLink API key
api_key = 'e040c7ef-8aa2-4e02-a18b-782cbd05a158'
headers = {
    'Ok-Access-Key': api_key,
    'Accept': 'application/json',
}

# Token contract address
contract_address = '0x2e6ee934c0bb2a8446c50acef58e9caa47a39dcd'
chain_id = 0  # Polygon chain ID

# URL for querying token price
url = f'https://www.oklink.com/api/v5/explorer/tokenprice/market-data?chainId={chain_id}&tokenContractAddress={contract_address}'

# Making the request
response = requests.get(url, headers=headers)
data = response.json()

# Checking and printing the token price
if data['code'] == '0':
    token_data = data['data'][0]
    token_price = token_data.get('lastPrice', 'Price not found')
    print(f"Token price is: ${token_price}")
else:
    print(f"Error fetching data: {data.get('msg', 'Unknown error')}")
