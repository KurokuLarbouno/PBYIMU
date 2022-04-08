import bpy

from .my_property import MyProperties # 找到my_property.py，匯入 class MyProperties

# python tuple type，必定包含2個或更多的element，所以在這裡需要再唯一元素旁加一個逗號
classes = (
    MyProperties,
)

# 註冊自己在classes的operator
def register_property():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
        bpy.types.Scene.my_tool = bpy.props.PointerProperty(type= MyProperties)

# 解除註冊自己在classes的operator
def unregister_property():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
        del bpy.types.Scene.my_tool