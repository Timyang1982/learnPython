@echo off &color 0a&setlocal enabledelayedexpansion&title %~n0
@mode con lines=60 cols=100


adb -s PRWWDIHYSCQ4AMN7 shell ls >nul

IF %ERRORLEVEL% ==0 goto 0
IF NOT %ERRORLEVEL% ==0 goto 1

:1
ECHO 手机未连接成功，请检查是否打开USB调试
pause>nul& exit


:0

echo 手机连接成功,启动
echo 启动微博自动浏览新闻脚本
echo.



ping -n 1 127.0.0.1>nul

adb -s PRWWDIHYSCQ4AMN7 shell < start_weibo.txt

::adb shell sh /sdcard/QQ_auto.sh

echo.
echo.







pause