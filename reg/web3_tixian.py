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

redis_client = redis.StrictRedis(host='localhost', port=6379, db=3)

class Web3TiXian:
    def __init__(self):
        pancakeRouterAddress = config('EbcState_ADDRESS', default='')
        pancakeAbi = tokenAbi(pancakeRouterAddress)  # 合约 ABI 
        # 初始化 Web3 连接
        # bsc = "https://rpc.ankr.com/bsc/174ba138f2cbc5773ef292c0e0a941ec3f23246439e9f0b8d7bec242a67f8c20"  #免费
        bsc=config('BSC', default='')
        self.web3 = Web3(Web3.HTTPProvider(bsc))
        if not self.web3.is_connected(): 
            print("Not Connected to BSC wait...")    
            return 'Not Connected to BSC' 
        self.contract = self.web3.eth.contract(address=pancakeRouterAddress, abi=pancakeAbi)
    
    def listen_Withdrawal_events(self,latest_block):
        
        # 从最新的 10 个区块中获取事件日志
        # latest_block = self.web3.eth.block_number
        from_block = latest_block - 10 if latest_block >= 10 else 0
        to_block = latest_block

        # 获取 Deposit 事件日志
        events = self.contract.events.Withdrawal().get_logs(fromBlock=57923019, toBlock=57923020)

        # 处理事件日志并提取所需数据  57917516
        event_list = []
        for event in events:
            event_data = {
                'user': event['args']['user'],
                'amount': event['args']['amount'],                
                'time': event['args']['timestamp'],
                'hash': event['args']['hash'],
            }
            event_list.append(event_data)
        
        return event_list




def process_Withdrawal_event(event_list):
    # Process the event (e.g., save to database, perform some action)
    logger.info('获取用户提现记录'+'开始...' )
    for event_data in event_list:
        try:
            with transaction.atomic():
                # 判读id 是否重复 
                
                payTokenObj=payToken.objects.filter(HashId=event_data['hash']).first()
                # 表示已经处理过流水
                if payTokenObj:                    
                    logger.info('该笔流水已处理 id:'+event_data['hash'] +' 用户:'+str(event_data['user']) )
                    continue

                # 获得用户 对象
                try:
                    t_user = User.objects.get(username=event_data['user'])
                except User.DoesNotExist:
                    t_user = None
                    logger.info('Failed:用户'+str(event_data['user'])+ '不存在' )
                    continue
                
                # now_userToken = t_user.usertoken_set.first()     # type: Optional[userToken] 
                # if  not now_userToken:                    
                #     logger.info('获取用户充值记录'+t_user.id+'用户token不存在' )
                #     continue
                #记录  添加余额   // layer==0  冲 usdt  1  yl   2 jz
                t_Remark='提现完成'
                # now_userToken.jzToken-=float(event_data['amount'])
                # now_userToken.save()
                # # 充值
                # if event_data['layer']==0:
                #     now_userToken.usdtToken-=float(event_data['amount'])
                #     now_userToken.save()
                #     t_Remark='充值USDT'
                # if event_data['layer']==1:
                #     now_userToken.ylToken-=float(event_data['amount'])
                #     now_userToken.save()
                #     t_Remark='充值YL'
                # if event_data['layer']==2:
                #     now_userToken.jzToken-=float(event_data['amount'])
                #     now_userToken.save()
                #     t_Remark='充值JZ'
                
                  
                ebcJiaSuShouYiJiLu.objects.create(
                    uidB=t_user.id,
                    fanHuan=event_data['amount'],
                    Layer=event_data['layer'],
                    cTime=event_data['time'], 
                    Remark=t_user.id+t_Remark,
                )
                logger.info('用户'+t_user.id+t_Remark+event_data['amount'] )

                
        except Exception as e:
                    # 处理异常
                    result = ["Failed-everybadyFan", f"ERROR: {e}"]
                    print(result)
                    logger.info(result)
                    return result
    # Add your processing logic here

 
def listen_to_Withdrawal_events():

    if not redis_client.exists('tiXianLatest_block'):
        # 如果不存在，则将 t_pyUserNumberAll 设置为 0
        latest_block = 57917516
    else:
        # 如果存在，则从 Redis 中获取值
        latest_block = redis_client.get('tiXianLatest_block')  
      
    web3_client = Web3TiXian()
    event_list = web3_client.listen_Withdrawal_events(int(latest_block))
    
    process_Withdrawal_event(event_list)
    redis_client.set('tiXianLatest_block', str(latest_block + 9)) 
    time.sleep(2)
  
