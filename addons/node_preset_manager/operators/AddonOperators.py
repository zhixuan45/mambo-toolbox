import bpy
import json
import os
from ..__init__ import dir_init_main, dir_presets

from ..config import __addon_name__
from ..preference.AddonPreferences import ExampleAddonPreferences

class NODE_OT_save_node_preset(bpy.types.Operator):
    bl_idname = "node.save_node_preset"
    bl_label = "保存节点预设"
    
    filepath : bpy.props.StringProperty(subtype='FILE_PATH')
    
    def execute(self, context):
        node_tree = context.space_data.edit_tree
        
        def convert_blender_data(value):
            """统一处理Blender数据类型转换"""
            if hasattr(value, '__iter__'):
                return [float(v) for v in value]  # 处理Vector/Color等可迭代类型
            try:
                return float(value)  # 处理普通数值
            except (TypeError, ValueError):
                return str(value)  # 其他类型转为字符串
        
        nodes_data = {
            'nodes': [{
                'bl_idname': n.bl_idname,
                'name': n.name,  # 新增节点名称保存
                'location': [float(x) for x in n.location],  # 确保转换为Python列表
                'inputs': [{
                    'default_value': convert_blender_data(getattr(i, 'default_value', None)),
                    'name': i.name
                } for i in n.inputs],
                'outputs': [{
                    'default_value': convert_blender_data(getattr(o, 'default_value', None)),
                    'name': o.name
                } for o in n.outputs]
            } for n in node_tree.nodes],
            'links': [
                {
                    'from_node': link.from_node.name,
                    'from_socket': link.from_socket.identifier,  # 使用唯一标识符
                    'to_node': link.to_node.name,
                    'to_socket': link.to_socket.identifier
                } for link in node_tree.links
            ]
        }
        
        with open(self.filepath, 'w') as f:
            json.dump(nodes_data, f, indent=2)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

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
            
            # 加载节点数据
            node_map = {}
            for node_info in nodes_data['nodes']:
                node = node_tree.nodes.new(node_info['bl_idname'])
                node.name = node_info['name']
                node.location = node_info['location']
                node_map[node_info['name']] = node

                # 处理输入值
                for i, input_info in enumerate(node_info.get('inputs', [])):
                    if i < len(node.inputs) and input_info['default_value'] is not None:
                        try:
                            val = input_info['default_value']
                            if isinstance(val, list):
                                node.inputs[i].default_value = tuple(val)
                            else:
                                node.inputs[i].default_value = float(val)
                        except Exception as e:
                            print(f"输入值设置失败：{node.name}.{i} - {str(e)}")
                
                # 处理输出值
                for o, output_info in enumerate(node_info.get('outputs', [])):
                    if o < len(node.outputs):
                        try:
                            val = output_info.get('default_value', [])
                            node.outputs[o].default_value = val if isinstance(val, float) else tuple(val)
                        except Exception as e:
                            print(f"输出值设置失败：{node.name}.{o} - {str(e)}")

            # 重建连接
            for link_info in nodes_data.get('links', []):
                try:
                    from_node = node_map[link_info['from_node']]
                    to_node = node_map[link_info['to_node']]
                    from_socket = next(s for s in from_node.outputs if s.identifier == link_info['from_socket'])
                    to_socket = next(s for s in to_node.inputs if s.identifier == link_info['to_socket'])
                    node_tree.links.new(to_socket, from_socket)
                except Exception as e:
                    print(f"连接重建失败：{str(e)}")
            
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"加载预设失败: {str(e)}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class NODE_OT_load_builtin_preset(bpy.types.Operator):
    bl_idname = "node.load_builtin_preset"
    bl_label = "加载内置预设"
    preset_name: bpy.props.StringProperty() # type: ignore

    def execute(self, context):
        preset_name = self.preset_name
        preset_path = os.path.join(dir_presets, f"builtin_preset_{preset_name}.json")
        if os.path.exists(preset_path):
            print(f"加载内置预设：{preset_name}")
            # 直接调用 load_node_preset 操作符，不传递 filepath
            bpy.ops.node.load_node_preset(filepath=preset_path)
        return {'FINISHED'}