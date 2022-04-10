import sys
#this must point to a pyserial install dir for the OS (makes it work with Blender version currently running)
sys.path.append("C:\\Program Files\\Blender Foundation\\Blender 2.93\\2.93\\python\\lib")

import bpy
import serial
import time
import math
import mathutils

from ..utility.sensor import Sensor
from ..utility.serial import serial_ports

class MIMU_OP_Run_IMU(bpy.types.Operator):
    """Run IMU Testing."""

    bl_idname = "mimu.run_imu"                      # 可以在bpy.mimu.run_imu下找到Run IMU
    bl_label = "Run IMU"                            # 用在operator search的關鍵字
    bl_options = {'REGISTER', 'UNDO', "BLOCKING"}   # 可以在使用operator之後用Ctrl+Z Undo
    _timer = None
    armerture = None
    sensors = None
    readCount = 0

    @classmethod                    # 綁定在類別上，不需要實際建立物件即可呼叫
    def poll(cls, context):         
        return True

    def invoke(self, context, event):
        scene = context.scene
        mytool = scene.my_tool
        self.armerture = bpy.data.objects['Armature']
        if self.armerture == None:              #沒東西可選會是None Type，裡面沒有type選項
            # if context.active_object.type == 'MESH':
            #     self.objs = bpy.context.selected_objects
            # self.objs = bpy.context.selected_pose_bones_from_active_object
            # bpy.data.objects['Armature'].pose.bones['mixamorig:LeftArm']            
            print('dont select a thing')
            return {'CANCELLED'}
        com = mytool.my_COM
        try:
            self.ser = serial.Serial(com, '115200')
        except:
            print("Serial failed")
            return {'CANCELLED'}


        self.sensors = self.SetupSensors(scene)

        self._timer = context.window_manager.event_timer_add(0.005, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

   
    def execute(self, context):
        if(self.ser.is_open):
            as_bytes = ''
            # print(self.ser.in_waiting)
            while(self.ser.in_waiting > 40):
                try:
                    as_bytes = self.ser.readline()
                except:
                    print("as_bytes failed")
                    self.readCount += 1
                    if self.readCount > 500:
                        print("COM Port failed")
                        self._finish(context)
                # print(len(as_bytes))

                if(len(as_bytes) > 20):
                        self.readCount = 0
                        for sensor in self.sensors:
                            sensor.ReadnSet(as_bytes)

    # 輸入事件
    def modal(self, context, event):
        if event.type == 'TIMER':
            self.execute(context)

        if event.type == 'MIDDLEMOUSE': # Free navigation
            return {'PASS_THROUGH'}
            
        elif event.type == 'LEFTMOUSE':  # Confirm
            return {'PASS_THROUGH'}
            # print('Confirm')
            # self._finish(context)
            # return {'FINISHED'}

        elif event.type in ('RIGHTMOUSE', 'ESC'):  # Cancel
            print('Cancel')
            self._finish(context)
            return {'CANCELLED'}


        return {'RUNNING_MODAL'}

    
    def _finish(self, context):
        context.window_manager.event_timer_remove(self._timer)
        self.ser.close()
        {'CANCELLED'}

    def GetArmature():
        arm = bpy.data.objects['Armature']
        arm.rotation_mode = 'QUATERNION'
        return arm

    def SetupSensors(self, scene):
        mytool = scene.my_tool
        Sensors = []
                
        #Right Arm
        UpperArmRight = Sensor("upper_arm.R")
        # UpperArmRight.set_bonename("mixamorig:RightArm")
        UpperArmRight.setup_bone("mixamorig:RightArm", self.armerture)
        UpperArmRight.set_devicename('6')
        Sensors.append(UpperArmRight)

        LowerArmRight = Sensor("forearm.R")
        LowerArmRight.setup_bone("mixamorig:RightForeArm", self.armerture)
        LowerArmRight.set_devicename("5")
        Sensors.append(LowerArmRight)

        HandRight = Sensor("hand.R")
        HandRight.setup_bone("mixamorig:RightHand", self.armerture)
        HandRight.set_devicename("4")
        Sensors.append(HandRight)
        
        return Sensors