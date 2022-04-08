import bpy

class MyProperties(bpy.types.PropertyGroup):
    
    my_string : bpy.props.StringProperty(name= "File Location")
    
    my_float_vector6 : bpy.props.FloatVectorProperty(name= "R_UpArm", subtype='XYZ', precision=4, size=3, default= (0,0,0))
    my_float_vector5 : bpy.props.FloatVectorProperty(name= "R_Fore", subtype='XYZ', precision=4, size=3, default= (0,0,0))
    my_float_vector4 : bpy.props.FloatVectorProperty(name= "R_Hand", subtype='XYZ', precision=4, size=3, default= (0,0,0))
    
    my_sync : bpy.props.BoolProperty(name= "sync", description= "control sync", default= False)

    my_COM : bpy.props.EnumProperty(
        name= "Serial Port",
        description= "Working Serial Port",
        items= [
            ('NONE', "NONE", ""),
            ('COM4', "COM4", ""),
            ("COM5", "COM5", ""),
            ("COM6", "COM6", ""),
            ("COM7", "COM7", ""),
            ("COM8", "COM8", ""),
            ("COM9", "COM9", ""),
        ],
    )

        
    def add_items_from_collection_callback(self, context):
        items = []
        scene = context.scene
        for item in scene.my_items.values():
            items.append((item.my_COM, item.my_COM, ""))
        return items