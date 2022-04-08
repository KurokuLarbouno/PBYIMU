import bpy

keys = []

# 註冊自己在classes的operator
def register_keymap():
    wm = bpy.context.window_manager         # window manager
    addon_keyconfig = wm.keyconfigs.addon   # keyconfig
    kc = addon_keyconfig

    km = kc.keymaps.new(name = "3D View", space_type = "VIEW_3D")                     # keymap
    kmi = km.keymap_items.new("wm.call_menu", "X", "PRESS", ctrl=True, shift=True)   # keymap input 綁定動作
    kmi.properties.name = "MIMU_MT_Key_Menu"            #指定要喚醒的menu
    keys.append((km, kmi))


# 解除註冊自己的keymap
def unregister_keymap():
    
    for km, kmi in keys:
        km.keymap_items.remove(kmi)

    keys.clear()