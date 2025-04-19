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
        layout.operator("node.save_node_preset")
        layout.operator("node.load_node_preset")
        
        # 内置预设面板
        box = layout.box()
        box.label(text="内置预设")
        row = box.row()
        row.prop(context.scene, 'node_preset_items', text="")
        row.operator("node.load_builtin_preset", text="加载")
