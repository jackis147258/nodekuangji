import requests
from django.db.models import Count, F, Subquery, OuterRef, ExpressionWrapper, IntegerField

from django.db import transaction
from .models import CustomUser  # 假设 CustomUser 是用户模型
import logging
import openpyxl
from datetime import datetime

logger = logging.getLogger(__name__)

def get_transactions_from_bscscan(contract_address, start_block, end_block, api_key):
    url = f"https://api.bscscan.com/api?module=account&action=tokentx&contractaddress={contract_address}&startblock={start_block}&endblock={end_block}&sort=asc&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == '1':  # 确保查询成功
        return data['result']
    else:
        return []

def bscIsOneToken():
    # 示例调用
    contract_address = '0x6fdE5ec4ed6adCeee8B19136E697A94f7B0885a6'  # 代币合约地址
    start_block = 43255262
    end_block = 'latest'
    bscscan_api_key = 'BD1S3M7QY58J5AE11JUWVXGZWDHU7QFFAF'

    # toToken 地址
    # to_address = '0x6fde5ec4ed6adceee8b19136e697a94f7b0885a6'  # 替换为你的 toToken 地址

    # 假设代币的 decimals 为 18（大多数 ERC20 代币是 18 位小数）
    decimals = 18
    one_token_value = 10 ** decimals  # 1 枚代币的实际值（以 wei 计）

    # 从数据库获取所有 userType 为 'candy' 的用户
    candy_users = CustomUser.objects.filter(userType='candy')
    # candy_users = CustomUser.objects.filter(userType='candy', id__gt=5000)


    # 获取交易记录
    transactions = get_transactions_from_bscscan(contract_address, start_block, end_block, bscscan_api_key)

    # 遍历每个用户，检查是否有转账交易
    for user in candy_users:
        from_address = user.username  # 假设用户的 fromToken 地址存储在 wallet_address 字段中
        
        # 遍历每笔交易，检查是否符合条件
        for tx in transactions:
            block_number = tx.get('blockNumber', '未知区块')  # 取区块号，如果没有则返回 '未知区块'
            logger.info(f"区块编号为 {block_number}")
            # if tx['from'].lower() == from_address.lower() and tx['to'].lower() == to_address.lower() and int(tx['value']) == one_token_value:
            if tx['from'].lower() == from_address.lower()  and int(tx['value']) == one_token_value:
                # 如果符合条件，更新 CustomUser 表中的 isOneToken 字段
                try:
                    with transaction.atomic():
                        user.isOneToken = 1
                        user.save(update_fields=['isOneToken'])
                        # 提取区块号
                        block_number = tx.get('blockNumber', '未知区块')  # 取区块号，如果没有则返回 '未知区块'


                        logger.info(f"用户 {user.id} 转出 1 枚代币到  ，区块编号为 {block_number}")
                except Exception as e:
                    logger.error(f"更新用户 {user.id} 的 isOneToken 字段失败: {e}")

                # 找到交易后可以停止进一步的判断
                break



    

# 输出需要充值 用户 
def generate_custom_user_report():
    # 创建一个 Excel 工作簿
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "CustomUser Report"

    # 添加标题行
    ws.append([
        'ID', 'Username', '全部有效数量',   
        '新增有效用户', '有效用户*300值'
    ])

    # 子查询：统计每个用户的子用户数量
    # parent_count_subquery = CustomUser.objects.filter(
    #     parent_id=OuterRef('id')
    # ).values('parent_id').annotate(count=Count('id')).values('count')

    # 主查询：获取所有 userType 为 'candy' 的用户
    candy_users = CustomUser.objects.filter(userType='candy')

    # 循环处理每个用户
    for user in candy_users:
        # 计算每个用户的子用户数量和其他字段
        parent1Num = CustomUser.objects.filter(parent_id=user.id,isOneToken=1).count()
        # parent1NumMultiplied = parent1Num * 300
          # 如果 user.candyFanNum 是 None，则将其设为 0
        candyFanNum = user.candyFanNum if user.candyFanNum is not None else 0

        parent1NumMinusCandyFanNum = parent1Num - candyFanNum
        

        if parent1NumMinusCandyFanNum != 0:
            parent1NumMinusCandyFanNumMultiplied = parent1NumMinusCandyFanNum * 300

            # 将结果添加到 Excel 文档中
            ws.append([
                user.id,
                user.username,
                parent1Num,
                # parent1NumMultiplied,
                parent1NumMinusCandyFanNum,
                parent1NumMinusCandyFanNumMultiplied
            ])
            # 打印结果到控制台
            print(f"User ID: {user.id}, Username: {user.username}, Parent1Num: {parent1Num}, Parent1NumMinusCandyFanNum: {parent1NumMinusCandyFanNum}, Parent1NumMinusCandyFanNumMultiplied: {parent1NumMinusCandyFanNumMultiplied}")


    # 保存 Excel 文件

     # 获取当前时间并格式化为 'YYYYMMDD_HHMM'
    current_time = datetime.now().strftime("%Y%m%d_%H%M")

    # 保存 Excel 文件，文件名包含当前时间到分钟
    file_path = f'report_{current_time}.xlsx'

    # file_path = 'custom_user_report.xlsx'
    
    wb.save(file_path)

    return file_path  # 返回文件路径用于后续操作

def printcc():
    # 区块记录用户是否转账CC Token
    bscIsOneToken()

    # 调用该函数生成报告
    file_path = generate_custom_user_report()
    print(f"Excel report generated: {file_path}")



# ------------------------------------------------------------over------------
# 更新用户 candyFanNum 需要返利的直推人数 
def update_candy_fan_num():
    # 获取所有 userType 为 'candy' 的父级用户
    candy_users = CustomUser.objects.filter(userType='candy')

    # 循环处理每个父级用户
    for user in candy_users:
        # 统计该用户的所有 isOneToken 为 1 的子级用户数
        candy_fan_count = CustomUser.objects.filter(parent_id=user.id, isOneToken=1).count()
        # 更新当前用户的 candyFanNum 字段
        user.candyFanNum = candy_fan_count
        user.save(update_fields=['candyFanNum'])