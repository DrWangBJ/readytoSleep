function istimeforsleep
c=Time'系统时间
a=#23:30:00# '定义时间段1
b=#23:59:59# '定义时间段2
d=#0:00:00# '定义时间段3
e=#9:17:00# '定义时间段4
If DateDiff("n",a,c)>0 And DateDiff("n",c,b)>0 Or DateDiff("n",d,c)>0 And DateDiff("n",c,e)>0 then '判断时间段
istimeforsleep=True
else
istimeforsleep=False
end if
end function

sub lockscreen
dim sl
set sl=wscript.CreateObject("wscript.shell")
'sl.popup "睡觉，再不睡觉，鸡都叫了",1, "睡觉",vbOKOnly or vbExclamation or vbSystemModal
'msgbox "睡觉，再不睡觉，鸡都叫了", vbOKOnly or vbExclamation or vbSystemModal, "睡觉"
sl.run "rundll32.exe user32.dll,LockWorkStation",0

end sub

CreateObject("WScript.Shell").Run "cmd /c lockscreen.bat",0

'if istimeforsleep then lockscreen

'set s = WScript.CreateObject("WScript.Shell")
'do While istimeforsleep
    'uacPrompt
    'runbat
'    lockscreen
'    WScript.sleep 100
'loop