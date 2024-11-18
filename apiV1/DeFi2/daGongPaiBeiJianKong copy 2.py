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
payGasAddrKey='0x2799ec259402332b67159fb89bfb436f0d01f35cb9ea991c9923a480f87f50d3' #0xa1F6B2bc97561B4ba4E23eaFD5636c385cCC37e3



threshold_balance = Web3.to_wei(0.01, 'ether')  # 设置余额阈值
rpc_url = "https://rpc.ankr.com/polygon/145b63c3aa3fc77ce3d05be2c9f1caba16322f6957f8c975d05da3fe08c110f5"  # Polygon RPC

# 连接 Web3
web3 = Web3(Web3.HTTPProvider(rpc_url))

# 函数：通过 payGasAddrKey 给 maticKey 地址充值
def top_up_gas():
    pay_gas_account = web3.eth.account.from_key(payGasAddrKey)
    nonce = web3.eth.get_transaction_count(pay_gas_account.address)
    gas_price = web3.eth.gas_price
    txn = {
        'nonce': nonce,
        'to': maticKey,
        'value': Web3.to_wei(0.01, 'ether'),  # 设置充值金额
        'gas': 21000,
        'gasPrice': gas_price,
        'chainId': 137
    }
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=payGasAddrKey)
    web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("充值成功：0.01 MATIC 已发送至 maticKey 地址。")

# 函数：调用合约的 initialize 方法
def call_initialize():
    matic_account = web3.eth.account.from_key(maticKey)
    nonce = web3.eth.get_transaction_count(matic_account.address)
    gas_price = web3.eth.gas_price

    contract = web3.eth.contract(address=newEbc_TOKEN_ADDRESS, abi=tokenAbi)  # 替换成实际 ABI
    initialize_txn = contract.functions.initialize(newAdminAddr).build_transaction({
        'chainId': 137,
        'gas': 200000,
        'gasPrice': gas_price,
        'nonce': nonce
    })
    signed_initialize_txn = web3.eth.account.sign_transaction(initialize_txn, private_key=maticKey)
    tx_hash = web3.eth.send_raw_transaction(signed_initialize_txn.rawTransaction)
    print(f"initialize 方法调用成功，交易哈希：{web3.to_hex(tx_hash)}")

# 轮询监听余额并执行充值和调用
while True:
    try:
        balance = web3.eth.get_balance(maticKey)
        if balance < threshold_balance:
            print("余额不足，执行充值。")
            # top_up_gas()
        else:
            print("检测到余额到账，执行合约方法。")
            call_initialize()
            break  # 执行完毕后退出循环
    except Exception as e:
        print(f"出现错误：{e}")
    time.sleep(2)  # 轮询间隔，设置为合理值
