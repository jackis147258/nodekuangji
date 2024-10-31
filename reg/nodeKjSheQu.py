
import asyncio
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

from datetime import  timedelta
from django.db import transaction
from decouple import config

from django.contrib.auth import get_user_model
User = get_user_model()
from typing import Type
from .  import ebcFenRun
from typing import Optional
from app1.models import webInfo
from django.db.models import Q
from django.db.models import Count,Sum

import random
import string

# 单独一个用户 分销返加速  
# def userFenRun(t_user,tokenZhiYa: Type[tokenZhiYaJiShi]):
def sheQuFenRun():  # amount 分润基数  layer 类型0 矿机质押  1 每日获取利润
    logger.info('start:社区分润开始。。。' )        
    try:
        with transaction.atomic():   
            #1.获取 需要分润数量
            now_webid = webInfo.objects.filter(webid=3).first()    
            t_fenRunNumber= now_webid.jiangJinChi 
            # 获取 TDxiaoQuAmount 数量大于 30000 的用户集合
            # users_with_high_tdxiaoqu_amount = CustomUser.objects.filter(TDxiaoQuAmount__gt=30000)
            # 筛选 TDxiaoQuAmount 大于 30000 且 username 为空，同时排除特定的用户
            users_with_high_tdxiaoqu_amount = CustomUser.objects.filter(
                Q(TDxiaoQuAmount__gte=10000)  
            ).exclude(
                Q(username='0x606adb6c2b7d415e0fd58b7d9cff6b71e5139ceb') | Q(username='0x8b1a82fa7d895f041854607f613160e216c060d')| Q(username='admin1')
            )
            if users_with_high_tdxiaoqu_amount is None:
                now_webid.jiangJinChi =0
                now_webid.save()
                logger.info('社区奖励完成--没有用户满足条件' )        
                return  True, '分润结束' 



            # # 获取所有用户的tuanduiLevel字段的计集合
            # tuandui_level_counts = users_with_high_tdxiaoqu_amount.values('tuanduiLevel').annotate(count=Count('tuanduiLevel'))
            # 获取所有用户的tuanduiLevel字段的计集合
            tuandui_level_counts = users_with_high_tdxiaoqu_amount.values('tuanduiLevel').annotate(count=Count('tuanduiLevel'))

            # 计算tuanduiLevel字段的合计值
            tuandui_level_sum = users_with_high_tdxiaoqu_amount.aggregate(total_tuanduiLevel=Sum('tuanduiLevel'))['total_tuanduiLevel']




            # 3. 计算每个用户应得的分润数量
            # user_count = users_with_high_tdxiaoqu_amount.count()
            if tuandui_level_sum is None or tuandui_level_sum <=0 :
                now_webid.jiangJinChi =0
                now_webid.save()
                logger.info('社区奖励完成--没有分红权' )        
                return  True, '分润结束' 

            per_user_fenRun = t_fenRunNumber / tuandui_level_sum
            # 输出用户集合
            for t_user in users_with_high_tdxiaoqu_amount:
                # print(f"用户名: {user.username}, TDxiaoQuAmount: {user.TDxiaoQuAmount}")
                t_fenRunAll=t_user.tuanduiLevel*per_user_fenRun
                now_userToken = t_user.usertoken_set.first()     # type: Optional[userToken] 
                now_userToken.jzToken+=t_fenRunAll 
                now_userToken.save()
                # 写入记录     
                t_ebcJiaSuShouYiJiLu=ebcJiaSuShouYiJiLu ()
                t_ebcJiaSuShouYiJiLu.uidA=0   #发送方 0平台整理后分配
                t_ebcJiaSuShouYiJiLu.uidB=t_user.id  # 接收方
                t_ebcJiaSuShouYiJiLu.status=1  #已转
                t_ebcJiaSuShouYiJiLu.Layer=5  # 0充值 1 代数 2 层数  5 分红
                t_ebcJiaSuShouYiJiLu.fanHuan=t_fenRunAll
                t_ebcJiaSuShouYiJiLu.Remark='社区奖励'+str(t_fenRunAll)      #'    
                t_ebcJiaSuShouYiJiLu.save()   

            #1.需要分润数量清零
            # now_webid = webInfo.objects.filter(webid=3).first()    
            now_webid.jiangJinChi =0
            now_webid.save()

    except Exception as e:
        # 处理错误，此时事务已经回滚 
        result = ["Failed-sheQuYeji", f"ERROR: {e}"]
        logger.info(result)
        return  False, {e}
        # return result       
    logger.info('社区奖励完成-完成分润' )        
    return  True, '分润成功' 



# # 单独一个用户 分销返加速  
# # def userFenRun(t_user,tokenZhiYa: Type[tokenZhiYaJiShi]):
# def TDyeJi(t_user,number):  # amount 分润基数  layer 类型0 矿机质押  1 每日获取利润

#     logger.info('start:用户'+str(t_user.id) +'开始分润' )        
   
#     try:
#         # 同级别不重复
#         # t_best=t_user.cengShu
#         t_backStr={'valid': True, 'message': '团队业绩计算成功' }
#         # t_backStr={'valid': False, 'message': ' ' }


#         t_parent_id=t_user.parent_id    
#         for i in range(0, 20, 1): #执行20次 向上找20级          

#             # 处理第一个人             
#               # 到了顶级 就直接 跳出
#             if t_parent_id==1 or t_parent_id==None:
#                 logger.info('用户id:'+str(t_parent_id) +t_user.username+'到了顶级不进行分润了' )
#                 t_backStr={'valid': True, 'message': '成功-parentDingji' }
#                 break  

#             try:                
#                 parentUser = CustomUser.objects.get(id=t_parent_id) # type: Optional[CustomUser]  
#                 # 执行获取到 parentUser 后的逻辑
#             except CustomUser.DoesNotExist:
#                 # 处理 parentUser 不存在的情况
#                 t_backStr={'valid': True, 'message': '成功-DoesNotExist' }
#                 break
           
#             # 如果矿机有停运状态 不能那反润
#             # if tokenZhiYaJiShi.get_kuangjiList0_by_uid(parentUser) != None:
#             #     logger.info('用户id:'+str(t_parent_id) +t_user.username+'有矿机停止质押,请重新质押' )
#             # children_count = parentUser.get_children().count()  
#             # 看是否满足返还条件
#             # if isFanDai(i,children_count):                 
#             if True:   
#                 try:
#                     with transaction.atomic(): 

#                         children = parentUser.get_children()                        
#                         # 计算每个直推人的 TDallAmount 数量
#                         td_all_amounts = [child.TDallInAmount for child in children]

#                         if td_all_amounts:
#                             # 找到最大的 TDallAmount  大区
#                             max_td_all_amount = max(td_all_amounts)

#                             # 计算其他人的 TDallAmount 总和  小区
#                             sum_other_td_all_amounts = sum(td_all_amounts) - max_td_all_amount

#                             # 返回值
#                             result = sum_other_td_all_amounts
#                         else:
#                             result = 0
#                         # 确认 团队等级
#                         t_tuanduiLevel=0
#                         if result>=30000:
#                             t_tuanduiLevel=1
#                         if result>=50000:
#                             t_tuanduiLevel=2
#                         if result>=100000:
#                             t_tuanduiLevel=5
#                         if result>=300000:
#                             t_tuanduiLevel=15
#                         if result>=500000:
#                             t_tuanduiLevel=30

#                         parentUser.TDallAmount=max_td_all_amount #得到团队大区业绩
#                         parentUser.TDxiaoQuAmount=sum_other_td_all_amounts #得到小区团队业绩总和
#                         parentUser.tuanduiLevel=t_tuanduiLevel
#                         parentUser.TDallInAmount+=number #的到用户总业绩
#                         parentUser.save()

#                         # now_parentToken = parentUser.usertoken_set.first()     # type: Optional[userToken] 
#                         # if  not now_parentToken: 
#                         #     # return JsonResponse({'valid': False, 'message': '用户token不存在'}) 
#                         #     logger.info('用户token不存在,用户id:'+str(parentUser.id)  )        

#                         #     return  False, '用户token不存在'
#                         # now_parentToken.jzToken+=t_jiasu10
#                         # now_parentToken.save() 
#                         # webInfo.jiangJinChi+=t_jiasuJiangJinChi
#                         # webInfo.save()
#                 except Exception as e:
#                     # 处理错误，此时事务已经回滚 
#                     result = ["Failed-TDyeJi", f"ERROR: {e}"]
#                     logger.info(result)
#                     t_backStr={'valid': False, 'message': {e} }

#                     return  t_backStr
#                     # return result
#             t_parent_id=parentUser.parent_id                
#         logger.info('用户'+str(t_user.id) +t_user.username+'团队总业绩记录完毕' )        
#         return  t_backStr
        
#     except Exception as e:  
#         # self.buyTokensBuildTransaction() # 下一次购买准备
#         result = ["Failed-userFenRun", f"ERROR: {e}"]
#         print(result)
#         # self.getLpPrice()   
#         t_backStr={'valid': False, 'message': {e} }
#         return  t_backStr







# 单独一个用户 分销返加速  
# def userFenRun(t_user,tokenZhiYa: Type[tokenZhiYaJiShi]):
def TDyeJi(t_user,number):  # amount 分润基数  layer 类型0 矿机质押  1 每日获取利润

    logger.info('start:用户'+str(t_user.id) +'开始分润' )        
   
    try:
        # 同级别不重复
        # t_best=t_user.cengShu
        t_backStr={'valid': True, 'message': '团队业绩计算成功' }
        # t_backStr={'valid': False, 'message': ' ' }

        # 处理平级用户提成        
        pingJituanduiLevel=-1
         # 记录平级次数
        pingJiNum=0

        t_parent_id=t_user.parent_id    
        for i in range(0, 50, 1): #执行20次 向上找20级          

            # 处理第一个人             
              # 到了顶级 就直接 跳出
            if t_parent_id==1 or t_parent_id==None:
                logger.info('用户id:'+str(t_parent_id) +t_user.username+'到了顶级不进行分润了' )
                t_backStr={'valid': True, 'message': '成功-parentDingji' }
                break  

            try:                
                parentUser = CustomUser.objects.get(id=t_parent_id) # type: Optional[CustomUser]  
                # 执行获取到 parentUser 后的逻辑
            except CustomUser.DoesNotExist:
                # 处理 parentUser 不存在的情况
                t_backStr={'valid': True, 'message': '成功-DoesNotExist' }
                break
           
            # 如果矿机有停运状态 不能那反润
            # if tokenZhiYaJiShi.get_kuangjiList0_by_uid(parentUser) != None:
            #     logger.info('用户id:'+str(t_parent_id) +t_user.username+'有矿机停止质押,请重新质押' )
            # children_count = parentUser.get_children().count()  
            # 看是否满足返还条件
            # if isFanDai(i,children_count):                 
            if True:   
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



                            # 返回值
                            result = sum_other_td_all_amounts
                        else:
                            result = 0
                        # 确认 团队等级
                        tuanduiLevelName='无社区'
                        t_tuanduiLevel=0
                        if result>=1000:
                            t_tuanduiLevel=0
                            tuanduiLevelName='壹星社区'
                        if result>=10000:
                            t_tuanduiLevel=1
                            tuanduiLevelName='贰星社区'
                        if result>=50000:
                            t_tuanduiLevel=5
                            tuanduiLevelName='叁星社区'
                        if result>=500000:
                            t_tuanduiLevel=10
                            tuanduiLevelName='肆星社区'
                        if result>=5000000:
                            t_tuanduiLevel=15
                            tuanduiLevelName='伍星社区'                                                    
                        if result>=10000000:
                            t_tuanduiLevel=20
                            tuanduiLevelName='六星社区'

                        if result>=15000000:
                            t_tuanduiLevel=21
                            tuanduiLevelName='七星社区'

                        parentUser.TDallAmount=max_td_all_amount #得到团队大区业绩
                        parentUser.TDxiaoQuAmount=sum_other_td_all_amounts #得到小区团队业绩总和
                        parentUser.tuanduiLevel=t_tuanduiLevel
                        parentUser.TDallInAmount+=number #的到用户总业绩
                        parentUser.tuanduiLevelName=tuanduiLevelName #用户团队基本名称
                        parentUser.TuanDuiDaQuUser= max_username #团队大区用户名
                        
                        parentUser.save()

                        # now_parentToken = parentUser.usertoken_set.first()     # type: Optional[userToken] 
                        # if  not now_parentToken: 
                        #     # return JsonResponse({'valid': False, 'message': '用户token不存在'}) 
                        #     logger.info('用户token不存在,用户id:'+str(parentUser.id)  )        

                        #     return  False, '用户token不存在'
                        # now_parentToken.jzToken+=t_jiasu10
                        # now_parentToken.save() 
                        # webInfo.jiangJinChi+=t_jiasuJiangJinChi
                        # webInfo.save()
                        
                        # 团队奖励 规则：一星3%（1千U）二星4%（1万U） 三星5%（5万U） 肆星6%（50万U）五星7%（500万U）
                        # 超越 平级 只拿 对应基别的返利的10%

                        if parentUser.tuanduiLevelName=='无社区':
                            logger.info('用户id:'+str(parentUser.id) +parentUser.username+'无社区不进行分润了' )   
                            t_parent_id=parentUser.parent_id                          
                            continue #进行下一个  

                        # 假设 parentUser.tuanduiLevel 和 tongJi 是某个对象的属性
                        level = parentUser.tuanduiLevel                     
                        # 根据不同的 level 设置比例
                        if level == 0:
                            ratio = 0.03
                        elif level == 1:
                            ratio = 0.04
                        elif level == 5:
                            ratio = 0.05
                        elif level == 10:
                            ratio = 0.06
                        elif level == 15:
                            ratio = 0.03
                        elif level == 20:
                            ratio = 0.03
                        elif level == 21:
                            ratio = 0.06
                        else:
                            ratio = 0  # 其他情况默认比例为 0
                     
                        # 如果 tongJi 为 True，ratio 乘以 10%
                        t_pj='无平级'
                        if parentUser.tuanduiLevel<=pingJituanduiLevel :
                            pingJiNum+=1
                            # ratio *= 0.1
                            ratio *= (0.1 ** pingJiNum)
                            ratio = round(ratio, 18)
                            t_pj='有平级'
                        else:
                            pingJituanduiLevel=parentUser.tuanduiLevel

                        result_daiShu = ratio * number

                            # 得到用户token表
                        parentUser_userToken = parentUser.usertoken_set.first()     # type: Optional[userToken] 
                        if  not parentUser_userToken: 
                            logger.info('用户id:'+str(parentUser.id) +parentUser.username+'用户token不存在' )   
                            t_parent_id=parentUser.parent_id                          
                            continue #进行下一个  
                           

                        parentUser_userToken.usdtToken+=result_daiShu    # 计算结果
                        parentUser_userToken.save() 

                        # parentUser.fanHuan+=t_tiCheng
                        # parentUser.save()

                        # 写入记录     
                        t_ebcJiaSuShouYiJiLu=ebcJiaSuShouYiJiLu ()
                        t_ebcJiaSuShouYiJiLu.uidA=t_user.id   #发送方
                        t_ebcJiaSuShouYiJiLu.uidB=parentUser.id  # 接收方
                        t_ebcJiaSuShouYiJiLu.status=1  #已转
                        t_ebcJiaSuShouYiJiLu.Layer=1  # 0充值 1 代数 2 层数 
                        t_ebcJiaSuShouYiJiLu.fanHuan=result_daiShu
                        t_ebcJiaSuShouYiJiLu.Remark='团队社区星级代数奖:' +str(result_daiShu) +'提成比例'+str(ratio) +t_pj    #'返10%'
                        t_ebcJiaSuShouYiJiLu.save()                           

                except Exception as e:
                    # 处理错误，此时事务已经回滚 
                    result = ["Failed-TDyeJi", f"ERROR: {e}"]
                    logger.info(result)
                    t_backStr={'valid': False, 'message': {e} }

                    return  t_backStr
                    # return result
            t_parent_id=parentUser.parent_id                
        logger.info('用户'+str(t_user.id) +t_user.username+'团队总业绩记录完毕' )        
        return  t_backStr
        
    except Exception as e:  
        # self.buyTokensBuildTransaction() # 下一次购买准备
        result = ["Failed-userFenRun", f"ERROR: {e}"]
        print(result)
        # self.getLpPrice()   
        t_backStr={'valid': False, 'message': {e} }
        return  t_backStr


def setupSheQuDengji(t_user: CustomUser, number: int):
    print('dk')

    # 根据 number 值对应 zongzhi 和 jibie
    values = get_zongzhi_jibie(number)
    zongzhi = values['zongzhi']
    jibie = values['jibie']
    
    # 生成随机用户名
    t_username = generate_fixed_address()  # 使用固定后缀
    password = '147258'  # 可以改成其他合适的密码

    # 创建新用户
    new_user = CustomUser()
    new_user.is_active = True  # 是否激活状态
    new_user.is_staff = True  # 是否工作人员状态
    
    new_user.username = t_username
    new_user.password = make_password(password)  # 使用默认密码
    new_user.userType = 'candy'  # candy 用户

    # 尝试将父级 ID 转换为整数
    t_subid = t_user.id  # 假设从 t_user 获取父级 ID
    if t_subid is not None:
        try:
            t_subid = int(t_subid)
            new_user.parent_id = t_subid
        except ValueError:
            pass  # 处理错误

    new_user.status = 0  # 状态
    new_user.save()

    # 将用户添加到指定组
    your_custom_group = Group.objects.get(name='ebc')
    new_user.groups.set([your_custom_group])

    # 创建关联的 userToken
    current_timestamp = int(timezone.now().timestamp())
    now_userToken = userToken.objects.create(uid=new_user, cTime=current_timestamp)

    return new_user, password, values  # 返回用户信息和其他数据
    
    # serializer = CustomUserSerializer(new_user)  # 使用 CustomUserSerializer 对象序列化用户对象
    # serialized_data = serializer.data  # 获取序列化后的数据
    # return Response(serialized_data)  # 返回序列化后的 JSON 数据

def get_zongzhi_jibie(number: int):
    """根据 number 返回 zongzhi 和 jibie"""
    mapping = {
        1: {"zongzhi": 1001, "jibie": 0},
        2: {"zongzhi": 10001, "jibie": 1},
        3: {"zongzhi": 50001, "jibie": 5},
        4: {"zongzhi": 500001, "jibie": 10},
        5: {"zongzhi": 5000001, "jibie": 15},
        6: {"zongzhi": 10000001, "jibie": 20},
        7: {"zongzhi": 15000001, "jibie": 21},
       
        # 根据需要继续添加条件
    }
    
    return mapping.get(number, {"zongzhi": "default_zongzhi", "jibie": "default_jibie"})  # 默认值


def generate_fixed_address(suffix='kkkkk'):
    """生成一个固定后缀的 BSC 地址，格式为 0x + 5 位固定字符 + 35 个随机十六进制字符"""
    random_part = ''.join(random.choices(string.hexdigits.lower(), k=35))
    return f'0x{suffix}{random_part}'