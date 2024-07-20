# myapp/web3_utils.py
import json
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware
from django.conf import settings
from .models import ebcJiaSuShouYiJiLu,userToken,payToken
from .abi import tokenAbi
# from config import EbcContractTokenAddress
from decouple import config
from django.db import transaction
from django.contrib.auth import get_user_model
User = get_user_model()
import logging
logger = logging.getLogger(__name__)
from typing import Optional
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=4)

class Web3Price:
    def __init__(self):
        # 0x9E5993a7D9af815216810680e0a319491C263B46   0x779732DC4aa3Bf415a0D1435e919BcAF5a9210E7
        # pancakeRouterAddress = config('EbcState_ADDRESS', default='')         
        pancakeRouterAddress = '0x4edad210cb43337175D0Da38EbaEa96a71e6E5b8'
        self.EbcStateADDRESS = pancakeRouterAddress

        pancakeAbi = tokenAbi(pancakeRouterAddress)  # 合约 ABI 
        # 初始化 Web3 连接
        # bsc = "https://rpc.ankr.com/bsc/174ba138f2cbc5773ef292c0e0a941ec3f23246439e9f0b8d7bec242a67f8c20"  #免费
        bsc=config('BSC', default='')
        self.web3 = Web3(Web3.HTTPProvider(bsc))
        if not self.web3.is_connected(): 
            print("Not Connected to BSC wait...")    
            return 'Not Connected to BSC' 
        self.contract = self.web3.eth.contract(address=pancakeRouterAddress, abi=pancakeAbi)
    
    def get_price(self,latest_block):
       
        # 从最新的 10 个区块中获取事件日志
        # latest_block = self.web3.eth.block_number
        # from_block = latest_block - 20 if latest_block >= 10 else 0
        # to_block = latest_block
        logger.info('提取tokenPrice ...当前价格'+str(latest_block) )
        logger.info('合约地址'+str(self.EbcStateADDRESS) )
         
        pairAddr='0x2E6Ee934c0bB2a8446C50acEf58e9caa47a39DCD'
        usdtWei=1000000000000000000
    #    720497527344270402
        t_price1= self.contract.functions.getTokenPrice(pairAddr,usdtWei).call()

        t_price118=t_price1/1000000000000000000

        pairAddr='0xf6291fdfb6918368C8C3fb9A7719659ADBd8F9bF'
        usdtWei=1000000000000000000
        # 80973
        t_price2= self.contract.functions.getTokenPrice(pairAddr,usdtWei).call()

        t_price26=t_price2/1000000
        t_tokenP=t_price26/t_price118
        print (t_tokenP)
        logger.info('提取tokenPrice'+str(t_tokenP) )
        return "{:.2f}".format(t_tokenP)



def format_token_amount(raw_amount, decimals=18):
    # 将字符串转换为浮点数，并应用小数位转换
    formatted_amount = float(raw_amount) / (10 ** decimals)
    # 返回格式化后的数值，保留两位小数
    return "{:.2f}".format(formatted_amount)


 
def getPrice():

    if not redis_client.exists('token_price'):
        # 如果不存在，则将 t_pyUserNumberAll 设置为 0
        latest_price = 0.11
    else:
        # 如果存在，则从 Redis 中获取值
        latest_price = redis_client.get('token_price')  
      
    web3_client = Web3Price()

    # now_block = web3_client.web3.eth.block_number
    # if int(latest_block)>int(now_block):
    #     latest_block=now_block

    new_price = web3_client.get_price(float(latest_price))
    
    # process_Withdrawal_event(new_price)
    redis_client.set('token_price', str(float(new_price))) 
   
  
