
def register_addon():

    # Menus
    from ..menu import register_menus  # 找到menu資料匣(init.py)，提取register_menus
    register_menus()
    
    # Operators
    from ..operator import register_operators  # 找到operator資料匣(init.py)，提取register_operators
    register_operators()

    # Property
    from ..property import register_property  # 找到property資料匣(init.py)，提取register_property
    register_property()

    # Keymaps
    from .keymap import register_keymap  # 找到register資料匣(keymap.py)，提取register_keymap
    register_keymap ()



def unregister_addon():

    # Menus
    from ..menu import unregister_menus  # 找到menu資料匣(init.py)，提取register_menus
    unregister_menus()

    # Operators
    from ..operator import unregister_operators   # 找到operator資料匣(init.py)，提取unregister_operators
    unregister_operators()

    # Property
    from ..property import unregister_property  # 找到property資料匣(init.py)，提取unregister_property
    unregister_property()

    # Keymaps
    from .keymap import unregister_keymap  # 找到register資料匣(keymap.py)，提取unregister_keymap
    unregister_keymap ()