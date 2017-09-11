#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import unittest
import os
import sys
import logging
from ConfigParser import ConfigParser


libpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not libpath in sys.path:
    sys.path.append(libpath)
from common.dou import Dou

class TestDou(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = Dou(device_id,logger)

    @classmethod
    def tearDownClass(cls):
        cls.mod.logger.info('Dou Automation Test Completed')

    def testdou(self):
        self.mod.openRelay()
        if testtype == "normal":
             for i in range(2000):
                battery = self.mod.get_battery()
                if battery == "100":
                    self.mod.device.delay(3*60)
                break
                self.mod.device.delay(100)
                self.mod.logger.info("current battery:%s" %battery)

        for loop in range(int(testloop)):
            
            '''game_battery = self.Game(loop)
            self.mod.logger.info("game_battery:%s" %game_battery)'''

            music_battery = self.Music(loop)
            self.mod.logger.info("music_battery:%s" %music_battery)
            
            '''tencentVideo_battery = self.TencentVideo(loop)
            self.mod.logger.info("tencentVideo_battery:%s" %tencentVideo_battery)
            
            call_battery = self.Call(loop)
            self.mod.logger.info("call_battery:%s" %call_battery)
            
            camera_battery = self.Camera(loop)
            self.mod.logger.info("camera_battery:%s" %camera_battery)
            
            browser_battery = self.Browser(loop)
            self.mod.logger.info("browser_battery:%s" %browser_battery)
            
            baiduMap_battery = self.BaiduMap(loop)
            self.mod.logger.info("baiduMap_battery:%s" %baiduMap_battery)
            
            weibo_battery = self.Weibo(loop)
            self.mod.logger.info("weibo_battery:%s" %weibo_battery)
            
            wechat_battery = self.wechat(loop)
            self.mod.logger.info("wechat_battery:%s" %wechat_battery)'''
            
            #self.clearallapp()

    def clearallapp(self):
        self.mod.clearapp()
		
    def Game(self,loop):
        #self.mod.standby(int(standby_time))
        battery = self.mod.game_test(int(game_time),loop)
        return battery
    
    def Music(self,loop):
        #self.mod.standby(int(standby_time))
        battery = self.mod.play_music(int(music_time),loop)
        return battery

    def TencentVideo(self,loop):
        #self.mod.standby(int(standby_time))
        battery = self.mod.tencent_video_test(int(tencentVideo_time),loop,True)
        return battery

    def Call(self,loop):
        #self.mod.standby(int(standby_time))
        #self.mod.Wi_Fi_isconnect()
        battery = self.mod.Call_test(int(call_time),loop,True)
        return battery
    
    def Camera(self,loop):
        #self.mod.standby(int(standby_time))
        battery = self.mod.camera_test(int(camera_time),int(recording_time),loop)
        return battery

    def Browser(self,loop):
        #self.mod.standby(int(standby_time))
        battery = self.mod.browser_test(int(browser_time),loop)
        return battery

    def BaiduMap(self,loop):
        #self.mod.standby(int(standby_time))
        self.mod.openGPS()
        battery = self.mod.baidumap_test(int(baiduMap_time),loop)
        self.mod.closeGPS()
        return battery

    def Weibo(self,loop):
        #self.mod.standby(int(standby_time))
        battery = self.mod.sina_weibo_test(int(sinawebo_time),loop)
        return battery

    def wechat(self,loop):
        #self.mod.standby(int(standby_time))
        battery = self.mod.wechat_test(int(wechat_time),loop)
        return battery

if __name__ == '__main__':
    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    commonconfig = ConfigParser()
    commonconfig.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"configure","common.ini"))
    device_id = commonconfig.get("Default","deviceid")
    logger.info("device_id:%s"%device_id)

    fh = logging.FileHandler(device_id+".log")
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d: [%(levelname)s] [%(funcName)s] [%(lineno)d] %(message)s',
        '%y%m%d %H:%M:%S')
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    testtype = commonconfig.get("Default","TEST_TYPE")
    testloop = commonconfig.get("Default","TEST_LOOP")
    logger.info("test type:%s"%testtype)

    standby_time = commonconfig.get(testtype,"Standby")
    game_time = commonconfig.get(testtype,"Game")
    music_time = commonconfig.get(testtype,"Music")

    tencentVideo_time = commonconfig.get(testtype,"TencentVideo")
    call_time = commonconfig.get(testtype,"Call")
    camera_time = commonconfig.get(testtype,"Camera")
    recording_time = commonconfig.get(testtype,"Recording")
    browser_time = commonconfig.get(testtype,"Browser")
    baiduMap_time = commonconfig.get(testtype,"BaiduMap")
    sinawebo_time = commonconfig.get(testtype,"SinaWebo")
    wechat_time = commonconfig.get(testtype,"WeChat")


    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestDou)
    suite = unittest.TestSuite([suite1])
    unittest.TextTestRunner(verbosity=2).run(suite)

