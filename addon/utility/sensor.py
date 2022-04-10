import sys
import bpy
import math
import mathutils

class Sensor(object):
    bonename = None
    bone = None
    devicename = None
    TransposeMethod = None
    offsetEuler = None
    TpCount = 0
    TpAmount = 50
    oriQuat = mathutils.Quaternion((1, 0, 0, 0))
    offsetQuat = mathutils.Quaternion((1, 0, 0, 0))

    def __init__(self, name):
        """Return a Customer object whose name is *name*.""" 
        self.TransposeMethod = "QUATERNION"
        self.devicename = name
        self.bonename = name

    def set_bonename(self, name):
        # 儲存初始骨骼
        self.bonename = name

    def setup_bone(self, name, armerture):
        self.bonename = name
        self.bone = armerture.pose.bones[self.bonename]
        self.bone.rotation_mode = self.TransposeMethod
        oriQuat = self.bone.rotation_quaternion

    def set_devicename(self, name):
        self.devicename = name

    def ReadnSet(self, line):
        try:
            asline = line.decode('ascii').strip()
        except:
            return -1
            
        _oldQuat = mathutils.Quaternion((1, 0, 0, 0))
        # 儲存先前骨骼位置，以防讀取失誤
        if(self.bone!= None):
            self.bone.rotation_mode = "QUATERNION"
            _oldQuat = self.bone.rotation_quaternion

        myQuat = self.getQuatFromLine(asline, '~', self.devicename, ',', _oldQuat)
        if (myQuat !=  None):
            if(self.bone!= None):            
                self.bone.rotation_mode = self.TransposeMethod
                self.bone.rotation_quaternion = myQuat
            else:
                print("Empty bone"+self.devicename)

    def Tpose(self, line):
        my_tool = bpy.context.scene.my_tool
        try:
            asline = line.decode('ascii').strip()
        except:
            return -1

        defaultQuat = mathutils.Quaternion((1, 0, 0, 0))

        myQuat = self.getQuatFromLine(asline, '~', self.devicename, ',', defaultQuat)

        if (myQuat !=  None):
            myEuler = mathutils.Euler((0, 0, 0), 'XYZ')
            
            if self.TpCount < self.TpAmount:
                self.offsetQuat += myQuat
                self.TpCount += 1
            else:
                Q = self.offsetQuat
                A = self.TpCount
                self.offsetQuat = mathutils.Quaternion((Q.w/A, Q.x/A, Q.y/A, Q.z/A))
                myEuler = self.offsetQuat.to_euler('XYZ')
                myEuler = mathutils.Euler((myEuler.x*57.3, myEuler.y*57.3,myEuler.z*57.3), 'XYZ')
                if self.devicename == '6':
                    my_tool.my_float_vector6.x = myEuler.x
                    my_tool.my_float_vector6.y = myEuler.y
                    my_tool.my_float_vector6.z = myEuler.z
                elif self.devicename == '5':
                    my_tool.my_float_vector5.x = myEuler.x
                    my_tool.my_float_vector5.y = myEuler.y
                    my_tool.my_float_vector5.z = myEuler.z
                elif self.devicename == '4':
                    my_tool.my_float_vector4.x = myEuler.x
                    my_tool.my_float_vector4.y = myEuler.y
                    my_tool.my_float_vector4.z = myEuler.z
                self.TpCount = 0

        if(self.bone!= None):
            self.bone.rotation_mode = self.TransposeMethod
            self.bone.rotation_quaternion = defaultQuat
        else:
            print("Empty bone")
        return(0)
    
    def getQuatFromLine(self, textLine, textHeader, deviceHeader, splitter, oldQuat):
        """從字串分離出四元數回傳"""
        my_tool = bpy.context.scene.my_tool
        # 分離標頭
        if(textHeader != None and splitter != None and textLine != None):
            TextAfterHeader = textLine.split(textHeader)
            TextAfterSplitter = TextAfterHeader[len(TextAfterHeader)-1].split(splitter)      # 取距離換行最近header之間為資料來源

            if(len(TextAfterSplitter) == 5 and deviceHeader == TextAfterSplitter[0]):
                qW = self.try2GetFloat(TextAfterSplitter[1], oldQuat.w)
                qX = self.try2GetFloat(TextAfterSplitter[2], oldQuat.x)
                qY = self.try2GetFloat(TextAfterSplitter[3], oldQuat.y)
                qZ = self.try2GetFloat(TextAfterSplitter[4], oldQuat.z)
                # 檢查結果是否正確
                if(math.isnan(qW) or math.isnan(qX) or math.isnan(qY) or math.isnan(qZ)):
                    return ('Quat Error')
                else:
                    finalQuat = mathutils.Quaternion((qW, qZ, qX, qY))
                    if(my_tool.my_sync == True):
                        offEuler = mathutils.Euler((0,0,0))
                        if self.devicename == '6':
                            vector = my_tool.my_float_vector6
                        elif self.devicename == '5':
                            vector = my_tool.my_float_vector5
                        elif self.devicename == '4':
                            vector = my_tool.my_float_vector4                            
                        offEuler = mathutils.Euler((vector.x, vector.y, vector.z))
                        offQuat = offEuler.to_quaternion()
                        finalQuat = finalQuat - offQuat
                    return finalQuat  
    
    def try2GetFloat(self, str, qOld):
        try:
            qOut = float(str)
        except:
            print("GetFloat failed")
            qOut = qOld
        return qOut