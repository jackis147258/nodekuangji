from django.contrib.auth.models import  Group
from .models import CustomUser,ebcJiaSuShouYiJiLu,tokenZhiYaJiShi,userToken,payToken
from decimal import Decimal
from itertools import islice
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import tools
import logging
logger = logging.getLogger(__name__)
from django.db import transaction
from typing import Optional

 # def sanYeji(string user_id,string t_time):
def sanYeji( user_id, t_time):
    try:                
        parentUser = CustomUser.objects.get(id=user_id) # type: Optional[CustomUser]  
        # 执行获取到 parentUser 后的逻辑
    except CustomUser.DoesNotExist:
        # 处理 parentUser 不存在的情况
        t_backStr={'valid': True, 'message': '成功-DoesNotExist' }
        print(t_backStr)
    
    
    # 如果矿机有停运状态 不能那反润
    # if tokenZhiYaJiShi.get_kuangjiList0_by_uid(parentUser) != None:
    #     logger.info('用户id:'+str(t_parent_id) +t_user.username+'有矿机停止质押,请重新质押' )
    # children_count = parentUser.get_children().count()  
    # 看是否满足返还条件
    # if isFanDai(i,children_count):                 
        
    try:
        with transaction.atomic(): 

            children = parentUser.get_children()     
            # 计算每个直推人的 TDallAmount 和用户名 .username
            td_all_amounts_with_usernames = [(child.TDallInAmount, child.username) for child in children]
            
        
            # # 计算每个直推人的 TDallAmount 数量
            # td_all_amounts = [child.TDallInAmount for child in children]

            if td_all_amounts_with_usernames:
                # 找到最大的 TDallAmount  大区
                # max_td_all_amount = max(td_all_amounts)
                    # 找到最大 TDallInAmount 以及对应的用户名
                max_td_all_amount, max_username = max(td_all_amounts_with_usernames, key=lambda x: x[0])
                        # 输出最大值和对应的用户名
                
                print(f"最大 TDallInAmount: {max_td_all_amount}, 对应的用户: {max_username}")



                # 计算其他人的 TDallAmount 总和  小区
                # sum_other_td_all_amounts = sum(td_all_amounts) - max_td_all_amount
                # sum_other_td_all_amounts = sum(td_all_amounts_with_usernames, key=lambda x: x[0]) - max_td_all_amount

                # 计算所有 TDallInAmount 的总和
                total_sum = sum(amount for amount, _ in td_all_amounts_with_usernames)

                # 从总和中减去一个最大值
                sum_other_td_all_amounts = total_sum - max_td_all_amount
    except Exception as e:
        # 处理错误，此时事务已经回滚 
        result = ["Failed-TDyeJi", f"ERROR: {e}"]
        logger.info(result)
        t_backStr={'valid': False, 'message': {e} }

    