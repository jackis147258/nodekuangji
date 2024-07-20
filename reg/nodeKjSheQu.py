
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
            users_with_high_tdxiaoqu_amount = CustomUser.objects.filter(TDxiaoQuAmount__gt=200)

            # # 获取所有用户的tuanduiLevel字段的计集合
            # tuandui_level_counts = users_with_high_tdxiaoqu_amount.values('tuanduiLevel').annotate(count=Count('tuanduiLevel'))
            # 获取所有用户的tuanduiLevel字段的计集合
            tuandui_level_counts = users_with_high_tdxiaoqu_amount.values('tuanduiLevel').annotate(count=Count('tuanduiLevel'))

            # 计算tuanduiLevel字段的合计值
            tuandui_level_sum = users_with_high_tdxiaoqu_amount.aggregate(total_tuanduiLevel=Sum('tuanduiLevel'))['total_tuanduiLevel']




            # 3. 计算每个用户应得的分润数量
            # user_count = users_with_high_tdxiaoqu_amount.count()
            if tuandui_level_sum > 0:
                per_user_fenRun = t_fenRunNumber / tuandui_level_sum
            else:
                per_user_fenRun = 0
            # 输出用户集合
            for t_user in users_with_high_tdxiaoqu_amount:
                # print(f"用户名: {user.username}, TDxiaoQuAmount: {user.TDxiaoQuAmount}")
                t_fenRunAll=t_user.tuanduiLevel*per_user_fenRun
                now_userToken = t_user.usertoken_set.first()     # type: Optional[userToken] 
                now_userToken.usdtToken+=t_fenRunAll 
                now_userToken.save()
                # 写入记录     
                t_ebcJiaSuShouYiJiLu=ebcJiaSuShouYiJiLu ()
                t_ebcJiaSuShouYiJiLu.uidA=0   #发送方 0平台整理后分配
                t_ebcJiaSuShouYiJiLu.uidB=t_user.id  # 接收方
                t_ebcJiaSuShouYiJiLu.status=1  #已转
                t_ebcJiaSuShouYiJiLu.Layer=1  # 0充值 1 代数 2 层数 
                t_ebcJiaSuShouYiJiLu.fanHuan=t_fenRunAll
                t_ebcJiaSuShouYiJiLu.Remark='社区奖励'+str(per_user_fenRun)      #'返4.5%'    
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
    logger.info('社区奖励完成' )        
    return  True, '分润成功' 


    
 
# 单独一个用户 分销返加速  
# def userFenRun(t_user,tokenZhiYa: Type[tokenZhiYaJiShi]):
def TDyeJi(t_user,t_number):  # amount 分润基数  layer 类型0 矿机质押  1 每日获取利润

    logger.info('start:用户'+str(t_user.id) +'开始分润' )        
   
    try:
        # 同级别不重复
        # t_best=t_user.cengShu
        t_backStr={'valid': True, 'message': '团队业绩计算成功' }
        # t_backStr={'valid': False, 'message': ' ' }


        t_parent_id=t_user.parent_id    
        # t_parent_id=t_user.id    
        for i in range(0, 10, 1): #执行10次 向上找10级        
            # 处理第一个人             
              # 到了顶级 就直接 跳出
            if t_parent_id==1 or t_parent_id==None:
                logger.info('用户id:'+str(t_parent_id) +t_user.username+'到了顶级不进行分润了' )
                t_backStr={'valid': True, 'message': '成功-parentDingji' }
                break                        
            try:                
                parentUser = CustomUser.objects.get(id=t_parent_id)
                # 执行获取到 parentUser 后的逻辑
            except CustomUser.DoesNotExist:
                # 处理 parentUser 不存在的情况
                t_backStr={'valid': True, 'message': '成功-DoesNotExist' }
                break
           
            # 如果矿机有停运状态 不能那反润
            # if tokenZhiYaJiShi.get_kuangjiList0_by_uid(parentUser) != None:
            #     logger.info('用户id:'+str(t_parent_id) +t_user.username+'有矿机停止质押,请重新质押' )
            children_count = parentUser.get_children().count()  
            # 看是否满足返还条件
            # if isFanDai(i,children_count):                 
            if True:   
                try:
                    with transaction.atomic():    

                        children = parentUser.get_children()                        
                        # 计算每个直推人的 TDallAmount 数量
                        td_all_amounts = [child.TDallAmount for child in children]

                        if td_all_amounts:
                            # 找到最大的 TDallAmount
                            max_td_all_amount = max(td_all_amounts)

                            # 计算其他人的 TDallAmount 总和
                            sum_other_td_all_amounts = sum(td_all_amounts) - max_td_all_amount

                            # 返回值
                            result = sum_other_td_all_amounts
                        else:
                            result = 0
                        # 确认 团队等级
                        t_tuanduiLevel=0
                        if result>30000:
                            t_tuanduiLevel=1
                        if result>50000:
                            t_tuanduiLevel=2
                        if result>100000:
                            t_tuanduiLevel=5
                        if result>300000:
                            t_tuanduiLevel=15
                        if result>500000:
                            t_tuanduiLevel=30

                        parentUser.TDallAmount+=t_number #得到团队总业绩
                        parentUser.TDxiaoQuAmount=result #得到小区团队业绩总和
                        parentUser.tuanduiLevel=t_tuanduiLevel
                        parentUser.save()

                        # now_parentToken = parentUser.usertoken_set.first()     # type: Optional[userToken] 
                        # if  not now_parentToken: 
                        #     # return JsonResponse({'valid': False, 'message': '用户token不存在'}) 
                        #     logger.info('用户token不存在,用户id:'+str(parentUser.id)  )        

                        #     return  False, '用户token不存在'
                        # now_parentToken.jzToken+=t_jiasu10
                        # now_parentToken.save()

                        # 写入记录     
                        t_ebcJiaSuShouYiJiLu=ebcJiaSuShouYiJiLu ()
                        t_ebcJiaSuShouYiJiLu.uidA=t_user.id   #发送方
                        t_ebcJiaSuShouYiJiLu.uidB=parentUser.id  # 接收方
                        t_ebcJiaSuShouYiJiLu.status=1  #已转
                        t_ebcJiaSuShouYiJiLu.Layer=1  # 0充值 1 代数 2 层数 
                        t_ebcJiaSuShouYiJiLu.fanHuan=t_number
                        t_ebcJiaSuShouYiJiLu.Remark='团队总业绩增加:'+str(t_number)      #'返4.5%'    
                        t_ebcJiaSuShouYiJiLu.save()   
                        # webInfo.jiangJinChi+=t_jiasuJiangJinChi
                        # webInfo.save()
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
    
     
