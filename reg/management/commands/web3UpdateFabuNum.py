from django.core.management.base import BaseCommand
from  reg.web3_cc import Web3cc  # 根据你的路径导入 Web3cc 类
from  reg.web3_cc1 import update_candy_fan_num  
import requests
# 自定义命令必须继承自 BaseCommand 类
class Command(BaseCommand):
    help = '调试 Web3cc 类中的方法'

    def handle(self, *args, **kwargs):
        # 更新 已发转币数量
        update_candy_fan_num()
        self.stdout.write(self.style.SUCCESS('update_candy_fan_num 调试完成！'))
    

    
