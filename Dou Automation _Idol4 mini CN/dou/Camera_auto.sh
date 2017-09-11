#! /system/bin/sh
######################### 介绍和使用方法 ########################
#
# 介绍：采用循环输入和点击坐标来，循环发送消息
#
# 使用方法：
#		1.设置要发送多少条消息
#		2.设置发送键在手机上的坐标（可打开"setting->Developer options->point location（勾选），然后点击send键的位置查看）
#		3.设置发送消息的间隔时间
#杀掉shell脚本进程：
#
#	adb shell ps |findstr "shell"
#	adb shell kill PID

#################################################################

sleep 10
j=0;
while [ j -lt 20 ] # 1.设置数量
do 
	input tap 370 1100 	#2.坐标
	sleep 30	#3.设置间隔时间
	echo " "
	j=$(($j+1))
done 

