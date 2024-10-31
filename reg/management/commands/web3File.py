from django.core.management.base import BaseCommand
from  reg.web3_cc import Web3cc  # 根据你的路径导入 Web3cc 类
from  reg.web3_cc1 import  generate_custom_user_report,  bscIsOneToken 

import requests

# 自定义命令必须继承自 BaseCommand 类
class Command(BaseCommand):
    help = '调试 Web3cc 类中的方法'

    def handle(self, *args, **kwargs): 
        
        bscIsOneToken()
        self.stdout.write(self.style.SUCCESS('bscIsOneToken 调试完成！'))

        # 输出当前 需要 转币数量
        generate_custom_user_report()  
        self.stdout.write(self.style.SUCCESS('generate_custom_user_report 调试完成！'))


      
  