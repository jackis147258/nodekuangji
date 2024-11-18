import time 
import datetime
from web3 import Web3
import GetTokens
from abi import tokenAbi

ebcOld_TOKEN_ADDRESS = '0x10E5a77Af4AB39eEF8393fCb2f8cfDe1971857Fb' 
newEbc_TOKEN_ADDRESS = '0xcEa2729fE4D4cEEB74113DE43B607cF57467ef8b' 
maticKey = '0x2799ec259402332b67159fb89bfb436f0d01f35cb9ea991c9923a480f87f50d3'

class DefiAuto:
    def __init__(self):        
        bsc ='https://rpc.ankr.com/polygon/145b63c3aa3fc77ce3d05be2c9f1caba16322f6957f8c975d05da3fe08c110f5'    
        self.web3 = Web3(Web3.HTTPProvider(bsc)) 
        self.TokenToSellAddress = self.web3.to_checksum_address(ebcOld_TOKEN_ADDRESS)
        self.newTokenToSellAddress = self.web3.to_checksum_address(newEbc_TOKEN_ADDRESS)

        try:
            sellTokenAbi = tokenAbi(self.TokenToSellAddress) 
            newTokenToSellAddressAbi = tokenAbi(self.newTokenToSellAddress) 
            self.contractSellToken = self.web3.eth.contract(self.TokenToSellAddress, abi=sellTokenAbi)                    
            self.contractNewSellToken = self.web3.eth.contract(self.newTokenToSellAddress, abi=newTokenToSellAddressAbi)
        except Exception as e:    
            result = ["Failed -InitializeTrade", f"ERROR: {e}"]
            print(result) 

    def oldEbc2NewEbc(self):
        maticKeyAddr = self.web3.eth.account.from_key(maticKey)   
        tokenList = []
        
        for myToken in GetTokens.tokenList: 
            gasAccountWallet = self.web3.to_checksum_address(myToken['token'])
            successful = False  # 用于跟踪当前 token 是否处理成功
            
            while not successful:  # 重复处理直到成功
                try:
                    # 获取用户信息
                    _userStakeA = self.contractSellToken.functions._userStakeA(gasAccountWallet).call() 
                    _userStakeB = self.contractSellToken.functions._userStakeB(gasAccountWallet).call() 
                    # ...（省略其他调用）

                    # 构建交易
                    token_txn = self.contractNewSellToken.functions.stakeTestSet(
                        gasAccountWallet,
                        _userStakeA, 
                        _userStakeB, 
                        # 其他参数
                    ).build_transaction({
                        'chainId': 137,
                        'gas': 6000000,
                        'gasPrice': self.web3.eth.gas_price,
                        'nonce': self.web3.eth.get_transaction_count(maticKeyAddr.address),
                    })
                    
                    signed_txn = self.web3.eth.account.sign_transaction(token_txn, private_key=maticKey)
                    tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)             

                    time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    result = [time1, '数据转移成功:', gasAccountWallet, 'token:', myToken['token'], self.web3.to_hex(tx_hash)]
                    tokenList.append(result)
                    print(result)

                    time.sleep(20)
                    successful = True  # 标记处理成功

                except Exception as e:
                    result = ["Failed-transfer_bnbGas", f"ERROR: {e}"]
                    print(result)
                    time.sleep(5)  # 等待一段时间后重试
                    # 继续处理当前 token

        result = ['全部数据转移', len(tokenList), '个']
        print(result)
        return 'ok'

def getOld():
    print('abc')
    defi = DefiAuto()
    defi.oldEbc2NewEbc() 

if __name__ == "__main__":
    getOld()
