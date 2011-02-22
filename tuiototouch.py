#! /usr/bin/python
#
#	tuiototouch, a bridge between TUIO and Linux input for multitouch
#
#	The copyright owners for the contents of this file are:
#		Ecole Nationale de l'Aviation Civile, France (2010-2011)
#
#	main and only file
#
#	Contributors:
#		Simon Charvet <charvet@lii-enac.fr>
#
#
#	This program is provided to you as free software;
#	you can redistribute it	and/or modify it under the terms of the
#	GNU General Public License as published by the Free Software
#	Foundation; either version 2 of the License, or (at your option)
#	any later version.

import tuio
import uinput
import time

class Device(object):

    def __init__(self):
        self.objects=dict()
        self.empty=1
        self.capabilities= {
        uinput.EV_KEY: [uinput.BTN_TOUCH],
        uinput.EV_ABS: [uinput.ABS_MT_POSITION_X, uinput.ABS_MT_POSITION_Y,uinput.ABS_MT_TRACKING_ID],
        }
        self.abs_parameters = {uinput.ABS_MT_POSITION_X:(0, 1000, 0, 0), uinput.ABS_MT_POSITION_Y:(0, 1000, 0, 0),
        uinput.ABS_MT_TRACKING_ID:(0, 10, 0, 0)}
        self.device=uinput.Device(name="TUIO-multitouch")
        self.device.capabilities=self.capabilities
        self.device.abs_parameters=self.abs_parameters

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
            self.treatment(self.objects[key])
            i+=1
            if i==len(self.objects):
                self.device.emit(0,0,0,syn=False)
                print ("type :0 code :0 value :0")
                self.empty=1

    def treatment(self, obj):
            print ("type :%d code : %d value : %d" % (uinput.EV_ABS, uinput.ABS_MT_TRACKING_ID, obj.sessionid))
            self.device.emit(uinput.EV_ABS, uinput.ABS_MT_TRACKING_ID, obj.sessionid, syn=False)
            print ("type :%d code : %d value : %d" % (uinput.EV_ABS, uinput.ABS_MT_POSITION_X, obj.xpos*1000))
            self.device.emit(uinput.EV_ABS, uinput.ABS_MT_POSITION_X, obj.xpos*1000, syn=False)
            print ("type :%d code : %d value : %d" % (uinput.EV_ABS, uinput.ABS_MT_POSITION_Y, obj.ypos*1000))
            self.device.emit(uinput.EV_ABS, uinput.ABS_MT_POSITION_Y, obj.ypos*1000, syn=False)
            self.device.emit(0, 2, 0, syn=False)
            print("type :%d code : %d value : %d"%(0,2,0))

class DeviceWME(Device):

    def __init__(self):
        Device.__init__(self)
        self.capabilities[uinput.EV_ABS] = \
            [uinput.ABS_MT_POSITION_X, uinput.ABS_MT_POSITION_Y,
            uinput.ABS_MT_TRACKING_ID,
            uinput.ABS_X, uinput.ABS_Y]
        self.abs_parameters[uinput.ABS_X] = (0,1000,0,0)
        self.abs_parameters[uinput.ABS_Y] = (0,1000,0,0)
        self.device.capabilities=self.capabilities
        self.device.abs_parameters=self.abs_parameters
        self.x_mouse=0
        self.y_mouse=0

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
            obj = self.objects[key]
            if i==0:
                modified=0
                if self.x_mouse!=obj.xpos*1000:
                    modified=1
                    self.x_mouse=obj.xpos*1000
                    print ("type :3 code :0 value :%d"%self.x_mouse)
                    self.device.emit(uinput.EV_ABS, uinput.ABS_X, self.x_mouse, syn=False)
                if self.y_mouse!=obj.ypos*1000:
                    modified=1
                    self.y_mouse=obj.ypos*1000
                    print ("type :3 code :1 value :%d"%self.y_mouse)
                    self.device.emit(uinput.EV_ABS, uinput.ABS_Y, self.y_mouse, syn=False)
                if modified:
                    print ("type: 0 code :0 value :0")
                    self.device.emit(0,0,0,syn=False)
            self.treatment(obj)
            i+=1
            if i==len(self.objects):
                self.device.emit(0,0,0,syn=False)
                print ("type :0 code :0 value :0")
                self.empty=1

if __name__ == "__main__":
    import sys
    tracking=tuio.Tracking()
    if '--no-mouse-emu' in sys.argv:
        device=Device()
    else:
        device=DeviceWME()
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
