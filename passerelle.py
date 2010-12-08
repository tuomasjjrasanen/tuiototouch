#! /usr/bin/python

__author__="Charvet Simon"
__date__ ="$2 nov. 2010 10:09:35$"

import tuio
import uinput
import time

class Device:

    def __init__(self):
        self.objects=dict()
        self.empty=1
        capabilities= {
        uinput.EV_KEY: [uinput.BTN_TOUCH],
        uinput.EV_ABS: [uinput.ABS_MT_POSITION_X, uinput.ABS_MT_POSITION_Y,uinput.ABS_MT_TRACKING_ID, uinput.ABS_X, uinput.ABS_Y],
        }
        abs_parameters = {uinput.ABS_MT_POSITION_X:(0, 1000, 0, 0), uinput.ABS_MT_POSITION_Y:(0, 1000, 0, 0),
        uinput.ABS_MT_TRACKING_ID:(0, 10, 0, 0), uinput.ABS_X:(0,1000,0,0), uinput.ABS_Y:(0,1000,0,0)}
        self.device=uinput.Device(name="TUIO-multitouch")
        self.device.capabilities=capabilities
        self.device.abs_parameters=abs_parameters
        self.x_mouse=0
        self.y_mouse=0
        self.x=[]
        self.y=[]
        self.cpt=0
        self.press=0

    def update(self,list_obj,list_cursors):
        list=set(list_obj).union(set(list_cursors))
        self.objects.clear()
        for obj in list:
            self.objects[obj.sessionid]=obj

    def display(self):
        if len(self.objects)==0 and self.empty:
            self.empty=0
            #self.device.emit(uinput.EV_KEY, uinput.BTN_TOUCH, 0)
            #print ("type :%d code : %d value : %d" % (uinput.EV_KEY, uinput.BTN_TOUCH, 0))
        i=1
        for key in self.objects:
            obj=self.objects[key]
            self.device.emit(uinput.EV_ABS, uinput.ABS_MT_TRACKING_ID, obj.sessionid, syn=False)
            print ("type :%d code : %d value : %d" % (uinput.EV_ABS, uinput.ABS_MT_TRACKING_ID, obj.sessionid))
            self.device.emit(uinput.EV_ABS, uinput.ABS_MT_POSITION_X, obj.xpos*1000, syn=False)
            print ("type :%d code : %d value : %d" % (uinput.EV_ABS, uinput.ABS_MT_POSITION_X, obj.xpos*1000))
            self.device.emit(uinput.EV_ABS, uinput.ABS_MT_POSITION_Y, obj.ypos*1000, syn=False)
            print ("type :%d code : %d value : %d" % (uinput.EV_ABS, uinput.ABS_MT_POSITION_Y, obj.ypos*1000))
            self.device.emit(0, 2, 0, syn=False)
            print("type :%d code : %d value : %d"%(0,2,0))
            self.x.append(obj.xpos*1000)
            self.y.append(obj.ypos*1000)
            if (max(self.x)-min(self.x)<10)&(max(self.y)-min(self.y)<10):
                self.cpt+=1
                self.rectangle=1
                print self.cpt
            else:
                self.cpt=0
                self.rectangle=0
                self.x=[]
                self.y=[]
            if self.rectangle & (self.cpt>200):
                if self.press:
                    self.device.emit(uinput.EV_KEY, uinput.BTN_TOUCH, 0)
                    print ("type :%d code : %d value : %d" % (uinput.EV_KEY, uinput.BTN_TOUCH, 0))
                    self.press=0
                else:
                    self.device.emit(uinput.EV_KEY, uinput.BTN_TOUCH, 1)
                    print ("type :%d code : %d value : %d" % (uinput.EV_KEY, uinput.BTN_TOUCH, 1))
                    self.press=1
                self.x=[]
                self.y=[]
                self.cpt=0
                self.rectangle=0
            if self.empty:
                if self.x_mouse!=obj.xpos*1000:
                    self.x_mouse=obj.xpos*1000
                    self.device.emit(uinput.EV_ABS, uinput.ABS_X, self.x_mouse,syn=False)
                    print ("type :3 code :0 value :%d"%self.x_mouse)
                if self.y_mouse!=obj.ypos*1000:
                    self.y_mouse=obj.ypos*1000
                    self.device.emit(uinput.EV_ABS, uinput.ABS_Y, self.y_mouse,syn=False)
                    print ("type :3 code :1 value :%d"%self.y_mouse)
                self.empty=0
            else:
                print "reset"
                self.cpt=0
                self.empty=0
            if i==len(self.objects):
                self.device.emit(0,0,0,syn=False)
                print ("type :0 code :0 value :0")
                self.empty=1
            i+=1

if __name__ == "__main__":
    tracking=tuio.Tracking()
    device=Device()
    try:
        while 1:
            tracking.update()
            objects=tracking.objects()
            cursors=tracking.cursors()
            device.update(objects,cursors)
            device.display()
            time.sleep(0.01)
    except KeyboardInterrupt:
        tracking.stop()
