
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



# 单独一个用户 分销返加速  
# def userFenRun(t_user,tokenZhiYa: Type[tokenZhiYaJiShi]):
def sheQuFenRun():  # amount 分润基数  layer 类型0 矿机质押  1 每日获取利润

    logger.info('start:社区分润开始。。。' )        
    #1.获取 需要分润数量
    now_webid = webInfo.objects.filter(webid=3).first()    
    t_fenRunNumber= now_webid.jiangJinChi
    # now_webid.jiangJinChi=now_webid.jiangJinChi+t_tiCheng
    # now_webid.save() 

    # 2. 全部用户收集 满足条件用户：小分区 大于3万的并去平级

    # try:
    #     t_user = User.objects.get(id=tokenZhiYa.uid_id)
    # except User.DoesNotExist:
    #     t_user = None
    #     logger.info('Failed:用户'+str(tokenZhiYa.uid)+ '不存在' )
    #     return 'no'
   
    try:  
        
        User.objects.get(id=1)
        # 同级别不重复
        t_best=t_user.cengShu

        t_parent_id=t_user.parent_id    
        # t_parent_id=t_user.id    
        for i in range(0, 10, 1): #执行10次 向上找10级        
            # 处理第一个人             
              # 到了顶级 就直接 跳出
            if t_parent_id==1 or t_parent_id==None:
                logger.info('用户id:'+str(t_parent_id) +t_user.username+'到了顶级不进行分润了' )
                break                        
            try:                
                parentUser = CustomUser.objects.get(id=t_parent_id)
                # 执行获取到 parentUser 后的逻辑
            except CustomUser.DoesNotExist:
                # 处理 parentUser 不存在的情况
                continue
            if parentUser.fanHuan is None:
                parentUser.fanHuan=0   
            # #  是否跨级
            if parentUser.cengShu <= t_best:
                logger.info('用户id:'+str(t_parent_id) +t_user.username+'低于反润级别拿不到代数分润' )
                continue
            t_best=parentUser.cengShu

            # 判断用户根据矿机个数是否可以得到反润级数
            if t_best-1 <=i :
                logger.info('用户id:'+str(t_parent_id) +t_user.username+'反润级别超过用户矿机级别' )
                continue
            # 如果矿机有停运状态 不能那反润
            if tokenZhiYaJiShi.get_kuangjiList_by_uid(parentUser) != None:
                logger.info('用户id:'+str(t_parent_id) +t_user.username+'有矿机停止质押,请重新质押' )




            children_count = parentUser.get_children().count()  
            # 看是否满足返还条件
            if isFanDai(i,children_count):                 
                try:
                    with transaction.atomic():                        
                        parentUser.fanHuan+=t_jiasu10
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
                        t_ebcJiaSuShouYiJiLu.fanHuan=t_jiasu10
                        t_ebcJiaSuShouYiJiLu.Remark='代数返奖励'+layerName+str(t_jiasu10)      #'返4.5%'    
                        t_ebcJiaSuShouYiJiLu.save()   
                        # 计入奖金池
                        # t_jiasuJiangJinChi

                        now_webid = webInfo.objects.filter(webid=3).first()    
                        now_webid.jiangJinChi=now_webid.jiangJinChi+t_jiasuJiangJinChi
                        now_webid.save()

                        # webInfo.jiangJinChi+=t_jiasuJiangJinChi
                        # webInfo.save()
                except Exception as e:
                    # 处理错误，此时事务已经回滚 
                    result = ["Failed-userFenRun", f"ERROR: {e}"]
                    logger.info(result)
                    return  False, {e}
                    # return result
            t_parent_id=parentUser.parent_id                
        logger.info('用户'+str(t_user.id) +t_user.username+'代级分润完成' )        
        return  True, '分润成功'
        
        
        # logger.info('用户'+str(t_user.id) +t_user.username+'层级分润开始' )
        # #  推广入金收益的1%个人加速
        # # t_jiasu1=t_user.userStakesB*1.5*0.01*0.01        
        # # t_jiasu1=tokenZhiYa.number*1.5*0.01*0.01        
        # t_jiasu1=0
        # if tokenZhiYa.layer==0:#矿机 计算            
        #     t_jiasu1=tokenZhiYa.number*1.5*0.01*0.01
        # if tokenZhiYa.layer==1:            
        #     t_jiasu1=tokenZhiYa.number*0.01

        
        # # 处理伞下1%
        # j=0
        # for i in islice(range(t_user.id-1, 0, -1),51): #islice  最多执行30次
        #     j=j+1
        #     # 处理第一个人
        #     # if i==t_user.id-1
        #     a_nodeUsers = CustomUser.objects.filter(pk=i)
        #     if not a_nodeUsers.exists():
        #         continue  
    
        #     a_nodeUser = a_nodeUsers.first()
        #     try:
        #         children_count = a_nodeUser.get_children().count()
        #     except Exception as e:
        #         print(f"Error: {e}")
        #     # children_count = a_nodeUser.get_children().count()   
        #     # 如果为真 ，那么给用户增加加速值1%
        #     if isFan(j,children_count): 
        #         try:
        #             with transaction.atomic():                        
        #                 a_nodeUser.fanHuan+=t_jiasu1
        #                 a_nodeUser.save()
        #                 # 增加记录
        #                 # 写入记录     
        #                 t_ebcJiaSuShouYiJiLu=ebcJiaSuShouYiJiLu ()
        #                 t_ebcJiaSuShouYiJiLu.uidA=t_user.id   #发送方
        #                 t_ebcJiaSuShouYiJiLu.uidB=a_nodeUser.id  # 接收方
        #                 t_ebcJiaSuShouYiJiLu.status=1  #已转
        #                 t_ebcJiaSuShouYiJiLu.Layer=2       # 伞下用户                 
        #                 t_ebcJiaSuShouYiJiLu.fanHuan=t_jiasu1
        #                 t_ebcJiaSuShouYiJiLu.Remark='层级返加速'+layerName+str(t_jiasu1)    
        #                 t_ebcJiaSuShouYiJiLu.save()  
        #         except Exception as e:
        #             # 处理错误，此时事务已经回滚 
        #             result = ["Failed-userFenRun", f"ERROR: {e}"]
        #             logger.info(result)
        # # 代数 和 层级 处理后 用户 状态为1 处理完成
        # tokenZhiYa.status=1
        # tokenZhiYa.save()
        # # t_user.status=1
        # # t_user.save()
        
        # logger.info('用户 id'+str(t_user.id) +t_user.username+'代级层级完成' )
        
    except Exception as e:  
        # self.buyTokensBuildTransaction() # 下一次购买准备
        result = ["Failed-userFenRun", f"ERROR: {e}"]
        print(result)
        # self.getLpPrice()   
    
    return 'ok'

# 是否返代级收益
def isFanDai(j,children_count):
    if j <= 0 and children_count >= 1:
        return True
    elif j <= 1 and children_count >= 2:
        return True
    elif j <= 2 and children_count >= 3:
        return True
    elif j <= 3 and children_count >= 4:
        return True      
    elif j <= 4 and children_count >= 5:
        return True
    elif j <= 5 and children_count >= 6:
        return True
    elif j <= 6 and children_count >= 7:
        return True
    elif j <= 7 and children_count >= 8:
        return True      
    elif j <= 8 and children_count >= 9:
        return True
    elif j <= 9 and children_count >= 10:
        return True  
    else:
        return False

# 是否返层级收益
def isFan(j,children_count):
    if j <= 5 and children_count >= 1:
        return True
    elif j <= 10 and children_count >= 2:
        return True
    elif j <= 15 and children_count >= 3:
        return True
    elif j <= 20 and children_count >= 4:
        return True
    elif j <= 25 and children_count >= 5:
        return True
    elif j <= 30 and children_count >= 6:
        return True
    elif j <= 35 and children_count >= 7:
        return True
    elif j <= 40 and children_count >= 8:
        return True
    elif j <= 45 and children_count >= 9:
        return True
    elif j <= 50 and children_count >= 10:
        return True
    else:
        return False
    
 



    
        
# 提现扣除数据库 数据
def tuanDuiRenShu(username):
    try: 
        # 如果 当前时间 小于 最后一次 加1.5% 的时间 那么应该 增加 并 扩展一天时间戳
        user = User.objects.filter(username=username).first()
        if user:
            #获得直推人数 
            children = user.get_children()     
            # 提取用户集合的名字
            # children_names = [child.username for child in children if child.status == 1]              
            # children_names = [child.username for child in children ]  
            children_names = [
                (child.username, "挖矿中" if child.status == 1 else "未挖矿") 
                for child in children
            ]            
            children_count = user.get_children().count()   
            # 获得全部后代人数
            get_descendants = user.get_descendants()     
            # 提取用户集合的名字          
            descendants_names = [
                (child.username, "挖矿中" if child.status == 1 else "未挖矿") 
                for child in get_descendants
            ]
            get_descendants_count=user.get_descendants().count()
            # total_records = len(get_descendants)

            # 获得包括自己的全部祖先节点
            # 共享人数
            userLast = CustomUser.objects.order_by('-id').first()
            gongXiangRenShu=userLast.id-user.id

            
            # 将变量保存到字典中
            result_dict = {
                'valid': True,
                'children_count': children_count,
                'children_names': children_names,  # 将用户集合的名字添加到字典
                'get_descendants': get_descendants_count,   #获得全部后代人数
                'descendants_names': descendants_names,  # 将用户集合的名字添加到字典
                'gongXiangRenShu':gongXiangRenShu,   #共享人数          
            }
        
            # t_js=JsonResponse({'valid': True, 'children_count': children_count,'get_descendants': get_descendants,'get_ancestors_include_self': get_ancestors_include_self,}) 
 
        return True, result_dict
    except Exception as e:  
            # self.buyTokensBuildTransaction() # 下一次购买准备
            result = ["Failed-everybadyFan", f"ERROR: {e}"]
            print(result)
            logger.info(result)        
            
            return False , result
            # self.getLpPrice()   
    
