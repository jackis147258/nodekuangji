# Create your tasks here

# from demoapp.models import Widget

from celery import shared_task
import time
from apiV1.DeFi2 import DeFi2,celeryPrice,celeryBuySell,getTokenNewUser

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery.exceptions import MaxRetriesExceededError
from reg.ebcFenRun import FenRun,createEbcUser
from reg import ebcUserTiXian ,getTokenJiLu
import logging

logger = logging.getLogger(__name__)

 
from .web3_utils import Web3Client,listen_to_deposit_events
from .web3_tixian import listen_to_Withdrawal_events
from .nodeKjFenRun import fanTiXianTime
from .nodeKjSheQu import  sheQuFenRun
from .web3_Price import getPrice
@shared_task
def listen_toDeposit ():
    listen_to_deposit_events()


# 提现
@shared_task
def listen_toWithdrawal ():
    listen_to_Withdrawal_events()

# 按小时 前 反提现
@shared_task
def fanTiXianTimeTask (t_house):    
    fanTiXianTime(t_house)
 

#社区分润
@shared_task
def sheQuFenRunTask ():
    sheQuFenRun()


#amt 实时价格
@shared_task
def tokenPrice ():
    getPrice()