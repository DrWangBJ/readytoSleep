function istimeforsleep
c=Time'ϵͳʱ��
a=#23:30:00# '����ʱ���1
b=#23:59:59# '����ʱ���2
d=#0:00:00# '����ʱ���3
e=#9:17:00# '����ʱ���4
If DateDiff("n",a,c)>0 And DateDiff("n",c,b)>0 Or DateDiff("n",d,c)>0 And DateDiff("n",c,e)>0 then '�ж�ʱ���
istimeforsleep=True
else
istimeforsleep=False
end if
end function

sub lockscreen
dim sl
set sl=wscript.CreateObject("wscript.shell")
'sl.popup "˯�����ٲ�˯������������",1, "˯��",vbOKOnly or vbExclamation or vbSystemModal
'msgbox "˯�����ٲ�˯������������", vbOKOnly or vbExclamation or vbSystemModal, "˯��"
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