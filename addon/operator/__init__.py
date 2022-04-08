import bpy

from .check_serial import MIMU_OP_Check_SP  # check_serial.py，匯入 class MIMU_OP_Check_SP
from .run_IMU import MIMU_OP_Run_IMU        # 找到run_IMU.py，匯入 class MIMU_OP_Run_IMU
from .tpose import MIMU_OP_Tpose            # tpose.py，匯入 class MIMU_OP_Tpose

# python tuple type，必定包含2個或更多的element，所以在這裡需要再唯一元素旁加一個逗號
classes = (
    MIMU_OP_Run_IMU, MIMU_OP_Check_SP, MIMU_OP_Tpose
)

# 註冊自己在classes的operator
def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

# 解除註冊自己在classes的operator
def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)