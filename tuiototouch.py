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
        uinput.EV_ABS: [uinput.ABS_MT_POSITION_X, uinput.ABS_MT_POSITION_Y,uinput.ABS_MT_TRACKING_ID],
        }
        abs_parameters = {uinput.ABS_MT_POSITION_X:(0, 1000, 0, 0), uinput.ABS_MT_POSITION_Y:(0, 1000, 0, 0),
        uinput.ABS_MT_TRACKING_ID:(0, 10, 0, 0)}
        self.device=uinput.Device(name="TUIO-multitouch")
        self.device.capabilities=capabilities
        self.device.abs_parameters=abs_parameters
        self.x_mouse=0
        self.y_mouse=0
        self.cpt=0

    def update(self,list_obj,list_cursors):
        list=set(list_obj).union(set(list_cursors))
        self.objects.clear()
        for obj in list:
            self.objects[obj.sessionid]=obj

    def display(self):
        if (len(self.objects)==0) & self.empty:
            print ("type :%d code : %d value : %d" % (uinput.EV_KEY, uinput.BTN_TOUCH, 0))
            self.device.emit(uinput.EV_KEY, uinput.BTN_TOUCH, 0)
            self.empty=0
        i=0
        for key in self.objects:
            if not self.empty:
                print ("type :%d code : %d value : %d" % (uinput.EV_KEY, uinput.BTN_TOUCH, 1))
                self.device.emit(uinput.EV_KEY, uinput.BTN_TOUCH, 1)
            self.empty=1
            obj=self.objects[key]
            print ("type :%d code : %d value : %d" % (uinput.EV_ABS, uinput.ABS_MT_TRACKING_ID, obj.sessionid))
            self.device.emit(uinput.EV_ABS, uinput.ABS_MT_TRACKING_ID, obj.sessionid, syn=False)
            print ("type :%d code : %d value : %d" % (uinput.EV_ABS, uinput.ABS_MT_POSITION_X, obj.xpos*1000))
            self.device.emit(uinput.EV_ABS, uinput.ABS_MT_POSITION_X, obj.xpos*1000, syn=False)
            print ("type :%d code : %d value : %d" % (uinput.EV_ABS, uinput.ABS_MT_POSITION_Y, obj.ypos*1000))
            self.device.emit(uinput.EV_ABS, uinput.ABS_MT_POSITION_Y, obj.ypos*1000, syn=False)
            self.device.emit(0, 2, 0, syn=False)
            print("type :%d code : %d value : %d"%(0,2,0))
            i+=1
            if i==len(self.objects):
                self.device.emit(0,0,0,syn=False)
                print ("type :0 code :0 value :0")
                self.empty=1

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
