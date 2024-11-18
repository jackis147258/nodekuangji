from django.core.management.base import BaseCommand
from  reg.web3_PriceBsc import  getPrice  # 根据你的路径导入 Web3cc 类
from  reg.web3_tixianBsc import  listen_to_Withdrawal_events
from  reg.web3_utilsBsc import listen_to_deposit_events

from reg.web3_utilsBsc import   listenDepositOne as bscChongZhi
from reg.web3_tixianBsc import  listen_to_Withdrawal_eventsOne as bscTiXian
from reg.shengji.upToken import  upToken
import requests

# 自定义命令必须继承自 BaseCommand 类
class Command(BaseCommand):
    help = '调试 Web3cc 类中的方法'

    def handle(self, *args, **kwargs):         
        # 加个测试
        # getPrice()

        # 账户星级升级
        t_upToken = upToken()
        t_upToken.shengji()

        # listen_to_Withdrawal_events()
        # listen_to_deposit_events()
        # bscChongZhi(44005275)
        # bscTiXian(44005275)


      
  