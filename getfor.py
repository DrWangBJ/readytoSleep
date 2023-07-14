# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:11:55 2023

@author: spark
"""
from detectwnd2 import GetForheadWind
import time

def istime():
    print(time.ctime())
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    print(now_localtime)
    if "23:30:00" < now_localtime < "23:59:59" or "00:00:01" < now_localtime < "04:00:00" :
        print("in")
        return 1
    else:
        return 0

hand=GetForheadWind()
# istime()
while True:
    if istime():
        if hand.isLock():
            time.sleep(5)
        else:
            hand.Lock()
            time.sleep(10)
    else:
        time.sleep(60)
            
        
        

    
    

