#! /system/bin/sh
#set -e

sleep 10
j=0;
while [ j -lt 20 ]
do 
	am start -a android.intent.action.CALL -d tel:10010   #2.打电话
	sleep 2
	input keyevent 26 
	sleep 178 #3.设置间隔时间	
	echo " "	
	j=$(($j+1))
done 

