import bpy


class MIMU_MT_Key_Menu(bpy.types.Menu):
    bl_idname = "MIMU_MT_Key_Menu"
    bl_label = "My IMU - Stream Test"


    def draw(self, context):

        layout = self.layout

        layout.operator_context = "INVOKE_DEFAULT"
        layout.label(text = "IMU Test ver0.0.1")

        layout.operator("mimu.run_imu", text = "Run IMU Test", icon = "GHOST_DISABLED")
