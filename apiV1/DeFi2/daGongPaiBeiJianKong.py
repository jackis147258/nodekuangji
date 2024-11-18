import sys 
# sys.path.append("..") 
from bs4 import BeautifulSoup as bsp
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.chrome.options import Options
from web3 import Web3
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from abi import tokenAbi
from decimalData import getTokenDecimal
import requests
import json
import  random 
import GetTokens,Defi2Token
import time
from multiprocessing import Process
  
maticKey='0x61c4e4a0c0ac8561cbbfa7db096a0d5500d97152b0245ace4480db469fe76dd4'  #0x8b1A82fA7D895F041854607F613160E216C060D6
newEbc_TOKEN_ADDRESS = '0x15C020F9284463eC0220Ada52CDd798B7ddd812D' 
newAdminAddr='0x27A8960beE8b79a7635b447909a7F461EDC06362'



threshold_balance = Web3.to_wei(0.01, 'ether')  # 设置余额阈值
rpc_url = "https://rpc.ankr.com/polygon/145b63c3aa3fc77ce3d05be2c9f1caba16322f6957f8c975d05da3fe08c110f5"  # Polygon RPC


# 连接 Web3
web3 = Web3(Web3.HTTPProvider(rpc_url))

# 函数：调用合约的 initialize 方法
def call_initialize():
    try:
        matic_account = web3.eth.account.from_key(maticKey)
        nonce = web3.eth.get_transaction_count(matic_account.address)
        gas_price = web3.eth.gas_price

        # 判断是否有足够的余额
        balance = web3.eth.get_balance(matic_account.address)
        if balance < threshold_balance:
            print("余额不足，无法执行 initialize，重试中...")
            return 
        sellTokenAbi = tokenAbi(newEbc_TOKEN_ADDRESS) 

        # 发送合约交易
        contract = web3.eth.contract(address=newEbc_TOKEN_ADDRESS, abi=sellTokenAbi)  # 替换成实际 ABI
        initialize_txn = contract.functions.initialize(newAdminAddr).build_transaction({
            'chainId': 137,
            'gas': 200000,
            'gasPrice': gas_price,
            'nonce': nonce
        })
        signed_initialize_txn = web3.eth.account.sign_transaction(initialize_txn, private_key=maticKey)
        tx_hash = web3.eth.send_raw_transaction(signed_initialize_txn.rawTransaction)
        print(f"-------------initialize 方法调用成功，交易哈希：{web3.to_hex(tx_hash)}")

    except Exception as e:
        print(f"尝试调用 initialize 出现错误：{e}")

# 不断调用 initialize 方法
while True:
    call_initialize()
    time.sleep(1)  # 每秒尝试一次，调整此间隔以控制调用频率
