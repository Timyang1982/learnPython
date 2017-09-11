import os
import subprocess
from Tkinter import *
from tkMessageBox import *
from ttk import *
from time import sleep

class Application:
    def __init__(self, parent):
        
        self.parent = parent
        self.dev_id = None
        self.type1_times = 0
        self.type23_times = 0
        self.test_times = 0
        self.case_num = 0
        
        # ----------- Start init Frame -----------
        self.set_container = Frame(self.parent)
        self.set_container.pack(fill = "both")
        self.type_container = Frame(self.parent)
        self.type_container.pack(fill = "both")
        self.package_container = Frame(self.parent)
        self.package_container.pack(fill = "both")
        self.package_lb_container = Frame(self.package_container)
        self.package_lb_container.pack(side = "left")
        self.package_btn_container = Frame(self.package_container)
        self.package_btn_container.pack(side = "left")
        self.bottom_container = Frame(self.parent)
        self.bottom_container.pack()
        self.bottom_container2 = Frame(self.parent)
        self.bottom_container2.pack()
        # ----------- Finish init Frame -----------
        
        # ----------- Start create wigets for setting m812 condition -----------
        self.device_label = Label(self.set_container, text = "DeviceID: ")
        self.device_label.pack(side = "left")
        self.combo_entry_container = Frame(self.set_container)
        self.combo_entry_container.pack(side = "left")
        self.combo(self.combo_entry_container)
        self.device_entry_value = StringVar()
        self.device_entry = Entry(self.combo_entry_container, textvariable=self.device_entry_value, width = 26)
        self.loop_label = Label(self.set_container, text = "Loop: ")
        self.loop_label.pack(side = "left")
        self.tt = IntVar()
        self.loop_entry = Entry(self.set_container, textvariable=self.tt, width = 10)
        self.tt.set("1")
        self.loop_entry.pack(side = "left")
        self.button_set_times = Button(self.set_container, command=self.set_button_click)
        self.button_set_times.configure(text="SET")
        self.button_set_times.pack(side = "right")
        # ----------- Finish create wigets for setting m812 condition -----------
        
        # ----------- Finish create wigets for choosing m812 type -----------
        self.rbtn_var = IntVar()
        self.rbtn1 = Radiobutton(self.type_container, text="System Stability", variable=self.rbtn_var, value=1, command = self.set_test_times)
        self.rbtn1.pack(side = "left", pady = 5)
        self.rbtn2 = Radiobutton(self.type_container, text="Application Stability1", variable=self.rbtn_var, value=2, command = self.set_test_times)
        self.rbtn2.pack(side = "left", padx = 5, pady = 5)
        self.rbtn3 = Radiobutton(self.type_container, text="Application Stability2", variable=self.rbtn_var, value=3, command = self.set_test_times)
        self.rbtn3.pack(side = "left", padx = 5, pady = 5)
        # ----------- Finish create wigets for choosing m812 type -----------
        
        # ----------- Start create wigets for setting circulation times -----------
        self.package_hsb = Scrollbar(self.package_lb_container, orient = HORIZONTAL)
        self.package_vsb = Scrollbar(self.package_lb_container, orient = VERTICAL)
        self.package_lb = Listbox(self.package_lb_container, selectmode = EXTENDED, height=20, width=50, font="Consolas 8", 
                                  yscrollcommand=self.package_vsb.set, 
                                  xscrollcommand=self.package_hsb.set)
        self.package_vsb.config(command=self.package_lb.yview)  
        self.package_hsb.config(command=self.package_lb.xview)  
        self.package_vsb.pack(fill="y", expand=0, side=RIGHT, anchor=N)  
        self.package_hsb.pack(fill="x", expand=0, side=BOTTOM, anchor=N)
        f_usage = open('Usage.txt', 'rb')
        for line in f_usage:
            self.package_lb.insert(END, line)
        self.package_lb.pack()
        self.button_create = Button(self.package_btn_container, command=self.create_button_click)
        self.button_create.configure(text="CREATE LIST")
        self.button_create.pack(side = "right")
        # ----------- Finish create wigets for setting circulation times -----------
        
        # ----------- Start create buttons for reset/start/exit m812 -----------
        self.button_quit = Button(self.bottom_container, command=self.quit_button_click)
        self.button_quit.configure(text="QUIT")
        self.button_quit.pack(padx = 5, side = "left")
        self.button_reset = Button(self.bottom_container, command=self.reset_button_click)
        self.button_reset.configure(text="RESET")
        self.button_reset.pack(padx = 5, side = "left")
        self.button_result = Button(self.bottom_container, command=self.get_result_click)
        self.button_result.configure(text="RESULT")
        self.button_start = Button(self.bottom_container, command=self.start_button_click)
        self.button_start.configure(text="START")
        #self.button_type_1 = Button(self.bottom_container2, command=self.script_debug)
        #self.button_type_1.configure(text="debug")
        # ----------- Finish create buttons for reset/start/exit m812 -----------
        
    def select_device(self, event):
        self.box['values'] = self.get_device_list()
        
    def get_device_list(self):
        dev_list = ["None"]
        subprocess.call('adb start-server', startupinfo=startupinfo)
        return_value = subprocess.Popen('adb devices', stdout = subprocess.PIPE, startupinfo=startupinfo).stdout.readlines()
        for line in return_value:
            m_dev_id = re.match(r'(\w+)(?=\t)', line)
            if m_dev_id:
                dev_id = m_dev_id.group()
                dev_list.append(dev_id)
        return dev_list
         
    def combo(self, parent_frame):
        self.box_value = StringVar()
        self.box = Combobox(parent_frame, textvariable=self.box_value,
                            state='readonly', width = 23)
        self.box.set("None")
        self.box.bind('<Button-1>',self.select_device)
        self.box.pack(side = "left")
        
    def create_button_click(self):
        package_f = open('packagelist.txt', 'wb')
        lb_curselection = self.package_lb.curselection()
        for loop in range(self.type23_times):
            for index in lb_curselection:
                line = self.package_lb.get(index)
                pacake_name = re.match(r'(\S+)', line[4:]).group()
                package_f.write(pacake_name+"\n")
        package_f.close()
        if self.case_num == 2:
            self.button_start.configure(text="CONTINUE")
        
    def set_button_click(self):
        if (type(self.tt.get()) == int and self.box_value.get() != "None" and self.case_num != 0):
            self.set_test_times()
            self.rbtn1.configure(state=DISABLED)
            self.rbtn2.configure(state=DISABLED)
            self.rbtn3.configure(state=DISABLED)
            self.loop_entry["state"]='readonly'
            self.dev_id = self.box_value.get()
            print self.dev_id, self.case_num, self.test_times
            self.button_result.pack(padx = 5, side = "left")
            self.button_start.configure(text="START")
            self.button_start.pack(padx = 5, side = "left")
            #self.button_type_1.pack(padx = 5, side = "left")
            self.box.forget()
            self.device_entry_value.set(self.dev_id)
            self.device_entry.config(state = "readonly")
            self.device_entry.pack(side = "left")
            if self.case_num != 1:
                self.get_package_list()
        else:
            showwarning(title = "Warning",message = "Set Devices ID, Test Times and Test Type first!")
            print "Set Devices ID, Test Times and Test Type first!"
         
    def reset_button_click(self):
        if os.path.exists("packagelist.txt"):
            os.remove("packagelist.txt")
        self.rbtn1.configure(state=NORMAL)
        self.rbtn2.configure(state=NORMAL)
        self.rbtn3.configure(state=NORMAL)
        self.box.set("None")
        self.tt.set("1")
        self.loop_entry["state"]='normal'
        self.device_entry.forget()
        self.box.pack(side = "left")
        self.package_lb.delete(0, self.package_lb.size()-1)
        self.button_result.forget()
        self.button_start.forget()
        f_usage = open('Usage.txt', 'rb')
        for line in f_usage:
            self.package_lb.insert(END, line)
        #self.button_type_1.forget()
        
    def test_custom(self):
        if os.path.exists("Monkey.sh") and os.path.exists("packagelist.txt"):
            #subprocess.call('adb -s ' + self.dev_id + ' shell setprop persist.tctphone.root 1', startupinfo=startupinfo)
            #sleep(5)
            subprocess.call('adb -s ' + self.dev_id + ' push ./Monkey.sh /data/local/tmp/monkey.sh', startupinfo=startupinfo)
            subprocess.call('adb -s '+ self.dev_id + ' push ./packagelist.txt /data/local/tmp/packagelist.txt', startupinfo=startupinfo)
            subprocess.call('adb -s '+ self.dev_id + ' push ./dump.sh /data/local/tmp/dump.sh', startupinfo=startupinfo)
            sleep(2)
            print 'adb -s '+ self.dev_id + ' shell sh /data/local/tmp/monkey.sh&'
            subprocess.Popen('adb -s '+ self.dev_id + ' shell sh /data/local/tmp/monkey.sh&', startupinfo=startupinfo)
            showinfo(title = "START",message = "Start Test")
        else:
            showwarning(title = "Warning",message = "Lack of necessary files")
            print "Lack of necessary files( 'Monkey.sh' or 'packagelist.txt' )"
        
    def start_button_click(self):
        case = self.rbtn_var.get()
        if case == 1:
            subprocess.Popen('adb -s '+ self.dev_id + ' shell setprop debug.tct.crash.sim disable', startupinfo=startupinfo)
            subprocess.call('adb -s ' + self.dev_id + ' push ./Monkey_system.sh /data/local/tmp/monkey_system.sh', startupinfo=startupinfo)
            subprocess.call('adb -s '+ self.dev_id + ' push ./dump.sh /data/local/tmp/dump.sh', startupinfo=startupinfo)
            print 'adb -s '+ self.dev_id + ' shell sh /data/local/tmp/monkey_system.sh&'
            subprocess.Popen('adb -s '+ self.dev_id + ' shell sh /data/local/tmp/monkey_system.sh '+str(self.type1_times)+' &', startupinfo=startupinfo)
            print "test1"
        elif case == 2:
            print "test2"
            self.package_lb.selection_set(0, self.package_lb.size()-1)
            if not os.path.exists("packagelist.txt"):
                self.create_button_click()
            self.test_custom()
        elif case == 3:
            print "test3"
            self.test_custom()
        else:
            showwarning(title = "Warning",message = "Unknow test Type")
            print "Unknow test Type"
     
    #def script_debug(self):
    #    print self.rbtn_var.get()
        
    def get_result_click(self):
        if not os.path.exists("./" + self.dev_id):
            os.mkdir("./" + self.dev_id)
            sleep(1)
        if self.case_num == 1:
            subprocess.Popen('adb pull /data/local/tmp/type1_monkeylog.txt ./'+ self.dev_id, startupinfo=startupinfo)
            return_value = subprocess.Popen('adb pull /data/local/tmp/type1_adblog.txt ./'+ self.dev_id, startupinfo=startupinfo)
            showinfo(title = "Waiting",message = "Waiting for getting TYPE1 results")
        else:
            return_value = subprocess.Popen('adb pull /data/local/tmp/monkey_test/ ./'+ self.dev_id, startupinfo=startupinfo)
            showinfo(title = "Waiting",message = "Waiting for getting TYPE2(3) results")
        return_value.wait()
        showinfo(title = "Finish",message = "Get results finished")
               
    def quit_button_click(self):
        self.parent.destroy()
        
    def get_package_list(self):
        self.package_lb.delete(0, self.package_lb.size()-1)
        adb_command = 'adb -s ' + self.dev_id + ' shell pm list packages'
        return_value = subprocess.Popen(adb_command, stdout = subprocess.PIPE, startupinfo=startupinfo).stdout.readlines()
        if self.case_num == 3:
            return_value.sort()
        index = 0
        for line in return_value:
            index += 1
            content= "%03d %s" %(index,line)
            self.package_lb.insert(END, content)
            
    def set_test_times(self):
        self.case_num = self.rbtn_var.get()
        if self.case_num == 1:
            self.type1_times = self.tt.get()
            if self.type1_times < 20:
                self.type1_times = 20
            self.tt.set(self.type1_times)
            self.test_times = self.type1_times
        else:
            self.type23_times = self.tt.get()
            if self.type23_times >= 600000:
                self.type23_times = 1
            self.tt.set(self.type23_times)
            self.test_times = self.type23_times
        print self.type1_times, self.type23_times
        
if __name__ == '__main__':
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
    else:
        startupinfo = None
        
    if os.path.exists("packagelist.txt"):
        os.remove("packagelist.txt")
    root = Tk()
    root.title("Monkey Tester")
    app = Application(root)
    root.mainloop()
