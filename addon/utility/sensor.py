import sys
import bpy
import math
import mathutils

class Sensor(object):
    bonename = None
    bone = None
    devicename = None
    TransposeMethod = None
    offsetEuler = mathutils.Vector((0, 0, 0))
    TpCount = 0
    TpAmount = 1
    oriQuat = mathutils.Quaternion((1, 0, 0, 0))
    offsetQuat = mathutils.Quaternion((1, 0, 0, 0))

    def __init__(self, name):
        self.TransposeMethod = "XYZ" # "QUATERNION"
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
        my_tool = bpy.context.scene.my_tool
        try:
            asline = line.decode('ascii').strip()
        except:
            return -1
            
        _oldQuat = mathutils.Quaternion((1, 0, 0, 0))
        # 儲存先前骨骼位置，以防讀取失誤
        if(self.bone!= None):
            _oldQuat = self.bone.rotation_quaternion

        myQuat = self.getQuatFromLine(asline, '~', self.devicename, ',', _oldQuat)
        if (myQuat !=  None):
            if(self.bone!= None):
                self.bone.rotation_mode = self.TransposeMethod
                # if(self.TransposeMethod == 'QUATERNION'): 
                #     if(my_tool.my_sync == True):
                #         Q = self.offsetQuat
                #         if self.devicename == '6':
                #             Q = my_tool.my_quat_vector6
                #         elif self.devicename == '5':
                #             Q = my_tool.my_quat_vector5
                #         elif self.devicename == '4':                 
                #             Q = my_tool.my_quat_vector4
                #         rQuat = myQuat - Q
                #     self.bone.rotation_quaternion = rQuat
                if(self.TransposeMethod == 'XYZ'): 
                    myEuler = myQuat.to_euler('XYZ')
                    prEuler = self.getParentEulr(self.bone)
                    myEuler.rotate(prEuler)
                    if(my_tool.my_sync == True):
                        if self.devicename == '6':
                            E = my_tool.my_float_vector6
                        elif self.devicename == '5':
                            E = my_tool.my_float_vector5
                        elif self.devicename == '4':
                            E = my_tool.my_float_vector4
                        offEuler = mathutils.Euler((-E.x, -E.y, -E.z), 'XYZ')
                        myEuler.rotate(offEuler)   # 補償Tpose值

                    self.bone.rotation_euler = myEuler
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
            oE = self.offsetEuler

            myEuler = mathutils.Euler((0, 0, 0), 'XYZ')
            
            if self.TpCount < self.TpAmount:
                E = myQuat.to_euler('XYZ')
                self.offsetEuler = mathutils.Vector((oE.x+E.x, oE.y+E.y, oE.z+E.z))
                self.TpCount += 1
            else:
                oE = self.offsetEuler
                A = self.TpCount
                E = mathutils.Euler((oE.x/A, oE.y/A, oE.z/A))
                self.offsetEuler = mathutils.Euler((0, 0, 0), 'XYZ')
                myQuat = E.to_quaternion()
                # myEuler = mathutils.Euler((myEuler.x*57.3, myEuler.y*57.3,myEuler.z*57.3), 'XYZ')
                if self.devicename == '6':
                    my_tool.my_quat_vector6.w = myQuat.w 
                    my_tool.my_quat_vector6.x = myQuat.x 
                    my_tool.my_quat_vector6.y = myQuat.y 
                    my_tool.my_quat_vector6.z = myQuat.z
                    my_tool.my_float_vector6.x = E.x 
                    my_tool.my_float_vector6.y = E.y 
                    my_tool.my_float_vector6.z = E.z
                elif self.devicename == '5':
                    my_tool.my_quat_vector5.w = myQuat.w 
                    my_tool.my_quat_vector5.x = myQuat.x
                    my_tool.my_quat_vector5.y = myQuat.y
                    my_tool.my_quat_vector5.z = myQuat.z
                    my_tool.my_float_vector5.x = E.x 
                    my_tool.my_float_vector5.y = E.y 
                    my_tool.my_float_vector5.z = E.z
                elif self.devicename == '4':
                    my_tool.my_quat_vector4.w = myQuat.w 
                    my_tool.my_quat_vector4.x = myQuat.x 
                    my_tool.my_quat_vector4.y = myQuat.y 
                    my_tool.my_quat_vector4.z = myQuat.z
                    my_tool.my_float_vector4.x = E.x 
                    my_tool.my_float_vector4.y = E.y 
                    my_tool.my_float_vector4.z = E.z
                self.TpCount = 0

        if(self.bone!= None):
            myEuler = mathutils.Euler((0, 0, 0), 'XYZ')
            self.bone.rotation_euler = myEuler
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
                    return finalQuat  
    
    def try2GetFloat(self, str, qOld):
        try:
            qOut = float(str)
        except:
            print("GetFloat failed")
            qOut = qOld
        return qOut

    def getParentEulr(self, childBone):
        prBone = childBone.parent
        # obj = prBone.id_data
        # matrix_final = obj.matrix_world @ prBone.matrix
        # _prEuler = matrix_final.to_euler()
        if (prBone != None):
            _prEuler = prBone.rotation_euler
            return mathutils.Euler((-_prEuler.x, -_prEuler.y, -_prEuler.z), 'XYZ')
        else:
            return mathutils.Euler((0, 0, 0), 'XYZ')
