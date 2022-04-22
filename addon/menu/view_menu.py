import bpy



class MIMU_PT_View_Menu(bpy.types.Panel):
    bl_label = "My IMU - Control Panel"
    bl_idname = "MIMU_PT_View_Menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "My IMU"
 
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        row = layout.row()
        row.label(text = "My IMU Tool", icon = 'MEMORY')
        row = layout.row()     
        
        # layout.operator("addonname.myop_calibrate")
        
        layout.operator("mimu.check_sp", text="Check Serial")
        row = layout.row()
        
        layout.prop(mytool, "my_string")
        row = layout.row()

        layout.prop(mytool, "my_float_vector6")
        layout.prop(mytool, "my_float_vector5")
        layout.prop(mytool, "my_float_vector4")
        row = layout.row()

        layout.prop(mytool, "my_quat_vector6")
        layout.prop(mytool, "my_quat_vector5")
        layout.prop(mytool, "my_quat_vector4")
        row = layout.row()

        layout.prop(mytool, "my_COM")
        row = layout.row()

        row = layout.row(align=True)
        row.prop(mytool, "my_sync", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("mimu.run_imu", text="Sync")
        row = layout.row(align=False)

        sub = row.row()
        sub.operator("mimu.tpose", text="Tpose")

        #testing
        # layout.operator("mimu.run_imu")
        # layout.prop(context.scene.my_COM_items, "asdf")