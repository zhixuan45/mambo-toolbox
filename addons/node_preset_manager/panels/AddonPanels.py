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
        # 保存和加载按钮
        layout.operator("node.save_node_preset")
        layout.operator("node.load_node_preset")
        
        # 预设按钮列表
        row = layout.row()
        row.label(text="预设列表:")
        
        # 获取presets目录下的所有JSON文件
        import os
        presets_dir = os.path.join(os.path.dirname(__file__), "..", "presets")
        if os.path.exists(presets_dir):
            for file in os.listdir(presets_dir):
                if file.endswith('.json'):
                    preset_name = os.path.splitext(file)[0]
                    row = layout.row()
                    op = row.operator("node.load_builtin_preset", text=preset_name)
                    op.preset_name = preset_name
