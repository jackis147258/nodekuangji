import json
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware
from django.conf import settings
from .models import ebcJiaSuShouYiJiLu, userToken  # 假设这些模型用于保存记录
from .abi import tokenAbi  # ABI 文件
from decouple import config
from django.db import transaction
from django.contrib.auth import get_user_model
User = get_user_model()
import logging
logger = logging.getLogger(__name__)
from typing import Optional
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=4)

class Web3cc:
    def __init__(self): 
        # 初始化 Web3 连接 
        pancakeRouterAddress = '0x6fdE5ec4ed6adCeee8B19136E697A94f7B0885a6'
        # pancakeRouterAddress = config('EbcState_ADDRESS', default='')

        self.EbcStateADDRESS = pancakeRouterAddress
        pancakeAbi = tokenAbi(pancakeRouterAddress)  # 合约 ABI 
    
        bsc = "https://rpc.ankr.com/bsc/174ba138f2cbc5773ef292c0e0a941ec3f23246439e9f0b8d7bec242a67f8c20"  #免费      
        self.web3 = Web3(Web3.HTTPProvider(bsc))
        if not self.web3.is_connected(): 
            print("Not Connected to BSC wait...")    
            return 'Not Connected to BSC'

        # 加载代币合约
        self.token_contract = self.web3.eth.contract(address=pancakeRouterAddress, abi=pancakeAbi)
 
    
    def get_transactions(self, start_block, end_block):
        # 查询从 start_block 到 end_block 之间的 Transfer 事件
        transfer_event_signature = self.web3.keccak(text="Transfer(address,address,uint256)").hex()
        
        try:
            # 调用合约事件过滤器
            event_filter = self.web3.eth.filter({
                "fromBlock": start_block,
                "toBlock": end_block,
                "address": self.token_contract.address,
                "topics": [transfer_event_signature]
            })
            logs = event_filter.get_all_entries()

            # 处理交易记录
            for log in logs:
                transaction = self.web3.eth.getTransactionReceipt(log['transactionHash'])
                to_address = log['topics'][2]  # 获取交易的目标地址

                # 判断是否转账到目标地址
                if self.web3.toChecksumAddress('0x6fde5ec4ed6adceee8b19136e697a94f7b0885a6') == self.web3.toChecksumAddress(to_address):
                    logger.info(f"找到转账到 0x6fde5ec4ed6adceee8b19136e697a94f7b0885a6 的交易: {log['transactionHash']}")
                    # 保存或处理交易记录
                    self.save_transaction(log, transaction)

        except Exception as e:
            logger.error(f"查询交易时出错: {str(e)}")
    
    def save_transaction(self, log, transaction):
        # 这里可以添加将交易记录保存到数据库的逻辑
        try:
            with transaction.atomic():
                ebcJiaSuShouYiJiLu.objects.create(
                    # 根据模型字段保存信息
                    transaction_hash=log['transactionHash'].hex(),
                    block_number=log['blockNumber'],
                    from_address=self.web3.toChecksumAddress(log['topics'][1]),
                    to_address=self.web3.toChecksumAddress(log['topics'][2]),
                    value=int(log['data'], 16),  # 假设代币的 value 是在 `log['data']` 中
                    gas_used=transaction['gasUsed']
                )
                logger.info(f"交易记录已保存: {log['transactionHash']}")
        except Exception as e:
            logger.error(f"保存交易记录时出错: {str(e)}")

# 示例调用
# web3cc_instance = Web3cc()
# web3cc_instance.get_transactions(10000000, 'latest')  # 查询从区块 10000000 到最新区块的交易
