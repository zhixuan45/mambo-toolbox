import bpy

from ..config import __addon_name__
from ....common.i18n.i18n import i18n
from ....common.types.framework import reg_order

@reg_order(0)
class NODE_PT_node_preset_panel(bpy.types.Panel):
    bl_label = "节点预设管理"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    
    def draw(self, context):
        layout = self.layout
        # 修改后的操作符引用
        layout.operator("npm.save_node_preset")
        layout.operator("npm.load_node_preset") 
        row.operator("npm.load_builtin_preset", text="加载")
