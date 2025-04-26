import bpy
import json
import os
from ..__init__ import dir_init_main, dir_presets

from ..config import __addon_name__
from ..preference.AddonPreferences import ExampleAddonPreferences

class NODE_OT_save_node_preset(bpy.types.Operator):
    bl_idname = "npm.save_node_preset"  # 原值："node.save_node_preset"

class NODE_OT_load_node_preset(bpy.types.Operator):
    bl_idname = "node.load_node_preset"
    bl_label = "加载节点预设"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH') # type: ignore

    def execute(self, context):
        try:
            node_tree = context.space_data.edit_tree
            # 仅清除当前插件创建的节点，保留其他插件节点
            for node in list(node_tree.nodes):
                if node.bl_idname.startswith('NODE_'):
                    node_tree.nodes.remove(node)
            
            with open(self.filepath, 'r') as f:
                nodes_data = json.load(f)
            
            load_nodes_from_data(node_tree, nodes_data)
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"加载预设失败: {str(e)}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class NODE_OT_load_builtin_preset(bpy.types.Operator):
    bl_idname = "npm.load_builtin_preset"  # 原值："node.load_builtin_preset"
    bl_label = "加载内置预设"

    def execute(self, context):
        preset_name = context.scene.node_preset_items
        preset_path = os.path.join(dir_presets, f"builtin_preset_{preset_name}.json")
        if os.path.exists(preset_path):
            print(f"加载内置预设：{preset_name}")
            # 直接调用 load_node_preset 操作符，不传递 filepath
            bpy.ops.node.load_node_preset(filepath=preset_path)
        return {'FINISHED'}