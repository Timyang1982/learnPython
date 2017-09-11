"""Camera library for scripts.
"""

import os
import subprocess
import ConfigParser
import time

from configs import GetConfigs,Configs
from configs import AppConfig
from automator.uiautomator import Device

#def Wi_Fi_connect_device(ip):

    #pidlist = returnValue.split("\n")
def connect_device(device_name,logger):
    """connect_device(device_id) -> Device
    Connect a device according to device ID.
    """
    environ = os.environ
    device_id = environ.get(device_name)
    if device_id == None:
        device_id = device_name
    backend = Configs("common").get("Info","backend")
    logger.info("Device ID is " + device_id + " backend is " + backend)
    if backend.upper() == "MONKEY":
        device = globals()["%sUser"%backend](device_id)
    else:
        device = Device(device_id)
    if device is None:
        logger.critical("Cannot connect device.")
        raise RuntimeError("Cannot connect %s device." % device_id)
    return device

def auto(weibo_auto_command):
        # start Weibo_auto shell
        #self.logger.info("auto start")
        #weibo_auto_command = "adb -s "+self.m_device+" shell sh /storage/sdcard1/Weibo_auto.sh"
        #weibo_auto_command = "adb shell sh /storage/sdcard1/Weibo_auto.sh"
        #subprocess.Popen(weibo_auto_command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.Popen(weibo_auto_command)
        #os.popen(weibo_auto_command)
        # p=subprocess.Popen(weibo_auto_command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # returnValue= p.communicate()[0]
        #self.logger.info("shellpid info:%s"%returnValue)
        #self.logger.info("weibo shell start")

class Dou(object):
    def __init__(self,device,logger):
        self.config = ConfigParser.ConfigParser()
        self.logger = logger
        self.m_device = device        
        self.appconfig = AppConfig("appinfo")
        if isinstance(device, Device):
            self.device = device
        else:
            self.device = connect_device(device,self.logger)
        self.config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"configure","common.ini"))
        self.phoneNumber = self.config.get("Telephony","phoneNumber")
        self.relayPort = self.config.get("Default","RelayPort")
        self.relaySerial = self.config.get("Default","RelaySerial")


    def start_app(self,name,b_desk=True):
        '''Call/People/ALL APPS/Messaging/Browser'''
        self.logger.debug("start app:%s" %(name))
        self.device.press.home()
        self.device.delay(2)
        if b_desk and self.device(description=name).wait.exists(timeout = 5000):
            self.logger.debug("%s exists"%name)
            self.device.delay(2)
            self.device(description=name).click()
            return True
        elif self.device(description="ALL APPS").exists:
            self.logger.debug("enter ALL APPS.")
            self.device(description="ALL APPS").click()
            #self.device().fling.horiz.toBeginning()

            '''for loop in range(5):
                self.device.swipe(540,560,540,1400,steps=20)
                self.device.delay(2)'''

            for loop in range(10):
                if self.device(description=name).exists:
                    self.device(description=name).click()
                    return True
                self.device.swipe(540,1400,540,560,steps=20)
        return False

    def Wi_Fi_isconnect(self):
        is_connect = 'adb shell dumpsys wifi ps | more'      
        p = subprocess.Popen(is_connect, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        returnValue= p.communicate()[0]
        self.logger.info("wifi info:%s"%returnValue)
        wifi_info_list = returnValue.split("\n")
        
        for loop in range(len(wifi_info_list)):
            self.logger.debug("loop:%s"%loop)
            if "Wi-Fi is enabled" in wifi_info_list[loop]: 
                self.logger.info("wifi is open")			
                return True
                break
            else:
                self.logger.info("wifi is close")
                return False
        
    def Wi_Fi_connect(self):
        ip = self.get_ip()
        command_port = "adb tcpip 5555"
        os.system(command_port)
        self.logger.info("5")
        time.sleep(5)
        self.logger.info("set port")
        self.closeRelay()
        command_ip = "adb connect %s" %ip 
        os.system(command_ip)
        self.logger.info("wifi connect ok")
		
    def get_ip(self):
        ip_command = 'adb shell dumpsys wifi | findstr "ip_address"'
        p = subprocess.Popen(ip_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ip_info = p.communicate()[0]
        self.logger.info('ip_info   %s' %ip_info)
        ip_address_strip = (str(ip_info)).strip()
        ip_address = ip_address_strip.strip("ip_address=")
        self.logger.info('ip_address   %s' %ip_address)        
        return ip_address

        
    def closeRelay(self):         
        print self.relaySerial
        print self.relayPort
        command = "CommandApp_USBRelay  "+self.relaySerial+" close "+self.relayPort
        os.system(command)        
        self.logger.info("close the relay")

    def openRelay(self):
        command = "CommandApp_USBRelay  "+self.relaySerial+" open "+self.relayPort
        os.system(command)
        self.logger.info("open the relay")

    def clearapp(self):
        self.logger.debug('clear all recent app')
        subprocess.Popen('adb shell input keyevent 187')
        self.device.delay(1)
        if self.device(resourceId="com.android.systemui:id/recents_clearall_button").exists:
            self.device(resourceId="com.android.systemui:id/recents_clearall_button").click()
            self.device.delay(2)
        self.device.press.back()
        self.device.press.home()

    def enterMusic(self):
        """Launch music by StartActivity.
        """          
        self.logger.debug('enter music')
        if self.device(resourceId=self.appconfig("Music","id_serach")).wait.exists(timeout = 5000):
            self.logger.info('enter music success!')
            return True
        self.start_app("Mix",b_desk=False)

        if self.device(resourceId=self.appconfig("Music","id_serach")).wait.exists(timeout = 5000):
            self.logger.info('enter music success!')
            return True
        else:
            self.logger.warning('enter music fail!')
            #self.save_fail_img()
            return False

    def enterBrowser(self):
        self.logger.debug('enter browser')
        if self.device(resourceId=self.appconfig("Browser","id_url")).wait.exists(timeout = 5000):
            self.logger.warning('enter Browser success!')
            return True
        self.start_app("Browser",b_desk=False)

        if self.device(resourceId=self.appconfig("Browser","id_url")).wait.exists(timeout = 5000):
            self.logger.warning('enter Browser success!')
            return True
        else:
            self.logger.warning('enter Browser fail!')
            #self.save_fail_img()
            return False

    def enterCamera(self):
        self.logger.debug('enter camera')
        if self.device(resourceId=self.appconfig("Camera","id_shutter")).wait.exists(timeout = 5000):
            self.logger.warning('enter camera success!')
            return True
        self.start_app("Camera",b_desk=False)

        if self.device(resourceId=self.appconfig("Camera","id_shutter")).wait.exists(timeout = 5000):
            self.logger.info('enter camera success!')
            return True
        else:
            self.logger.warning('enter camera fail!')
            #self.save_fail_img()
            return False

    def enterMap(self):
        self.logger.debug('enter baidu map')
        if self.device(resourceId="com.tct.launcher:id/workspace").exists:
            self.logger.debug("baidu map exists")
            self.device(className="android.widget.TextView",index=0).click()

        if self.device(resourceId=self.appconfig("Map","id_searchbox")).wait.exists(timeout = 5000):
            self.logger.warning('enter baidu map success!')
            self.logger.warning('enter baidu map success!')
            return True
        else:
            self.logger.warning('enter baidu map fail!')
            #self.save_fail_img()
            return False

    def enterWeibo(self):
        self.logger.debug('enter sina weibo')
        if self.device(description=self.appconfig("Sina","id_discover")).wait.exists(timeout = 10000):
            self.logger.info('enter weibo success!')
            return True
        self.start_app("Weibo",b_desk=True)

        if self.device(description=self.appconfig("Sina","id_discover")).wait.exists(timeout = 10000):
            self.logger.info('enter weibo success!')
            return True
        else:
            self.logger.warning('enter weibo fail!')
            #self.save_fail_img()
            return True

    def enterTencentVideo(self):
        self.logger.debug('enter tencent video')

        if self.device(resourceId=self.appconfig("Tencent","id_download_cancel")).wait.exists(timeout = 10000):
            self.device(resourceId=self.appconfig("Tencent","id_download_cancel")).click()

        if self.device(resourceId=self.appconfig("Tencent","id_search")).wait.exists(timeout = 10000):
            self.logger.info('enter tencent video success!')
            return True
        self.start_app("Tencent Video",b_desk=True)

        if self.device(resourceId=self.appconfig("Tencent","id_search")).wait.exists(timeout = 10000):
            self.logger.info('enter tencent video success!')
            return True
        else:
            self.logger.warning('enter tencent video fail!')
            #self.save_fail_img()
            return True
        return true

    def enterGame(self):
        self.logger.debug("enter NeedForSpeed")
        self.start_app("Hot Pursuit",b_desk=True)
        self.logger.info('enter NeedForSpeed  success!')
        return True

    def enterWechat(self):
        self.logger.debug('enter wechat')

        if self.device(resourceId="android:id/action_bar").wait.exists(timeout = 5000):
            self.logger.info("enter wechat success")
            return True

        self.start_app("WeChat",b_desk=True)

        if self.device(resourceId="android:id/action_bar").wait.exists(timeout = 5000):
            return True
        else:
            self.logger.warning('enter wechat fail!')
            #self.save_fail_img()
            return True


    def play_music(self,times,testloop):
        try:
            self.logger.info("Play music start")
            self.setDisplay15s()
            self.device.delay(1)
            music_battery = 0
            self.start_activity('com.alcatel.music5.china','com.alcatel.music5.activities.BaseMusicPlayerActivity')
            self.device.delay(5)            

            if self.device(resourceId="com.alcatel.music5.china:id/track_play_pause_image_btn").exists:
                self.device(resourceId="com.alcatel.music5.china:id/track_play_pause_image_btn").click()
                self.logger.info("CLICK id")
            else:
                self.logger.debug("com.alcatel.music5.china:id/track_play_pause_image_btn not exits.")
                self.device.click(550,1220)

            self.device.delay(3)
            #self.device.press.home()
            # if self.is_playing_music():
            self.logger.info("Playing Music 30 mins.")
            #self.device.press.power()
            battery_start = self.get_battery()
            self.logger.info("battery_start: %s" %battery_start)
            command = "adb shell dumpsys batterystats --reset"
            os.system(command)
            command = "adb shell dumpsys batterystats enable full-history"
            os.system(command)                      
			
            self.closeRelay()

            self.device.delay(60*times)

            self.openRelay()
            self.device.delay(2)
            
            date  = time.strftime("%H-%M-%S", time.localtime())
            print "date is %s" %date
            filename = "D:/batterystats.%s.music.txt" %date
            logfile = open(filename,"w")
            command = "adb shell dumpsys batterystats" 
            subprocess.Popen(command, shell=True, stdout=logfile, stderr=subprocess.PIPE)
            #stop playing music

            battery_finish = self.get_battery()
            self.logger.info("battery_finish: %s" %battery_finish)
            self.device.press.home()
            self.device.delay(3)
            self.setDisplayNever()
            self.start_activity('com.alcatel.music5.china','com.alcatel.music5.activities.BaseMusicPlayerActivity')
            
            self.logger.info("stop playing music")
            self.device.delay(3)
            if self.device(resourceId="com.alcatel.music5.china.debug:id/track_play_pause_image_btn").exists:
                self.device(resourceId="com.alcatel.music5.china.debug:id/track_play_pause_image_btn").click()
                self.logger.info("stop id")
            else:
                self.logger.debug("com.alcatel.music5.china.debug:id/track_play_pause_image_btn not exits.")
                self.device.click(550,1220)
                self.logger.info("stop ")
                
            self.device.delay(1)
            
            self.updateResult("music_battery",battery_finish,testloop)

            music_battery = int(battery_start)-int(battery_finish)
            self.logger.info("music_battery: %s" %music_battery)
        except Exception,e:
            self.logger.error(e)
            #self.save_fail_img()

        self.device.press.home()
        #self.setDisplayNever()

        return music_battery

    def is_playing_music(self):
        """check if music is playing or not.
        """
        data = self.device.server.adb.shell("dumpsys media_session")
        if not data:
            return None
        if "state=PlaybackState {state=3" in data:
            self.logger.debug("The music is playing now")
            return True
        else:
            self.logger.debug("The music is not playing.")
            return False

    def _exit(self):
        """exit music 
        """
        self.back_to_home()
        if self.device(packageName = self.appconfig("Music","package")).wait.gone(timeout = self.timeout):
            return True
        return False
    
    def closeMusic(self):
        """close music 
        """
        self.logger.debug('close music')
        if self.is_playing_music():
            self.logger.debug('Stop music play')
            self.device(resourceId=self.appconfig("Music","id_pause")).click()
            self.device.delay(1)
            self.device.press.home()
        return True

    def start_activity(self,packet,activity):
        data = self.device.server.adb.shell("am start -n %s/%s"%(packet,activity))
        if data.find("Error")>-1:
            self.logger.error("Fail: %s/%s" %(packet,activity))
            return False
        self.logger.info("start_activity %s success."%activity)
        return True

    def browser_test(self,times,testloop):
        try:
            #self.setDisplayNever()
            self.logger.debug("Browser test start")
            browser_battery = 0
            self.start_activity("com.android.browser","com.tencent.mtt.MainActivity")
            self.device.delay(5)
            # if self.enterBrowser():
            
            #self.music.play()#
            self.device.click(320, 90)
            subprocess.Popen("adb shell input text %s" %(self.appconfig("Browser","websit")))
            #self.device.shell_adb("shell input text %s" )
            self.device.delay(5)
            self.device.press.enter()
            self.device.delay(1)
			
            battery_start = self.get_battery()
            self.logger.info("battery_start: %s" %battery_start)
			
            command = "adb shell dumpsys batterystats --reset"
            os.system(command)
            command = "adb shell dumpsys batterystats enable full-history"
            os.system(command)  
			
            #browse website 30mins and close the relay
            self.closeRelay()
            self.logger.debug("browse website 30 mins.")
            self.device.delay(60*times)

            #browse website over and open the relay
            self.openRelay()
            self.device.delay(2)
            #self.device = connect_device(self.m_device,self.logger)            
            
            battery_finish = self.get_battery()
            date  = time.strftime("%H-%M-%S", time.localtime())
            print "date is %s" %date
            filename = "D:/batterystats.%s.browser.txt" %date
            logfile = open(filename,"w")
            command = "adb shell dumpsys batterystats" 
            subprocess.Popen(command, shell=True, stdout=logfile, stderr=subprocess.PIPE)
			
            self.logger.info("battery_finish: %s" %battery_finish)
            browser_battery = int(battery_start)-int(battery_finish)
            self.updateResult("browser_battery",battery_finish,testloop)

            self.logger.info("browser_battery: %s" %browser_battery)
            self.device.press.home()
            self.device.delay(2)
        except Exception,e:
            self.logger.error(e)
            #self.save_fail_img()

        return browser_battery

    def Call_test(self,times,testloop,networktype):
        try:            
            
            self.logger.debug("test call start") 
            self.setDisplay15s()		
            camera_battery = 0
			
            command = "adb shell dumpsys batterystats --reset"
            os.system(command)
            command = "adb shell dumpsys batterystats enable full-history"
            os.system(command)
			
            battery_start = self.get_battery()
            self.logger.info("battery_start: %s" %battery_start)
            self.device.delay(1)                   
            
            '''if networktype:
                self.openwifi()
            ip_add = self.get_ip()
            ip_addressandport = ip_add + ":5555"
            
            self.Wi_Fi_connect()	            
            ip_devices = Device(ip_addressandport)
            ip_devices.press.home()
            if ip_devices(resourceId="com.tct.launcher:id/page_indicator").exists:                
            	pass	
            call_battery=0
            
            #battery_start = 0
            battery_finish = 0
            devices_id = self.config.get("Telephony","deviceId")
            self.config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"configure","common.ini"))
            phoneNumber = self.config.get("Telephony","phoneNumber")

            command = "adb -s "+ ip_addressandport +" shell am start -a android.intent.action.CALL -d tel:"+phoneNumber
            self.logger.debug("phoneNumber:%s"%phoneNumber)           
            print time.strftime('%Y-%m-%d %H:%M:%S') 
			
            for loop in range(times):                
                battery_start_loop = self.get_call_battery(ip_addressandport)                
                self.logger.info("battery_start: %s" %battery_start_loop)
                for i in range(5):
                    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    returnValue= p.communicate()[0]
                    self.logger.debug("returnValue:%s"%returnValue)
                    if "Starting: Intent" in returnValue:
                        self.logger.info("Call success")
                        #self.closeRelay()
                        break                    
                #self.device.delay(3*60)
                time.sleep(3*60)          
                #self.device.wakeup()
                
                battery_finish = self.get_call_battery(ip_addressandport)   
                battery_finish_loop = self.get_call_battery(ip_addressandport)   
                self.logger.info("battery_finish_loop: %s" %battery_finish_loop)

                call_battery_loop = int(battery_start_loop)-int(battery_finish_loop)
                call_battery = call_battery + call_battery_loop	 
                if ip_devices(resourceId="com.android.dialer:id/floating_end_call_action_button").exists:
                    ip_devices(resourceId="com.android.dialer:id/floating_end_call_action_button").click()
                #command_shutdowndial = 'adb shell input keyevent 6'
                #subprocess.Popen(command_shutdowndial, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)				
                if ip_devices(resourceId="android:id/button1").exists:
                    ip_devices(resourceId="android:id/button1").click()
                #time.sleep(5)
            #call_battery = int(battery_start)-int(battery_finish)
            #self.updateResult("call_battery",battery_finish,testloop)            
            print time.strftime('%Y-%m-%d %H:%M:%S') 

            self.openRelay()
            time.sleep(3)
            command_return_usb = 'adb -s '+devices_id +' usb'
            os.system(command_return_usb)
            time.sleep(2)
            self.logger.info("call_battery: %s" %call_battery)'''
			
            
            self.config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"configure","common.ini"))
            phoneNumber = self.config.get("Telephony","phoneNumber")
            devices_id = self.config.get("Telephony","deviceId")
			
            command = "adb -s "+ devices_id +" shell am start -a android.intent.action.CALL -d tel:"+phoneNumber
            self.logger.debug("phoneNumber:%s"%phoneNumber) 
                                       
            for i in range(5):
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                returnValue= p.communicate()[0]
                self.logger.debug("returnValue:%s"%returnValue)
                if "Starting: Intent" in returnValue:
                    self.logger.info("Call success")                        
					self.closeRelay()
                    break
            self.device.delay(30*60)   
			
			self.openRelay()            
            #self.device.wakeup()                        

            battery_finish = self.get_battery()
            self.logger.info("battery_finish: %s" %battery_finish)
			
            date  = time.strftime("%H-%M-%S", time.localtime())
            print "date is %s" %date
            filename = "D:/batterystats.%s.call.txt" %date
            logfile = open(filename,"w")
            command = "adb shell dumpsys batterystats" 
            subprocess.Popen(command, shell=True, stdout=logfile, stderr=subprocess.PIPE)			
            
            call_battery = int(battery_start)-int(battery_finish)
            #self.updateResult("call_battery",battery_finish,testloop)
            self.logger.info("call_battery: %s" %call_battery) 
            if self.device(resourceId="com.android.dialer:id/floating_end_call_action_button").exists:
                self.device(resourceId="com.android.dialer:id/floating_end_call_action_button").click()               			
            if self.device(resourceId="android:id/button1").exists:
                self.device(resourceId="android:id/button1").click()

        except Exception,e:
            self.logger.error(e)
            #self.save_fail_img()

        self.setDisplayNever()
        self.device.press.home()
        #self.closewifi()
        self.device.delay(2)
        return call_battery

    def enterSetting(self):
        self.logger.debug('enter setting')
        if self.device(resourceId="com.android.settings:id/search").wait.exists(timeout = 5000):
            self.logger.info('enter setting success!')
            return True
        self.start_app("Settings",b_desk=True)

        if self.device(resourceId="com.android.settings:id/search").wait.exists(timeout = 5000):
            self.logger.info('enter setting success!')
            return True
        else:
            self.logger.warning('enter setting fail!')
            #self.save_fail_img()
            return False

    def standby(self,times):
        self.setDisplay15s()
        self.closeRelay()

        self.device.delay(15)
        self.logger.info("standby 1 minute")
        self.device.delay(60)
        self.openRelay()
        #self.device = connect_device(self.m_device,self.logger)
        self.device.delay(10)

    def setDisplay15s(self):
        self.logger.info("change display to 15s")
        self.enterSetting()       

        for loop in range(5):
            self.device.swipe(350,300,350,900,steps=5)
            self.device.delay(2)
            if self.device(text="Display").exists:
                self.device(text="Display").click()
                self.device.delay(2)
                break        
        
        for loop in range(5):
            self.device.swipe(350,900,350,350,steps=30)
            self.device.delay(2)
            if self.device(text="Sleep").exists:
                self.device(text="Sleep").click()
                self.device.delay(2)
                break
        if self.device(text="15 seconds").exists:
            self.device(text="15 seconds").click()
            self.logger.info("change display to 15s success")

        self.device.press.back()
        self.device.press.back()
        self.device.press.home()

    def setDisplayNever(self):
        self.logger.info("change display to Never")
        self.enterSetting()
        self.device.swipe(350,560,350,1200,steps=5)
        self.device.delay(1)

        for loop in range(5):
            self.device.swipe(350,300,350,900,steps=5)
            self.device.delay(2)
            if self.device(text="Display").exists:
                self.device(text="Display").click()
                self.device.delay(2)
                break        
        
        for loop in range(5):
            self.device.swipe(350,900,350,350,steps=30)
            self.device.delay(2)
            if self.device(text="Sleep").exists:
                self.device(text="Sleep").click()
                self.device.delay(2)
                break

        if self.device(text="Never").exists:
            self.device(text="Never").click()
            self.logger.info("change display to Never success.")
        self.device.press.back()
        self.device.press.back()
        self.device.press.home()


    def camera_test(self,camera_times,recording_times,testloop):
        try:
            self.logger.debug("camera test start")
            # self.setDisplayNever()
            camera_battery = 0
            #self.device.delay(5)
            self.start_activity("com.tct.camera","com.android.camera.CameraLauncher")

            #if self.enterCamera():
            battery_start = self.get_battery()
            self.logger.info("battery_start: %s" %battery_start)
            self.device.delay(1)
			
            command = "adb shell dumpsys batterystats --reset"
            os.system(command)
            command = "adb shell dumpsys batterystats enable full-history"
            os.system(command)  
			
            p=subprocess.Popen("camera.bat")

            self.logger.info("start camera.bat")
            
            self.device.delay(2)                                		            
            
            self.closeRelay()

            self.device.delay(60*camera_times)

            self.openRelay()
            self.device.delay(2)
            #self.device = connect_device(self.m_device,self.logger)            
			
            #kill shell pid
            shell_pid = self.get_shell_pid()
            self.logger.info("kill shell pid %s"%shell_pid)
            kill_command="adb -s "+self.m_device+" shell kill "+shell_pid
            if not shell_pid=="":
                os.system(kill_command)
                self.logger.info("kill shell pid success")
            self.device.delay(2)   			
            if self.device(resourceId=self.appconfig("Camera","id_video_shutter")).exists:
                self.device(resourceId=self.appconfig("Camera","id_video_shutter")).click()
                self.closeRelay()
                self.logger.info("recording 5 mins.")
                self.device.delay(60*recording_times)

                self.openRelay()
                self.device.delay(2)                
                #self.device = connect_device(self.m_device,self.logger)
                self.device(resourceId=self.appconfig("Camera","id_shutter")).click()
            
            battery_finish = self.get_battery()
            self.logger.info("battery_finish: %s" %battery_finish)
			
            date  = time.strftime("%H-%M-%S", time.localtime())
            print "date is %s" %date
            filename = "D:/batterystats.%s.camera.txt" %date
            logfile = open(filename,"w")
            command = "adb shell dumpsys batterystats" 
            subprocess.Popen(command, shell=True, stdout=logfile, stderr=subprocess.PIPE)			
            
            camera_battery = int(battery_start)-int(battery_finish)
            self.updateResult("camera_battery",battery_finish,testloop)
            self.logger.info("camera_battery: %s" %camera_battery)

        except Exception,e:
            self.logger.error(e)
            #self.save_fail_img()

        self.device.press.back()
        self.device.delay(1)
        self.device.press.home()
        self.device.delay(2)
        return camera_battery

    def baidumap_test(self,times,testloop):
        try:
            #self.setDisplayNever()
            self.logger.debug("baidu map test start")
            baidumap_battery= 0
            self.start_activity("com.baidu.BaiduMap","com.baidu.baidumaps.WelcomeScreen")
            self.device.delay(5)
           
            if self.device(resourceId="com.baidu.BaiduMap:id/negativeButton").exists:
                self.device(resourceId="com.baidu.BaiduMap:id/negativeButton").click()

            #cancel advertisement
            if self.device(resourceId="com.baidu.BaiduMap:id/btn_promote_cancel").exists:
                self.device(resourceId="com.baidu.BaiduMap:id/btn_promote_cancel").click()

            #skip version update
            if self.device(resourceId="com.baidu.BaiduMap:id/negativeButton").exists:
                self.device(resourceId="com.baidu.BaiduMap:id/negativeButton").click()

            if self.device(resourceId=self.appconfig("Map","id/route")).wait.exists(timeout=10000):
                self.device(resourceId=self.appconfig("Map","id/route")).click()
                self.device.delay(1)

            if self.device(resourceId=self.appconfig("Map","id_foot")).exists:
                self.device(resourceId=self.appconfig("Map","id_foot")).click()
                self.device.delay(1)

            if self.device(resourceId=self.appconfig("Map","id_end")).exists:
                self.device(resourceId=self.appconfig("Map","id_end")).click()
                self.device.delay(1)
            if self.device(resourceId="com.baidu.BaiduMap:id/iv_listitem_multiline_right").exists:
                self.device(resourceId="com.baidu.BaiduMap:id/iv_listitem_multiline_right").click()
                self.device.delay(1)

            if self.device(resourceId=self.appconfig("Map","id_confirm")).exists:
                self.device(resourceId=self.appconfig("Map","id_confirm")).click()
                self.device.delay(5)

            if self.device(resourceId="com.baidu.BaiduMap:id/to_navigation").exists:
                self.device(resourceId="com.baidu.BaiduMap:id/to_navigation").click()

            battery_start = self.get_battery()
            self.logger.info("battery_start: %s" %battery_start)
            command = "adb shell dumpsys batterystats --reset"
            os.system(command)
            command = "adb shell dumpsys batterystats enable full-history"
            os.system(command) 
			
            self.closeRelay()
            self.device.delay(60*times)

            self.openRelay()
            self.device.delay(2)
            #self.device = connect_device(self.m_device,self.logger)            

            battery_finish = self.get_battery()
            date  = time.strftime("%H-%M-%S", time.localtime())
            print "date is %s" %date
            filename = "D:/batterystats.%s.baidumap.txt" %date
            logfile = open(filename,"w")
            command = "adb shell dumpsys batterystats" 
            subprocess.Popen(command, shell=True, stdout=logfile, stderr=subprocess.PIPE)
			
            self.logger.info("battery_finish: %s" %battery_finish)
            self.updateResult("baidumap_battery",battery_finish,testloop)

            baidumap_battery = int(battery_start)-int(battery_finish)
            self.logger.info("baidumap_battery: %s" %baidumap_battery)

        except Exception,e:
            self.logger.error(e)
            #self.save_fail_img()


        self.device.press.back()
        self.device.delay(1)
        if self.device(resourceId="com.baidu.BaiduMap:id/visible").exists:
            self.device(resourceId="com.baidu.BaiduMap:id/visible").click()
            self.logger.info("navigation end")

        self.device.press.back()
        self.device.press.back()
        self.device.press.home()
        self.device.delay(2)
        return baidumap_battery

    def sina_weibo_test(self,times,testloop):
        try:
            #self.setDisplayNever()
            self.logger.debug("sina weibo test start")
            weibo_battery= 0
            #SplashActivity,VisitorMainTabActivity
            self.start_activity("com.sina.weibo","com.sina.weibo.MainTabActivity")

            #if self.enterWeibo():
            battery_start = self.get_battery()
            self.logger.info("battery_start: %s" %battery_start)
            command = "adb shell dumpsys batterystats --reset"
            os.system(command)
            command = "adb shell dumpsys batterystats enable full-history"
            os.system(command) 
			
            p=subprocess.Popen("weibo.bat")

            self.device.delay(2)

            #get shell process pid
            shell_pid=self.get_shell_pid()

            self.device.delay(1)
            self.closeRelay()

            self.logger.info("browser weibo 30mins")
            self.device.delay(60*times)

            self.openRelay()
            self.device.delay(5)
            #self.device = connect_device(self.m_device,self.logger)

            battery_finish = self.get_battery()


            self.logger.info("battery_finish: %s" %battery_finish)
            weibo_battery = int(battery_start)-int(battery_finish)
            self.updateResult("weibo_battery",battery_finish,testloop)

            self.logger.info("weibo_battery: %s" %weibo_battery)

            #kill shell pid
            shell_pid = self.get_shell_pid()
            self.logger.info("kill shell pid %s"%shell_pid)
            kill_command="adb -s "+self.m_device+" shell kill "+shell_pid
            if not shell_pid=="":
                os.system(kill_command)
                self.logger.info("kill shell pid success")
				
            date  = time.strftime("%H-%M-%S", time.localtime())
            print "date is %s" %date
            filename = "D:/batterystats.%s.weibo.txt" %date
            logfile = open(filename,"w")
            command = "adb shell dumpsys batterystats" 
            subprocess.Popen(command, shell=True, stdout=logfile, stderr=subprocess.PIPE)

        except Exception,e:
            self.logger.error(e)

        self.device.press.home()
        self.device.delay(2)
        return weibo_battery

    def get_shell_pid(self):
        sh_pid=""
        findpid_command = 'adb -s '+self.m_device+' shell ps |findstr "sh" '
        p = subprocess.Popen(findpid_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #self.logger.info("shellpid1 info:%s"%p)
        #returnValue=p.stdout.read()
        returnValue= p.communicate()[0]
        self.logger.info("shellpid info:%s"%returnValue)
        pidlist = returnValue.split("\n")
        for loop in range(len(pidlist)):
            self.logger.debug("loop:%s"%loop)
            if "poll_sched" in pidlist[loop] and  "shell" in pidlist[loop] and "0000000000" not in pidlist[loop]:
                self.logger.info("find shell process")
                sh_pidinfo = pidlist[loop]
                self.logger.info("sh_pidinfo:%s"%sh_pidinfo)
                pidinfo_list = sh_pidinfo.split()

                sh_pid=pidinfo_list[1]
                self.logger.info("sh_pid is:%s"%sh_pid)
                break
        else:
            self.logger.info("can not find shell process")
        return sh_pid

    def tencent_video_test(self,times,testloop,networktype):
        try:
            self.logger.debug("tencent video test start")
            t_video_battery= 0
            #self.setDisplayNever()

            if networktype:
                self.openwifi()

            self.start_activity("com.tencent.qqlive","com.tencent.qqlive.model.home.HomeActivity")
            
            #cancel apk update
            if self.device(resourceId="com.tencent.qqlive:id/download_storage_exception_button_cancel").exists:
                self.logger.info("cancel update")
                self.device(resourceId="com.tencent.qqlive:id/download_storage_exception_button_cancel").click()
                self.device.delay(2)

            if self.device(resourceId=self.appconfig("Tencent","id_search")).wait.exists(timeout = 10000):
                self.device(resourceId=self.appconfig("Tencent","id_search")).click()
            self.device.delay(2)

            self.device(resourceId=self.appconfig("Tencent","id_search_history")).click()
            self.device.delay(2)
            if self.device(text="01").wait.exists(timeout=10000):
                self.device(text="01").click()
                self.device.delay(2)
            else:
                self.device.press.back()
                self.device.press.back()
                self.device.press.home()
                self.closewifi()
                if networktype:
                    self.tencent_video_test(times,testloop,False)

            if self.device(resourceId=self.appconfig("Tencent","id_watch_sure")).exists:
                self.device(resourceId=self.appconfig("Tencent","id_watch_sure")).click()

            self.device.delay(2)
            
            self.device.click(675,400)
            self.device.delay(2)

            # tapcommand = "adb -s "+self.m_device+" shell input tap 1001 620"
            # os.system(tapcommand)
            # self.device.delay(1)
            # os.system(tapcommand)
            # self.device.delay(1)
            battery_start = self.get_battery()
            self.logger.info("battery_start: %s" %battery_start)
			
            command = "adb shell dumpsys batterystats --reset"
            os.system(command)
            command = "adb shell dumpsys batterystats enable full-history"
            os.system(command)                     	                      
            
            self.closeRelay()
            self.logger.debug("watching TV 30mins")
            self.device.delay(60*times)

            self.openRelay()
            self.device.delay(2)
            #self.device = connect_device(self.m_device,self.logger)
            date  = time.strftime("%H-%M-%S", time.localtime())
            print "date is %s" %date
            filename = "D:/batterystats.%s.tencentvideo.txt" %date
            logfile = open(filename,"w")
            command = "adb shell dumpsys batterystats" 
            subprocess.Popen(command, shell=True, stdout=logfile, stderr=subprocess.PIPE)
			
            battery_finish = self.get_battery()
            # battery_finish=0
            # for loop in range(10):
            #     self.logger.debug("get battery %s times"%loop)
            #     battery_finish = self.get_battery()
            #     if not battery_finish=="":
            #         self.logger.info(" get battery %s times ,get battery_finish success:%s"%(loop,battery_finish))
            #         break
            #     self.device.delay(2)

            self.logger.debug("battery_finish: %s" %battery_finish)
            t_video_battery = int(battery_start)-int(battery_finish)
            self.updateResult("tencentvideo_battery",battery_finish,testloop)

            self.logger.info("tencentvideo_battery: %s" %t_video_battery)

        except Exception,e:
            self.logger.error(e)
            #self.save_fail_img()
            self.device.press.home()

        self.device.press.back()
        self.device.press.back()
        self.device.press.back()
        self.device.press.back()
        self.device.press.home()
        self.device.delay(2)
        self.closewifi()
        return t_video_battery

    def updateResult(self,battery_type,battery_finish,loop):
        self.config.read('result.ini')
        # if not self.config.has_section("Default"):
        #         self.config.add_section("")
        section = "loop_"+str(loop+1)
        self.config.set(section, battery_type, battery_finish)
        self.config.write(open('result.ini', "r+"))
        self.logger.info("update %s success"%battery_type)

    def game_test(self,times,testloop):
        try:
            #self.device = connect_device(self.m_device,self.logger)
            self.logger.debug("Play games start")
            game_battery = 0
            self.device.delay(1)
            if not self.start_activity("com.ea.nfshp","com.ea.nfshp.GameActivity"):
                self.openRelay()
                self.device.delay(5)
                self.start_activity("com.ea.nfshp","com.ea.nfshp.GameActivity")
            #self.logger.info("start game success")            

            self.device.delay(15)
            self.device.click(970,580)
            self.device.delay(15)
            self.device.click(970,580)
            self.device.delay(1)
            battery_start = self.get_battery()
            self.logger.info("battery_start: %s" %battery_start)
            command = "adb shell dumpsys batterystats --reset"
            os.system(command)
            command = "adb shell dumpsys batterystats enable full-history"
            os.system(command)

            self.closeRelay()
            self.logger.info("paly games 30mins")
            self.device.delay(60*times)

            self.openRelay()
            self.device.delay(2)
            #self.device = connect_device(self.m_device,self.logger)
            battery_finish = self.get_battery()
            
            date  = time.strftime("%H-%M-%S", time.localtime())
            print "date is %s" %date
            filename = "D:/batterystats.%s.game.txt" %date
            logfile = open(filename,"w")
            command = "adb shell dumpsys batterystats" 
            subprocess.Popen(command, shell=True, stdout=logfile, stderr=subprocess.PIPE)
            #os.system(command)
            

            self.logger.info("battery_finish: %s" %battery_finish)
            self.updateResult("game_battery",battery_finish,testloop)

            game_battery = int(battery_start)-int(battery_finish)
            self.logger.info("game_battery: %s" %game_battery)
        except Exception,e:
            self.logger.error(e)
            #self.save_fail_img()
            self.device.press.home()

        self.device.press.home()
        self.device.delay(2)
        return game_battery


    def wechat_test(self,times,testloop):
        try:
            self.setDisplayNever()
            self.logger.debug("test wechat start")
            wechat_battery = 0
            if not self.start_activity("com.tencent.mm","com.tencent.mm.ui.LauncherUI"):
                self.openRelay()
                self.device.delay(2)
                self.start_activity("com.tencent.mm","com.tencent.mm.ui.LauncherUI")
            self.device.delay(5)            

            if self.device(text="WeChat Team").exists:
                self.device(text="WeChat Team").click()

            #if self.device(resourceId="com.tencent.mm:id/iz").exists:
                #self.device(resourceId="com.tencent.mm:id/iz").click()

            #if self.device(resourceId="com.tencent.mm:id/wq").exists:
            #    self.device(resourceId="com.tencent.mm:id/wq").click()

            if self.device(resourceId="com.tencent.mm:id/jj").exists:
                self.device(resourceId="com.tencent.mm:id/jj").click()
            self.device.delay(1)
            self.device.click(350, 1230)

            battery_start = self.get_battery()
            self.logger.info("battery_start: %s" %battery_start)
			
            command = "adb shell dumpsys batterystats --reset"
            os.system(command)
            command = "adb shell dumpsys batterystats enable full-history"
            os.system(command)
			
            subprocess.Popen("wechat.bat")

            self.device.delay(1)            

            self.closeRelay()

            self.logger.debug("test wechat  30mins")
            self.device.delay(60*times)

            self.openRelay()
            self.device.delay(2)
            #self.device = connect_device(self.m_device,self.logger)
            shell_pid=self.get_shell_pid()
            kill_command="adb -s "+self.m_device+" shell kill "+shell_pid
            if not shell_pid=="":
                self.logger.info("kill shell pid %s"%shell_pid)
                os.system(kill_command)
                self.logger.info("kill shell pid success")

            battery_finish = self.get_battery()           
            self.logger.info("battery_finish: %s" %battery_finish)
            date  = time.strftime("%H-%M-%S", time.localtime())
            print "date is %s" %date
            filename = "D:/batterystats.%s.wechat.txt" %date
            logfile = open(filename,"w")
            command = "adb shell dumpsys batterystats" 
            subprocess.Popen(command, shell=True, stdout=logfile, stderr=subprocess.PIPE)
			
            wechat_battery = int(battery_start)-int(battery_finish)

            self.updateResult("wechat_battery",battery_finish,testloop)

            self.logger.info("wechat_battery: %s" %wechat_battery)

        except Exception,e:
            self.logger.error(e)
            #self.save_fail_img()
            self.device.press.back()
            self.device.press.back()
            self.device.press.home()                   

        self.device.press.back()
        self.device.press.back()
        self.device.press.home()

        return wechat_battery

    def openwifi(self):
        self.logger.info("open wifi mobile test.")
        self.enterSetting()
        
        for loop in range(5):
            self.device.swipe(350,300,350,900,steps=5)
            self.device.delay(2)
            if self.device(text="Wi-Fi").exists:
                self.device(text="Wi-Fi").click()
                break
        #self.device.swipe(550,1200,550,560,steps=30)
        self.device.delay(2)
        if self.device(text="ON").exists:
            self.logger.info(" wifi is open areadly.")
            self.device.press.back()
            self.device.press.back()
            self.device.press.home()
            return

        if self.device(text="OFF").exists:
            self.device(text="OFF").click()
            self.logger.info("open wifi success.")

        self.device.delay(8)

        self.device.press.back()
        self.device.press.back()
        self.device.press.home()

        return False

    def closewifi(self):
        self.logger.debug("close wifi mobile test.")
        self.enterSetting()        
        self.device.delay(2)

        for loop in range(5):
            self.device.swipe(350,300,350,900,steps=5)
            self.device.delay(2)
            if self.device(text="Wi-Fi").exists:
                self.device(text="Wi-Fi").click()
                break

        if self.device(text="OFF").exists:
            self.logger.info(" wifi is close areadly.")
            self.device.press.back()
            self.device.press.back()
            self.device.press.home()
            return

        if self.device(text="ON").exists:
            self.device(text="ON").click()
            self.logger.info("close wifi success.")

        self.device.press.back()
        self.device.press.back()
        self.device.press.home()

        return False


    def openGPS(self):
        self.logger.debug("open gps.")
        self.enterSetting()

        for loop in range(5):
            if self.device(text="Location").exists:
                self.device(text="Location").click()
                break
            self.device.swipe(350,900,350,330,steps=30)
            self.device.delay(1)

        if self.device(text="ON").exists:
            self.logger.info(" GPS is open areadly.")
            return

        if self.device(text="OFF").exists:
            self.device(text="OFF").click()
            self.logger.info("GPS wifi success.")

        self.device.press.back()
        self.device.press.back()
        self.device.press.home()

    def closeGPS(self):
        self.logger.debug("close gps")
        self.enterSetting()

        for loop in range(5):
            if self.device(text="Location").exists:
                self.device(text="Location").click()
                break
            self.device.swipe(350,900,350,330,steps=30)
            self.device.delay(1)

        if self.device(text="OFF").exists:
            self.logger.info(" GPS close areadly.")
            return

        if self.device(text="ON").exists:
            self.device(text="ON").click()
            self.logger.info("close wifi success.")

        self.device.press.back()
        self.device.press.back()
        self.device.press.home()

    def get_battery(self):
        command = "adb -s "+self.m_device+" shell cat sys/class/power_supply/battery/capacity"

        for loop in range(10):
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            battery= p.communicate()[0]
            if "daemon not running" not in battery.strip() and not battery.strip()=="":
                self.logger.info(" get battery %s times,battery:%s"%(loop,battery.strip()))
                break
            time.sleep(2)
            #self.device.delay(2)

        return battery.strip()

    def get_call_battery(self,ip):
        command = "adb -s "+ ip +" shell cat sys/class/power_supply/battery/capacity"

        for loop in range(10):
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            battery= p.communicate()[0]
            if "daemon not running" not in battery.strip() and not battery.strip()=="":
                self.logger.info(" get battery %s times,battery:%s"%(loop,battery.strip()))
                break
            #time.sleep(2)
            #self.device.delay(2)

        return battery.strip()    



if __name__ == '__main__':
    pass
            
