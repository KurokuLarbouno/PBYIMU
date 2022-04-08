bl_info = {
    "name": "Kun IMU Tools",
    "description": "Tools for live capture and read in of Motion Capture Suit",
    "author": "Kun",
    "version": (0, 1, 0),
    "blender": (2, 93, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Motion Capture"
}
    
    
def register():
    from .addon.register import register_addon
    register_addon()


def unregister():
    from .addon.register import unregister_addon
    unregister_addon()
