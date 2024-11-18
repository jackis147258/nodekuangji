
# Create your views here.
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from reg.forms import SignUpForm,UserMoveForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import  Group

 # Create your views here.
from reg.serializers import CourseSerializer,CustomUserSerializer,ebcJiaSuShouYiJiLuSerializer,tokenZhiYaJiShiSerializer ,payTokenSerializer,webInfoSerializer
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import JsonResponse
from reg.models import CustomUser,userToken,ebcJiaSuShouYiJiLu ,tokenZhiYaJiShi,payToken 
from django.contrib.auth import get_user_model
# from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from apiV1.DeFi2.ebcTiXian import dfEbcTixian
from config import EbcContractTokenAddress
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

# from mptt.utils import move_to
# from mptt.models import move_to
 
import logging
logger = logging.getLogger(__name__)

import asyncio

from django.contrib.auth import get_user_model
User = get_user_model()


from django.http import JsonResponse
# from django_redis import get_redis_connection
from datetime import datetime, timedelta


from typing import Optional
from django.db import transaction
from django.utils import timezone

import hashlib
import time
import hmac
 
from eth_account import Account
from eth_account.messages import encode_defunct

from Crypto.Hash import keccak
import eth_abi
from eth_utils import to_bytes
from eth_utils import to_bytes, to_checksum_address

from app1.models import webInfo
from web3 import Web3
from django.db.models import Q
from reg.shengji import GetTokensTxt 
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=4)



class upToken(object):    
    # def __init__(self):        
      
        
    #     try:
        
    #     except Exception as e:    
    #         result = ["Failed -InitializeTrade", f"ERROR: {e}"]
    #         print(result) 
    
    def addZongZhi(self,TDallInAmount,tuanduiLevel, userPAddr, user1Addr, user2Addr): # 转gas 费给地址    
        print(TDallInAmount)    
        user1Addr.TDallInAmount=TDallInAmount   # 团队全部总值
        user1Addr.save()     
        user2Addr.TDallInAmount=TDallInAmount   # 团队全部总值
        user2Addr.save()     
        userPAddr.TDallAmount=TDallInAmount   #  团队大区总值
        userPAddr.TDxiaoQuAmount=TDallInAmount   # 团队小区总值
        userPAddr.tuanduiLevel=tuanduiLevel   # 团队小区总值
        
        userPAddr.save()     
         
     # 给账号 转bnb
    def shengji(self): # 转gas 费给地址   
            # tokenList=[]
            for myToken in GetTokensTxt.tokenList:  
            
                # while not successful:  # 重复处理直到成功
                with transaction.atomic():

                    try:
                     
                        # gasAccountWallet = self.web3.to_checksum_address(myToken['userAddr'])

                        userPAddr = User.objects.filter(username=myToken['userPAddr']).first()  # type: Optional[CustomUser] 
                        if not userPAddr:
                            print({'valid': False, 'message': '用户不存在:'.myToken['userPAddr']})
                            break
                        user1Addr = User.objects.filter(username=myToken['user1Addr']).first()  # type: Optional[CustomUser] 
                        if not user1Addr:
                            print({'valid': False, 'message': '用户不存在:'.myToken['user1Addr']})
                            break
                        user2Addr = User.objects.filter(username=myToken['user2Addr']).first()  # type: Optional[CustomUser] 
                        if not user2Addr:
                            print({'valid': False, 'message': '用户不存在:'.myToken['user2Addr']})
                            break                        
                        xingJi=int(myToken['xingJi'])
                        if xingJi==0:  #1星
                            self.addZongZhi(1001,0,userPAddr,user1Addr,user2Addr)
                            print({'valid': True, 'message': userPAddr.username+'-1星设置成功'})
                            continue
                        if xingJi==1:#1星
                            self.addZongZhi(10001,1,userPAddr,user1Addr,user2Addr)
                            print({'valid': True, 'message': userPAddr.username+'-2星设置成功'})
                            continue
                        if xingJi==5:#1星
                            self.addZongZhi(50001,5,userPAddr,user1Addr,user2Addr)
                            print({'valid': True, 'message': userPAddr.username+'-3星设置成功'})
                            continue
                        if xingJi==10:#1星
                            self.addZongZhi(500001,10,userPAddr,user1Addr,user2Addr)
                            print({'valid': True, 'message': userPAddr.username+'-4星设置成功'})
                            continue
                        if xingJi==15:#1星
                            self.addZongZhi(5000001,15,userPAddr,user1Addr,user2Addr)
                            print({'valid': True, 'message': userPAddr.username+'-5星设置成功'})
                            continue
                        if xingJi==20:#1星
                            self.addZongZhi(10000001,20,userPAddr,user1Addr,user2Addr)
                            print({'valid': True, 'message': userPAddr.username+'-6星设置成功'})
                            continue
                        if xingJi==21:#1星
                            self.addZongZhi(15000001,21,userPAddr,user1Addr,user2Addr)
                            print({'valid': True, 'message': userPAddr.username+'-7星设置成功'})
                            continue 

                    except Exception as e: 
                         
                        print(f"ERROR: {e}") 
                        break   

            result=['全部数据转移',len(GetTokensTxt.tokenList),'个' ]
            print(result)
            return 'ok' 

def getOld():
    # 得到old数据列表    
    print('abc')
    defi= upToken()
    defi.shenji() 
    
if __name__ == "__main__":
    getOld()
   