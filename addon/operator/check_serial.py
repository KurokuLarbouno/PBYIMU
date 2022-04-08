import sys

import bpy

from ..utility.serial import serial_ports

class MIMU_OP_Check_SP(bpy.types.Operator):
    """Check Serial Port."""

    bl_idname = "mimu.check_sp"                      # 可以在bpy.mimu.run_imu下找到Run IMU
    bl_label = "Check Serial Port"                            # 用在operator search的關鍵字
    bl_options = {'REGISTER', 'UNDO', "BLOCKING"}   # 可以在使用operator之後用Ctrl+Z Undo
  

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        available_sp = serial_ports()
        comlen = len(available_sp)
        if (comlen > 0):            
            try:
                mytool.my_COM = available_sp[comlen-1]
            except:
                print("Can't find in list:" + available_sp[comlen-1])
            # mytool.my_COM = self.make_enum(available_sp)
        return {'FINISHED'}
