# -*- coding: UTF-8 -*-
"""Telephony library for scripts.
"""
import os
import sys
import time
# from common import Common
from common import *


class PreSettings(Common):
    """Provide common functions for scripts, such as launching activity."""  
        
    def enter_dialer(self):
        '''Launch calender by start activity.
        '''
        self.logger.debug("Enter Dialer")
        if self.device(description= self.appconfig.id("Dialer","id_enter_des")).exists:
            return True
        self.start_app("Call")
        self.device.delay(5)
        if self.device(resourceId = self.appconfig.id("Dialer","id_call")).exists:
            self.logger.debug("id_call exists")
            return True

        elif self.device(description = "Dial pad").wait.exists(timeout=self.timeout):
            self.logger.debug("Dial pad exists")
            return True
        else:
            self.logger.warning("id_enter or id_call not exists")
            return False
 
    def call_10010(self):
        self.enter_dialer()
        self.device.delay(2)
        #self.device(resourceId="com.android.dialer:id/floating_action_button").click()

       # if self.device(resourceId= self.appconfig.id("Dialer","id_enter")).exists:
        if self.device(resourceId = self.appconfig.id("Dialer","id_call")).exists:
            self.device(resourceId="com.android.dialer:id/one").click()
            self.device(resourceId="com.android.dialer:id/two").click()
            self.device(resourceId="com.android.dialer:id/three").click()
            self.device(resourceId="com.android.dialer:id/four").click()
            self.device(resourceId="com.android.dialer:id/five").click()
        elif self.device(description = "Dial pad").wait.exists(timeout= 10000):
            self.logger.debug("Dial pad exists")
            self.device(description = "Dial pad").click()
            #if self.device(description = self.appconfig.id("Dialer","id_call_des")).wait.exists(timeout=10000):
            if self.device(className = "android.widget.ImageButton").wait.exists(timeout=10000):
                self.device(resourceId="com.android.dialer:id/one").click()
                self.device(resourceId="com.android.dialer:id/zero").click()
                self.device(resourceId="com.android.dialer:id/zero").click()
                self.device(resourceId="com.android.dialer:id/one").click()
                self.device(resourceId="com.android.dialer:id/zero").click()
                #self.device(className = "android.widget.ImageButton").click()
                self.device.click(550,1640)
            else:
                self.logger.debug("id_call_des not exists")
        self.device(text = "00:05").wait.exists(timeout = 10000)
        if self.device(description='End').wait.exists(timeout=self.timeout):
            self.device(description='End').click()
            self.device.press.back()
            self.logger.info("Trace Success Loop")
            self.suc_times += 1
            self.logger.debug("call 10010 success")

    def enter_contacts(self):
        self.logger.debug("Launch Contacts")
        if self.device(text = self.appconfig.id("Contacts","contacts_text")).exists:
            self.device(text = self.appconfig.id("Contacts","contacts_text")).click()
            self.device.delay(1)
            return True
        self.start_app("Contacts")
        self.device.delay(2)
        if self.device(text = "All contacts").exists:
            self.device(text = "All contacts").click()
            self.device.delay(1)
            return True
        self.logger.debug("Launch Contacts Fail")
        return False

    def import_contacts(self):
        self.enter_contacts()
        if not self.device(text = "Import contacts").exists:
            self.device(text = "All contacts").click()

        self.device(text = "Import contacts").click()
        self.device(text = "Import from phone storage").click()
        self.device(text = "Import one vCard file").click()
        self.device(text = "OK").click()

        if self.device(resourceId="android:id/select_dialog_listview").child(index = 1).exists:
            self.device(resourceId="android:id/select_dialog_listview").child(index = 1).click()
            self.device(text = "OK").click()
            self.logger.info("Trace Success Loop")
            self.suc_times += 1
            self.logger.debug(" add email account success")
        else:
            self.logger.warning("10010.vcf not exists")
            return False

    def enter_message(self):
        """Launch browser.
        """
        self.logger.debug('enter Message')
        if self.device(resourceId= self.appconfig.id("Message","id_enter")).wait.exists(timeout=2000):
            return True
        self.start_app("Messaging")
        if self.device(resourceId= self.appconfig.id("Message","id_enter")).wait.exists(timeout=2000):
            return True
        else:
            self.logger.warning('Launch Message fail')
            return False
        return True


    def create_MMS(self):
        self.foward_text_mms()
        self.foward_picture_mms()
        self.foward_video_mms()
        self.foward_record_mms()

    def foward_text_mms(self):
        self.enter_message()
        try:
            #add text_mms
            self.logger.debug("add text_MMS account start")
            if self.device(resourceId="com.android.mms:id/floating_action_button").exists:
                self.device(resourceId="com.android.mms:id/floating_action_button").click()
                self.device(resourceId="com.android.mms:id/recipients_editor").set_text("1")
                self.device(text="Send message").click()
                self.device(resourceId="com.android.mms:id/embedded_text_editor").set_text("stability test")
                self.device(resourceId="com.android.mms:id/send_button_sms").click()
                self.device.press.back()
                self.device.delay(1)
                self.device.press.back()
                self.device.delay(1)
                self.device.press.back()
                self.logger.info("Trace Success Loop")
                self.suc_times += 1
                self.logger.debug(" add text_MMS account success")
        except Exception,e:
            self.logger.debug(" add text_MMS account failed")
            self.logger.warning(e)
            self.save_fail_img()

    def foward_picture_mms(self):
        self.enter_message()
        try:
            #add picture_mms
            self.logger.debug("add picture_mms account start")
            if self.device(resourceId="com.android.mms:id/floating_action_button").exists:
                self.device(description="add new message").click()
                self.device(resourceId="com.android.mms:id/recipients_editor").set_text("2")
                self.device(text="Send message").click()
                self.device(resourceId="com.android.mms:id/embedded_text_editor").set_text("stability test")
                self.device(resourceId="com.android.mms:id/share_button").click()
                self.device.delay(3)
                self.device.click(807, 470)

                if self.device(text="No thanks").exists:
                    self.device(text="No thanks").click()

                self.device(text="Take photo").click()
                self.device(resourceId="com.tct.camera:id/shutter_button_photo").click()
                self.device.delay(2)
                self.device(resourceId="com.tct.camera:id/btn_done").click()
                self.device.delay(2)

                #self.device(resourceId="com.android.mms:id/send_button_sms").click()
                self.device(description="Send MMS").click()
                self.device.delay(2)
                self.device.press.back()
                self.device.delay(1)
                self.device.press.back()
                self.logger.info("Trace Success Loop")
                self.suc_times += 1
                self.logger.debug(" add picture_MMS account success")
        except Exception,e:
            self.logger.debug(" add picture_MMS account failed")
            self.logger.warning(e)
            self.save_fail_img()

    def foward_video_mms(self):
        self.enter_message()
        try:
            #add video_mms
            self.logger.debug("add video_mms account start")
            if self.device(resourceId="com.android.mms:id/floating_action_button").exists:
                self.device(resourceId="com.android.mms:id/floating_action_button").click()
                self.device(resourceId="com.android.mms:id/recipients_editor").set_text("3")
                self.device(text="Send message").click()
                self.device(resourceId="com.android.mms:id/embedded_text_editor").set_text("stability test")
                self.device(resourceId="com.android.mms:id/share_button").click()
                self.device(text="Capture video").click()
                self.device(resourceId="com.tct.camera:id/shutter_button_photo").click()
                self.device.delay(1)
                self.device(resourceId="com.tct.camera:id/shutter_button_photo").click()
                self.device.delay(2)
                self.device(resourceId="com.tct.camera:id/btn_done").click()
                self.device.delay(2)

                self.device(description="Send MMS").click()
                self.device.delay(2)

                self.device.press.back()
                self.device.delay(1)
                self.device.press.back()
                self.logger.info("Trace Success Loop")
                self.suc_times += 1
                self.logger.debug(" add video_MMS account success")
        except Exception,e:
            self.logger.debug(" add video_MMS account failed")
            self.logger.warning(e)
            self.save_fail_img()

    def foward_record_mms(self):
        self.enter_message()
        try:
            #add record_mms
            self.logger.debug("add record_mms account start")
            if self.device(resourceId="com.android.mms:id/floating_action_button").exists:
                self.device(resourceId="com.android.mms:id/floating_action_button").click()
                self.device(resourceId="com.android.mms:id/recipients_editor").set_text("4")
                self.device(text="Send message").click()
                self.device(resourceId="com.android.mms:id/embedded_text_editor").set_text("stability test")
                self.device(resourceId="com.android.mms:id/share_button").click()
                self.device(text="Record audio").click()
                self.device(resourceId="com.tct.soundrecorder:id/recordButton").click()
                self.device.delay(2)
                self.device(text="Save").click()
                self.device.delay(2)
                #self.device(resourceId="com.android.mms:id/send_button_mms").click()
                self.device(description="Send MMS").click()
                self.device.delay(2)
                self.device.press.back()
                self.device.delay(1)
                self.device.press.back()
                self.logger.info("Trace Success Loop")
                self.suc_times += 1
                self.logger.debug(" add record_mms account success")
        except Exception,e:
            self.logger.debug(" add record_mms account failed")
            self.logger.warning(e)
            self.save_fail_img()
    def enter_Browser(self):
        """Launch browser.
        """
        self.logger.debug('enter browser')
        if self.device(resourceId= self.appconfig.id("Browser","id_url")).wait.exists(timeout=self.timeout):
            return True
        self.start_app("Browser")
        if self.device(resourceId= self.appconfig.id("Browser","id_url")).wait.exists(timeout=self.timeout):
            return True
        else:
            return False
    def save_bookmark(self):
        self.device(resourceId="com.android.browser:id/more_browser_settings").click()
        self.device(text="Save to bookmarks").click()
        self.device.delay(2)
        self.device(text="OK").click()

        if self.device(text="OK").exists:
            self.device(text="OK").click()

    def set_homepage(self):
        self.device(resourceId="com.android.browser:id/more_browser_settings").click()
        self.device.swipe(750,1300,750,500,steps=20)

        self.device(text="Settings").click()
        self.device(text="General").click()
        self.device(text="Set homepage").click()
        self.device(text="Current page").click()

        self.device.press.back()
        self.device.delay(1)
        self.device.press.back()
        self.device(resourceId="com.android.browser:id/more_browser_settings").click()
        self.device.swipe(750,1300,750,500,steps=20)

        self.logger.info("browser exit")
        self.device(text = "Exit").click()
        self.device(text = "Quit").click()

    def add_bookmarks(self):
        self.enter_Browser()

        url_text = self.device(resourceId="com.android.browser:id/url")
        if url_text.wait.exists(timeout=self.timeout):
            self.logger.debug("add bookmark1")
            #self.device(resourceId="com.android.browser:id/url").click()
            self.device.delay(1)
            bookmark1 = self.appconfig("Browser","bookmark1")
            self.logger.debug("bookmark1:%s"%bookmark1)
            url_text.set_text(bookmark1)
            #self.device(resourceId="com.android.browser:id/url").set_text("www.baidu.com")
            self.device.delay(2)
            self.device.press.enter()
            self.device.delay(3)
            self.save_bookmark()
            self.logger.info("Trace Success Loop")
            self.suc_times += 1
            self.logger.debug("add bookmark1 success")


        if url_text.wait.exists(timeout=5000):
            self.logger.debug("add bookmark2")
            #self.device(resourceId="com.android.browser:id/url").click()
            self.device.delay(2)
            bookmark2 = self.appconfig("Browser","bookmark2")
            self.logger.debug("bookmark2:%s"%bookmark2)

            url_text.set_text(bookmark2)
            self.device.delay(2)
            self.device.press.enter()
            self.device.delay(3)
            self.save_bookmark()

            self.logger.info("Trace Success Loop")
            self.suc_times += 1
            self.logger.debug("add bookmark1 success")


        if url_text.wait.exists(timeout=5000):
            self.logger.debug("add bookmark3")
            #self.device(resourceId="com.android.browser:id/url").click()
            self.device.delay(1)
            bookmark3 = self.appconfig("Browser","bookmark3")
            self.logger.debug("bookmark3:%s"%bookmark3)
            url_text.set_text(bookmark3)
            self.device.delay(2)
            self.device.press.enter()
            self.device.delay(3)
            self.save_bookmark()

            self.logger.info("Trace Success Loop")
            self.suc_times += 1
            self.logger.debug("add bookmark1 success")

        if url_text.wait.exists(timeout=5000):
            self.logger.debug("add bookmark4")
            #self.device(resourceId="com.android.browser:id/url").click()
            self.device.delay(1)
            bookmark4 = self.appconfig("Browser","bookmark4")
            self.logger.debug("bookmark4:%s"%bookmark4)
            url_text.set_text(bookmark4)
            self.device.delay(2)
            self.device.press.enter()
            self.device.delay(3)
            self.save_bookmark()

            self.logger.info("Trace Success Loop")
            self.suc_times += 1
            self.logger.debug("add bookmark1 success")


        if url_text.wait.exists(timeout=5000):
            self.logger.debug("add bookmark5")
            #self.device(resourceId="com.android.browser:id/url").click()
            self.device.delay(1)
            bookmark5 = self.appconfig("Browser","bookmark5")
            self.logger.debug("bookmark5:%s"%bookmark5)
            url_text.set_text(bookmark5)
            self.device.delay(2)
            self.device.press.enter()
            self.device.delay(3)
            self.save_bookmark()

            self.logger.info("Trace Success Loop")
            self.suc_times += 1
            self.logger.debug("add bookmark1 success")


        self.logger.debug("add bookmarks completed")

        #set homepage
        self.set_homepage()

    def enter_email(self):
        """Launch email by StartActivity.
        """
        self.logger.debug("Launch email.")
        if self.device(description=self.appconfig("Email","navigation")).wait.exists(timeout=self.timeout):
            return True
        self.start_app("Email")
        if self.device(resourceId="com.tct.email:id/lower_headline").wait.exists(timeout=self.timeout):
            self.logger.debug('Launch eamil success')
            return True
        else:
            self.logger.debug('Launch eamil fail')
            return False

    def add_email_account(self,email_act_psw):

        self.enter_email()
        self.device(text = "Email address").click()
        self.logger.info("Email address and password is:%s"%email_act_psw)
        email_act_psw_list = email_act_psw.split("|")
        email_act = email_act_psw_list[0]
        email_pws = email_act_psw_list[1]
        self.logger.debug("Email address:%s ,Email password:%s"%(email_act,email_pws))
        self.device(text = "Email address").set_text(email_act)
        self.device(text="Next").click()
        if self.device(text = "POP3").wait.exists(timeout=10000):
            self.device(text="POP3").click()
        else:
            self.logger.warning("pop3 not exists")
        self.device(resourceId = "com.tct.email:id/regular_password").set_text(email_pws)
        self.device(text="Next").click()

        self.device(resourceId="com.tct.email:id/account_server").clear_text()
        self.device.delay(1)
        self.device(resourceId="com.tct.email:id/account_server").set_text("mail.tcl.com")
        self.device(text="Next").click()
        self.device.delay(2)
        self.device(resourceId="com.tct.email:id/account_server").clear_text()
        self.device.delay(1)
        self.device(resourceId="com.tct.email:id/account_server").set_text("mail.tcl.com")
        self.device(text="Next").click()
        self.device.delay(1)
        self.device(text="Next").click()
        self.device(resourceId="com.tct.email:id/account_name").set_text(email_act)
        self.device(text="Finish").click()

        if self.device(resourceId="com.tct.email:id/dismiss_button").exists:
            self.device(resourceId="com.tct.email:id/dismiss_button").click()

        self.logger.info("Trace Success Loop")
        self.suc_times += 1
        self.logger.debug(" add email account success")


if __name__ == '__main__':
    a = PreSettings("158fdc50","TestPreSetting")
    a.delete_contact(5)

