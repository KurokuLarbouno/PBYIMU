import bpy

from .key_menu import MIMU_MT_Key_Menu # 找到key_menu.py，匯入 class MIMU_MT_Key_Menu
from .view_menu import MIMU_PT_View_Menu # 找到view_menu.py，匯入 class MIMU_PT_View_Menu

# python tuple type，必定包含2個或更多的element，所以在這裡需要再唯一元素旁加一個逗號
classes = (
    MIMU_MT_Key_Menu, MIMU_PT_View_Menu
)

# 註冊自己在classes的menu
def register_menus():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

# 解除註冊自己在classes的operator
def unregister_menus():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)