import bpy
import json
import os

from .operators import NODE_OT_save_node_preset, NODE_OT_load_node_preset

class NODE_PG_node_preset_props(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="预设名称")
    nodes_data: bpy.props.StringProperty(name="节点数据")

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

# 内置预设相关功能


def register():
    from . import operators
    
    # 注册属性组
    bpy.utils.register_class(NODE_PG_node_preset_props)
    bpy.types.Scene.node_preset_items = bpy.props.CollectionProperty(type=NODE_PG_node_preset_props)
    bpy.types.Scene.active_preset_index = bpy.props.IntProperty()
    
    # 注册操作符
    bpy.utils.register_class(operators.NODE_OT_save_node_preset)
    bpy.utils.register_class(operators.NODE_OT_load_node_preset)
    bpy.utils.register_class(operators.NODE_OT_load_builtin_preset)
    
    # 注册核心组件
    bpy.utils.register_class(NODE_PT_node_preset_panel)

def unregister():
    bpy.utils.unregister_class(NODE_PT_node_preset_panel)
    
    # 注销属性组
    del bpy.types.Scene.active_preset_index
    del bpy.types.Scene.node_preset_items
    bpy.utils.unregister_class(NODE_PG_node_preset_props)

if __name__ == "__main__":
    register()