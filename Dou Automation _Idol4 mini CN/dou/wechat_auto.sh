#! /system/bin/sh
# adb shell sh /mnt/sdcard/test/QQ2.sh

######################### 介绍和使用方法 ########################
#
# 介绍：采用循环输入和点击坐标来，循环发送消息
#
# 使用方法：
#		1.设置要发送多少条消息
#		2.设置发送键在手机上的坐标（可打开"setting->Developer options->point location（勾选），然后点击send键的位置查看）
#	
#################################################################


j=0;
while [ j -lt 30 ] # 1.设置要发送多少条消息
do 
	#input text Message
	input text '1'
	#input keyevent KEYCODE_SPACE
	#input text 00$j
	#echo "Input Message $j"
	#1320 1320 992 879
	input tap 660 705	#2.设置发送键在手机上的坐标，Rio4G-weixin&qq:440 420 ; Alto4.5:440 450 
	#echo `date +%T` >> sdcard/adb.txt
	sleep 60	#3.设置发送消息的间隔时间
	echo " "
	j=$(($j+1))
done 

echo "Test is over..."
