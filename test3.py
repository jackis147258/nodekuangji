import requests




pingJiNum=0
for i in range(0, 5, 1): #执行20次 向上找20级           
    pingJiNum+=1
    # pingJiNum = 3  # 假设初始值为1
    ratio = 1.0    # 初始的比例值

    # 使用指数运算，根据 pingJiNum 直接计算 ratio
    ratio *= (0.1 ** pingJiNum)
    ratio = round(ratio, 15)

    print(f"计算后的 ratio 值为: {ratio}")
 
