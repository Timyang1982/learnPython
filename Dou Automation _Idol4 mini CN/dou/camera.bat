@echo off &color 0a&setlocal enabledelayedexpansion&title %~n0
@mode con lines=60 cols=100


adb -s PRWWDIHYSCQ4AMN7 shell ls >nul

IF %ERRORLEVEL% ==0 goto 0
IF NOT %ERRORLEVEL% ==0 goto 1

:1
ECHO �ֻ�δ���ӳɹ��������Ƿ��USB����
pause>nul& exit


:0

echo �ֻ����ӳɹ�,����
echo ����camera�Զ�����Ϣ�ű�
echo.



ping -n 1 127.0.0.1>nul

adb -s PRWWDIHYSCQ4AMN7 shell < start_camera.txt



echo.
echo.







pause