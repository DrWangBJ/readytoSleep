# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 09:55:36 2023

@author: spark
"""
import ctypes
from ctypes import c_char_p
import time

class DetectWnd(object):
    _title=[u'哔哩哔哩',u'微博',u'[InPrivate]']
    _usetime=[10,5,10]
    _forbidtime=[120,120,360]
    
    def __init__(self):
        self.h = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\user32.dll")
        self.jj=u'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        self.Csp=c_char_p(self.jj.encode('gbk'))
        self.title=[]
        self.enable=[]
        self.antiTimer=[]
        self.showmsg1=[]
        self.showmsg2=[]
        self.hWnd=[]
        for it in self._title:
            self.title.append(it)
            self.enable.append(1)
            self.showmsg1.append(0)
            self.showmsg2.append(0)
            self.hWnd.append(-1)
        
        self.fen=[]
        for it in self._usetime:#许用分钟数
            self.fen.append(it)
            self.antiTimer.append(MyTimmer(it))

        # print(self.fen)
        
        self.forbidfen=[]
        self.forbidTimmer=[]
        for it in self._forbidtime:#禁用分钟数
            self.forbidfen.append(it)
            self.forbidTimmer.append(MyTimmer(it+0.5))


        
        
    def get_hWnd_hand(self):
        i=0
        for a in self.title:
            idx=-1
            hWnd=self.h.GetForegroundWindow()            
            # print(hWnd)
            self.h.GetWindowTextA(hWnd,self.Csp,ctypes.c_uint32(1000))            
            # print(self.Csp.value.decode('gbk'))
            b=self.Csp.value.decode('gbk')
            idx=b.find(a)
            # print(idx)
            # print(hWnd)
        #time.sleep(2)
            if idx<0:#没找到窗口目标
                print('not found')
                hWnd=-1
                self.h.GetWindowTextA(self.hWnd[i],self.Csp,ctypes.c_uint32(1000))
                b=self.Csp.value.decode('gbk')
                print(b)
                print(a)
                idx2=b.find(a)
                if idx2>=0:
                    print('old used')
                    hWnd=self.hWnd[i]
                else:
                    print('old missed')
            self.hWnd[i]=hWnd    
            # print(i)
            # print(hWnd)
            i=i+1
        return self.hWnd
    
    def msgbox(self,msg,msgtitle):
        self.h.MessageBoxTimeoutA(0,msg.encode('gbk'),msgtitle.encode('gbk'),0,0,3000)
        
        
    def mesg(self,idx):
        # print(idx)
        # print(self.showmsg1)
        # print(self.hWnd)
        if (self.showmsg1[idx]==0 and self.hWnd[idx]>0 and self.enable[idx]==1):
            #print('pop')
            msg=u'检测到打开了'+self.title[idx]+u',倒计时开始'
            self.msgbox(msg,u'倒计时提醒')
            self.showmsg1[idx]=1
            self.antiTimer[idx].start_count()
        
    def close_hWnd(self,idx):
        print('in close_hWnd')
        # print(self.enable[idx])
        print(self.hWnd)       
        if self.hWnd[idx]>0 and self.enable[idx]==0:
            #找到了窗口，并且它不被允许，下面要关掉它
            #self.h.SendMessageA(self.hWnd[i],ctypes.c_uint32(16),ctypes.c_uint32(0),ctypes.c_uint32(0))
            self.h.GetWindowTextA(self.hWnd[idx],self.Csp,ctypes.c_uint32(1000))
            b=self.Csp.value.decode('gbk')
            a=self.title[idx]
            id=b.find(a)
            msg=u'120分钟内不能再打开'+self.title[idx]+u'，否则直接关闭浏览器'
            self.msgbox(msg,u'禁用提示')
            print('id值是***********')
            print(id)
            if id>=0:
                #这是判断是否已经关闭过了，如果关闭过了，这里不会执行
                print('close')
                self.h.SendMessageA(self.hWnd[idx],ctypes.c_uint32(16),ctypes.c_uint32(0),ctypes.c_uint32(0))
                self.antiTimer[idx].counting=0
                
                    
    def closemsg(self,idx):
            msg=u'时间到，5s内关闭'+self.title[idx]+u'，否则直接关闭浏览器'
            self.msgbox(msg,u'关闭警告')
            # self.start_forbidclock()
            self.forbidTimmer[idx].start_count()
        
                
    def anticount(self):
        i=0
        for ti in self.antiTimer:
            print('ti counting value')
            print(ti.counting)
            ti.countUP()
            if self.antiTimer[i].isT()==1 and self.enable[i]==1 and self.showmsg2[i]==0:
                self.showmsg1[i]=0
                self.closemsg(i)
                self.showmsg2[i]=1
                self.enable[i]=0
            i=i+1
        # print(self.enable)
        # time.sleep(5)
        # cur_time=time.time()        
        # if (cur_time>self.anti_start+self.fen*60 and self.enable==1 and self.hWnd>0 and self.showmsg2==0):
        #     #time.sleep(self.fen*60)
        #     self.showmsg1=0
        #     self.closemsg()
        #     self.showmsg2=1
        #     time.sleep(5)
        #     self.enable=0
        #     #self.enable=0
        #     #time.sleep(30)
        
          
    def forbid(self):
        i=0
        for T in self.forbidTimmer:
            print('now is forbid countting')
            T.countUP()
            # time.sleep(5)
            # cur_time=time.time()
            # print('in forbid cur_time')
            # print(cur_time)
            # print('forbidfen')
            # print(self.start_time+self.forbidfen*60)
            
            #if cur_time<(self.start_time+self.forbidfen*60) and self.enable==0:#表示还没到时间，此时间段不能开窗口
            if T.isT()==0:#计时未结束，不能打开，打开就关闭
                print('ready to close')
                # self.enable[i]=0
                print(self.enable)
                self.close_hWnd(i)
                # self.get_hWnd_hand()
                # self.close_hWnd(i)
                self.showmsg2[i]=0
                
            else:
                self.enable[i]=1
                # print('keep running')
                # self.showmsg1=0
                # self.showmsg2=0
            i=i+1
        
        
class MyTimmer(object):
    def __init__(self,m):
        self.len=m
        self.last_time=0
        self.current_time=time.time()
        self.start_time=time.time()
        self.TimeUP=0
        self.counting=0
        
    def freshtime(self):
        self.last_time=self.current_time
        self.current_time=time.time()
        
    def setStart(self):
        self.start_time=time.time()
        self.TimeUP=0
        
    def countUP(self):
        if self.counting==1:
            self.freshtime()
            # print('time update')
            print('已过时间：')
            print(self.current_time-self.start_time)
        else:
            self.setStart()
            # print('start time update')
            #self.counting=1
            
        if self.current_time-self.start_time>=self.len*60:
            self.TimeUP=1
            self.counting=0
            
    def start_count(self):
        self.setStart()
        self.counting=1
            
    def isT(self):
        return self.TimeUP
        
class GetForheadWind():
    def __init__(self):
        self.h = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\user32.dll")
        self.jj=u'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        self.Csp=c_char_p(self.jj.encode('gbk'))

    def isLock(self):
        idx=-1
        hWnd=self.h.GetForegroundWindow()            
        # print(hWnd)
        if hWnd>0:
            self.h.GetWindowTextA(hWnd,self.Csp,ctypes.c_uint32(1000))            
        # print(self.Csp.value.decode('gbk'))
            b=self.Csp.value.decode('gbk')
            idx=b.find(u'Windows 默认锁屏界面')
        else:
            idx=-1
        # print(idx)
    #     # print(hWnd)
    # #time.sleep(2)
    #     if idx<0:#没找到窗口目标
    #         print('not found')
    #         hWnd=-1
    #         self.h.GetWindowTextA(self.hWnd[i],self.Csp,ctypes.c_uint32(1000))
    #         b=self.Csp.value.decode('gbk')
    #         print(b)
    #         print(a)
    #         idx2=b.find(a)
    #         if idx2>=0:
    #             print('old used')
    #             hWnd=self.hWnd[i]
    #         else:
    #             print('old missed')
    #     self.hWnd[i]=hWnd    
    #     # print(i)
    #     # print(hWnd)
    #     i=i+1
        return idx+1    
    
    def Lock(self):
        self.h.LockWorkStation()
    